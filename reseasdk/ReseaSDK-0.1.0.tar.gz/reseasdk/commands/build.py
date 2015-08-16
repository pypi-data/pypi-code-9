import argparse
import os
import stat
import subprocess
from reseasdk.helpers import render, info, error, generating, load_yaml
from reseasdk.validators import validate_build_config_yml, \
    validate_packages_yml, validate_package_yml


SHORT_HELP = "build an executable"
LONG_HELP = """
Usage: reseasdk build
"""

START_C_TEMPLATE = """\
#include <resea.h>
#undef PACKAGE_NAME
#define PACKAGE_NAME "start_apps"
#define DEFAULT_THREAD_SIZE 0x4000

Result  thread_create(Id group, const UChar *name,
                      Addr entry, Addr arg,
                      Addr stack, Size stack_size,
                      Id *r_thread, Id *r_group);
Id thread_set_status (Id thread, int status);
Id kernel_create_thread_group(void);
void thread_start_threading(void);

{% for app in start_order %}
void {{ app }}_startup();
{% endfor %}


static void app_entrypoint (void (*startup)()){

  startup();
  BUG("startup() returned");
  for(;;); // FIXME
}


void start_apps(void){
{% if with_thread %}
    Id thread, group;
{% endif %}

{% for app in start_order %}
{% if with_thread %}
    INFO("creating a startup thread named '{{ app }}'");
    thread_create(1, U"{{ app }}",
                  (Addr) app_entrypoint, (Addr) {{ app }}_startup,
                  (Addr) allocMemory(DEFAULT_THREAD_SIZE, 0),
                  DEFAULT_THREAD_SIZE, &thread, &group);
    thread_set_status(thread, 1 /* THREAD_RUNNABLE */); 
{% else %}
    INFO("starting {{ app }} (direct-startup)");
    {{ app }}_startup();
{% endif %}
{% endfor %}

{% if with_thread %}
    INFO("starting threading");
    thread_start_threading();
{% endif %}
}
"""

MAKEFILE_TEMPLATE = """\
LD_R ?= ld -r -o
MKDIR ?= mkdir

# build config
{% for k,v in config.items() %}
{{ k }} ?= {{ v }}
{% endfor %}
{% for k in config.keys() %}
export {{ k }}
{% endfor %}

# default
.PHONY: default
default: $(BUILD_DIR)/executable

# keep blank not to delete intermediate file (especially stub files)
.SECONDARY:
$(VERBOSE).SILENT:
CMDECHO = ./$(BUILD_DIR)/cmdecho

# start.o
{% for ext,compile,genstub,stub_prefix,stub_suffix in langs %}
{% if ext == 'c' %}
$(BUILD_DIR)/start.o: $(BUILD_DIR)/start.c
	$(MKDIR) -p $(@D)
	$(CMDECHO) 'COMPILE({{ ext }})' $@
	{{ compile }} $@ $<
{% endif %}
{% endfor %}

# executable
$(BUILD_DIR)/executable: \\
  {% for name,v in build_packages.items() %}
  $(BUILD_DIR)/{{name}}/__package__.o \\
  {% endfor %}
  $(BUILD_DIR)/start.o
	$(CMDECHO) LINK $@
	$(HAL_LINK) $@ $^


#
#  stub
#
{% for ext,compile,genstub,stub_prefix,stub_suffix in langs %}
{% if genstub != 'not_specified' %}
$(BUILD_DIR)/stubs/{{ ext }}/{{ stub_prefix }}%{{ stub_suffix }}: packages/%/package.yml
	$(MKDIR) -p $(@D)
	$(CMDECHO) 'GENSTUB({{ ext }})' $@
	{{ genstub }} $@ $<
{% endif %}
{% endfor %}

#
#  Files
#
{% for file in build_files %}

{% for required_by in file['required_by'] %}
{{ required_by }}: {{ file['path'] }}
{% endfor %}

{{ file['path'] }}: \\
  {% for d in file['depends'] %}
  {{ d }}
  {% endfor %}
	$(MKDIR) -p $(@D)
	$(CMDECHO) 'GEN' $@
{% for command in file['commands'] %}
	{{ command }}
{% endfor %}
{% endfor %}

{% for name,v in build_packages.items() %}
#
#  Package: {{ name }}
#
{% for ext,compile,genstub,stub_prefix,stub_suffix in v['langs'] %}

# compile ({{ ext }})
$(BUILD_DIR)/{{ name }}/%.o: \\
  packages/{{ name }}/%.{{ ext }} \\
  {% for d in v['depends'] %}
  {% if stub_prefix != 'not_specified' %}
  $(BUILD_DIR)/stubs/{{ ext }}/{{ stub_prefix }}{{ d }}{{ stub_suffix }} \\
  {% endif %}
  {% endfor %}
  $(BUILD_DIR)/Makefile
	$(MKDIR) -p $(@D)
	$(CMDECHO) 'COMPILE({{ ext }})' $@
	PACKAGE_NAME={{ name }} {{ compile }} $@ $<

{% endfor %}

# __package__.o
$(BUILD_DIR)/{{ name }}/__package__.o: \\
  {{ v['objs'] | join(" \\#  ") | replace("#", "\n") }}
	$(CMDECHO) GEN $@
	$(LD_R) $@ $(filter %.o, $^)


{% endfor %}
"""

CMDECHO = """\
#!/usr/bin/env zsh
autoload -Uz colors; colors

cmd=$1; shift
pad=${(r:$((16-${#cmd})):: :)}
echo "  ${fg[magenta]}$cmd$reset_color$pad$*"
"""


current_package = ''
package_ymls = {}


def dict_to_strdict(d):
    """Converts lists in `d` to a string.

    It converts elements in following rules:

    None -> ''
    list -> a concatenated string separated by whitespace
    """
    for k,v in d.items():
        if v is None:
            d[k] = ''
        if isinstance(v, list):
            d[k] = ' '.join(v)
        else:
            d[k] = str(v)
    return d


def get_package_yml(package):
    global package_ymls

    if package in package_ymls:
        return package_ymls[package]
    else:
        if not os.path.exists('packages/{}'.format(package)):
            get_package(package)
        yml = load_yaml('packages/{}/package.yml'.format(package),
                        validator=validate_package_yml)
        package_ymls[package] = yml
        return yml


class RecursiveDependencyError(Exception):
    pass


def tsort(deps):
    """Topological sorting by Kahn's algorithm."""
    l = []  # the result
    num = 0 # the number of all edges
    ins = {x: 0 for x in deps} # the number of in-degree edges

    # count in-degree edges
    for x in deps:
        for y in deps[x]:
            ins[y] += 1
            num += 1

    s = [] # a list of nodes with no in-defree edges
    for x in deps:
        if ins[x] == 0:
            s.append(x)

    while s:
        x = s.pop()
        l.insert(0, x)
        for d in deps[x]:
            num -= 1
            ins[d] -= 1
            if ins[d] == 0:
                s.append(d)

    if num > 0:
        raise RecursiveDependencyError()

    return l
          

def get_required_packages(packages, added=None):
    """Returns a dict of required packages: `{package_name: [dependencies]}`"""

    if added is None:
        added = []

    deps = {}
    for package in packages:
        yml = get_package_yml(package)
        deps[package] = yml.get('uses', [])
        deps[package] += yml.get('requires', [])
        deps[package] += yml.get('implements', [])
        unadded = list(filter(lambda r: r not in added, deps[package]))
        added += unadded + [package]
        deps.update(get_required_packages(unadded, added=added))
    return deps


def resolve_required_packages(packages, types=None, include_themselves=False):
    """Returns a list of package names, ordered by dependency."""

    # TODO: add tests

    if types is None:
        types = ['application', 'library', 'interface', 'group']

    l = []
    for x in tsort(get_required_packages(packages)):
        if get_package_yml(x).get('category') in types:
            l.append(x)

    if not include_themselves:
        # remove the elements in `packages` from `l`
        l2 = []
        for x in l:
            if x not in packages:
                l2.append(x)
        l = l2

    return l


def get_package_dir(package):
    cwd = os.getcwd()
    # look for packages.yml
    while True:
        prev = os.getcwd()
        os.chdir("..")
        if prev == os.getcwd():
            error("packages.yml not found")
        if os.path.exists("packages.yml"):
            package_dir = os.getcwd()
            break

    yml = load_yaml('packages.yml', validator=validate_packages_yml)
    os.chdir(cwd)

    # get the path to the package
    try:
        path = os.path.join(package_dir, yml["packages"][package]["path"])
    except KeyError:
        error("package not found in packages.yml: '{}'".format(package))

    return path


def get_package(package):
    """Prepare the package in `packages` directory."""
    os.makedirs('packages', exist_ok=True)
    os.chdir('packages')

    if package == current_package:
        path = ".."
    else:
        path = get_package_dir(package)

    os.symlink(path, package)
    os.chdir('..')


def load_packages(package_yml, config, target):
    builtin_apps = config.get('BUILTIN_APPS', [])
    if package_yml.get('category') == 'application':
        builtin_apps.append(package_yml['name'])

    required = resolve_required_packages(package_yml['requires'] +
                                         [config['HAL']],
                                         include_themselves=True)

    # load all config.global.yml
    for package in required:
        config_path = 'packages/{}/config.global.yml'.format(package)
        if os.path.exists(config_path):
            yml = load_yaml(config_path).items()
            for k,v in yml:
                if isinstance(v, str):
                    v = v.strip()

                # prepend
                if k.startswith("+"):
                    k = k.lstrip("+")
                    v = config.get(k, "") + v
                config[k] = v

    return config, required, builtin_apps


def generate_makefile(target):
    global current_package

    try:
        package_yml = load_yaml('package.yml')
    except FileNotFoundError:
        error("cannot load 'package.yml': are you in a package directory?")

    current_package = package_yml['name']

    # resolve packages dependencies, download/prepare them and load their build config
    build_config = load_yaml('config.{}.yml'.format(target),
                             validator=validate_build_config_yml)
    config, required, builtin_apps = load_packages(package_yml, build_config, target)
    hal = config['HAL']

    # prepare additional packages if needed
    additional = ['c_lang']

    for x in additional:
        if x not in required:
            build_config["BUILTIN_APPS"] += [x]
            config, required, builtin_apps = load_packages(package_yml,
                                                           build_config,
                                                           target)

    # generate the build directory
    build_dir = 'build/{}'.format(target)
    config['BUILD_DIR'] = build_dir
    if not os.path.exists(build_dir):
        generating('MKDIR', build_dir)
        os.makedirs(build_dir, exist_ok=True)

    # generate start.c
    start_c_path = 'build/{}/start.c'.format(target)
    generating('GEN', start_c_path)
    with_thread = config['STARTUP_WITH_THREAD']
    start_order = resolve_required_packages(builtin_apps, types=['application'],
                      include_themselves=True)
    start_c = render(START_C_TEMPLATE, locals())

    open(start_c_path, 'w').write(start_c)

    # create log file
    log_path = 'build/{}/boot.log'.format(target)
    if not os.path.exists(log_path):
        generating('GEN', log_path)
        open(log_path, 'w').close()

    # generate cmdecho
    cmdecho_path = 'build/{}/cmdecho'.format(target)
    if not os.path.exists(cmdecho_path):
        generating('GEN', cmdecho_path)
        with open(cmdecho_path, 'w') as f:
            f.write(CMDECHO)
        os.chmod(cmdecho_path, 0o777)

    generating('GEN', 'Makefile')

    # convert a list in `config` to a string
    config = dict_to_strdict(config)

    # langs
    langs = []
    for lang in filter(lambda s: s.startswith('LANG_EXT'), config.keys()):
        e = lang.split('LANG_EXT_')[1]
        ext = config[lang]
        langs.append((
            ext,
            config.get('LANG_COMPILE_' + e, 'not_specified'),
            config.get('LANG_GENSTUB_' + e, 'not_specified'),
            config.get('LANG_STUB_PREFIX_' + e, 'not_specified'),
            config.get('LANG_STUB_SUFFIX_' + e, 'not_specified')
        ))

    # build rules of __package__.o
    libs = resolve_required_packages([current_package], types=['library'])
    build_packages = {}
    build_files = []
    for name in builtin_apps + libs + [hal]:
        if 'build' not in package_ymls[name]:
            continue
        if package_ymls[name]['build'].get('sources', []) == []:
            continue

        build_dir = 'build/{}/{}'.format(target, name)
        sources = package_ymls[name]['build']['sources']
        depends = resolve_required_packages([name], include_themselves=True) 
        objs = []
        for source in sources:
            filename = os.path.splitext(source)[0]
            objs.append('{}/{}.o'.format(build_dir, filename))

        build_files += package_ymls[name]['build'].get('files', [])
        build_packages[name] = {
            'objs': objs,
            'langs': langs,
            'depends': depends
        }

    # let's generate Makefile
    makefile = render(MAKEFILE_TEMPLATE, locals())
    open('build/{}/Makefile'.format(target), 'w').write(makefile)


def build(target, regenerate=False):
    """Builds an executable."""
    if regenerate or not os.path.exists('build/{}/Makefile'.format(target)):
        generate_makefile(target)

    # execute make(1)
    try:
        r = subprocess.call(['make', '-f', 'build/{}/Makefile'.format(target)])
    except Exception as e:
        error('failed to execute make: ' + str(e))

    if r != 0:
        error('error occurred during make')


def main(args_):
    parser = argparse.ArgumentParser(prog='reseasdk build',
                                     description='build an executable')
    parser.add_argument('-r', action='store_true', help='regenerate Makefile')
    parser.add_argument('--target', default='release', help='the build target')
    args = parser.parse_args(args_)

    build(args.target, args.r)
