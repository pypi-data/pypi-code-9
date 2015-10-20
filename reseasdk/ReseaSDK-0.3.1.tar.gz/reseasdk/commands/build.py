import argparse
import os
import stat
import subprocess
import sys
import multiprocessing
from termcolor import colored
from reseasdk.package import get_package, load_global_yml, load_build_yml, \
    load_package_yml, resolve_package_dependency, filter_package_by_category
from reseasdk.helpers import render, info, notice, error, generating, \
    load_yaml, dict_to_strdict
from reseasdk.validators import validate_package_yml



SHORT_HELP = "build an executable"
LONG_HELP = """
Usage: reseasdk build
"""

START_C_TEMPLATE = """\
#include <resea.h>
#undef PACKAGE_NAME
#define PACKAGE_NAME "start_apps"
#define DEFAULT_THREAD_SIZE 0x4000

Result core_create_thread(Id group, const UChar *name, Size name_size,
                          Id *r_thread, Id *r_group);
Result core_run_thread(Id thread, Addr entry, Addr arg,
                       Addr stack, Size stack_size);
void core_start_threading(void);

{% for app in builtin_apps %}
void {{ app }}_startup();
{% endfor %}

void {{ current_package }}_test();

static void app_entrypoint (void (*startup)()){

  startup();
  BUG("startup() returned");
  for(;;); // FIXME
}


UNUSED static void test_entrypoint (void (*test)()){

  logprintf("[start_apps] TEST: start");
  test();
  logprintf("[start_apps] TEST: end");
  for(;;); // FIXME
}

void start_apps(void){
{% if with_thread %}
    Id thread, group;
{% endif %}

{% for app in builtin_apps %}
{%  if app != 'core' %}
{% if with_thread %}
    INFO("starting '{{ app }}'");
    core_create_thread(1, (const UChar *) "{{ app }}",
                       {{ app | length }}, &thread, &group);
    core_run_thread(thread, 
                    (Addr) app_entrypoint, (Addr) {{ app }}_startup,
                    (Addr) allocMemory(DEFAULT_THREAD_SIZE, ALLOCMEM_NORMAL),
                    DEFAULT_THREAD_SIZE);
{% else %}
    INFO("starting {{ app }} (direct-startup)");
    {{ app }}_startup();
{% endif %}
{% endif %}
{% endfor %}

{% if defaults['TEST'] == 'yes' %}
{% if with_thread %}
    INFO("starting 'test_{{ current_package }}'");
    core_create_thread(1, (const UChar *) "{{ current_package }}",
                       {{ current_package | length }}, &thread, &group);
    core_run_thread(thread, 
                    (Addr) app_entrypoint, (Addr) {{ current_package }}_startup,
                    (Addr) allocMemory(DEFAULT_THREAD_SIZE, ALLOCMEM_NORMAL),
                    DEFAULT_THREAD_SIZE);
{% else %}
    logprintf("[start_apps] TEST: start");
    {{ current_package }}_test();
    logprintf("[start_apps] TEST: <fail> threading is not enabled"
              " -- cannot start a test thread");
    logprintf("[start_apps] TEST: end");
{% endif %}
{% endif %}

{% if with_thread %}
    INFO("starting threading");
    core_start_threading();
{% endif %}
}
"""

MAKEFILE_TEMPLATE = """\
.PHONY: _default
_default: default
# keep blank not to delete intermediate file (especially stub files)
.SECONDARY:
$(VERBOSE).SILENT:

# default build config
{% for k,v in defaults.items() %}
export {{ k }} = {{ v }}
{% endfor %}

# {{ filetype }}
default: $(BUILD_DIR)/{{ filetype }}
$(BUILD_DIR)/{{ filetype }}: \\
    {% for obj in objs %}
    {{ obj }} \\
    {% endfor %}

{% if filetype == 'application' %}
\t$(CMDECHO) LINK $@
\t$(HAL_LINK) $@ $^
{% else %}
\t$(CMDECHO) LD_R $@
\t$(LD_R) $@ $^
{% endif %}


{% for abbrev,ext,with_stub in langs %}
#  *.{{ ext }}
{% if with_stub %}
STUBS_{{ ext }} = \\
{% for stub in stubs %}
  $(BUILD_DIR)/stubs/{{ ext }}/$(STUB_PREFIX_{{ ext }}){{ stub }}\
$(STUB_SUFFIX_{{ ext }}) \\
{% endfor %}

$(BUILD_DIR)/stubs/{{ ext }}/$(STUB_PREFIX_{{ ext }})%\
$(STUB_SUFFIX_{{ ext }}): \
packages/%/package.yml
\t$(MKDIR) -p $(@D)
\t$(CMDECHO) GENSTUB $@
\tPACKAGE_NAME=$(PACKAGE_NAME) $(GENSTUB_{{ ext }}) $@ $<
{% endif %}
$(BUILD_DIR)/%.o: packages/%.{{ ext }} $(STUBS_{{ ext }}) $(BUILD_DIR)/Makefile
\t$(MKDIR) -p $(@D)
\t$(CMDECHO) '{{ abbrev }}' $@
\tPACKAGE_NAME=$(PACKAGE_NAME) $(COMPILE_{{ ext }}) $@ $<
{% endfor %}

# start.c
$(BUILD_DIR)/start.o: $(BUILD_DIR)/start.c $(STUBS_c) $(BUILD_DIR)/Makefile
\t$(MKDIR) -p $(@D)
\t$(CMDECHO) CC $@
\t$(COMPILE_c) $@ $<

{% for file in files %}
{% for required_by in file['required_by'] %}
{{ required_by }}: {{ file['path'] }}
{% endfor %}

{{ file['path'] }}: \\
{% for d in file['depends'] %}
    {{ d }}
{% endfor %}
\t$(MKDIR) -p $(@D)
\t$(CMDECHO) 'GEN' $@
{% for command in file['commands'] %}
\t{{ command }}
{% endfor %}
{% endfor %}

{% for package_name,config in configs.items() %}
# {{ package_name }}
$(BUILD_DIR)/{{ package_name }}/%: PACKAGE_NAME = {{ package_name }}
{% for k,v in config['set'].items() %}
$(BUILD_DIR)/{{ package_name }}/%: {{ k }} = {{ v }}
{% endfor %}
{% for k,v in config['append'].items() %}
$(BUILD_DIR)/{{ package_name }}/%: {{ k }} += {{ v }}
{% endfor %}
{% endfor %}
"""


def clear_current_line():
    """Clears the current line in the terminal."""
    print('\r\x1b[0K', end='')


def prettify_make_output(p):
    prev_is_cmd = False
    while True:
        l = p.stdout.readline().decode('utf-8').rstrip()
        if prev_is_cmd:
            clear_current_line()

        if l == '':
            break
        elif l.startswith('--> '):
            try:
                cmd, rest = l.lstrip('--> ').split(' ', 1)
                s = '{:<8} {}'.format(
                    colored(cmd, 'magenta', attrs=['bold']),
                    colored(rest, 'yellow'))
                print(s, end='')
                sys.stdout.flush()
                prev_is_cmd = True
            except ValueError:
                print(l)
                prev_is_cmd = False
        else:
            print(l)
            prev_is_cmd = False


def load_configs(args, defaults):
    defaults.setdefault('LD_R', '$(LD) -r -o')
    defaults.setdefault('MKDIR', 'mkdir')
    defaults.setdefault('CMDECHO', 'echo "-->"')
    defaults.setdefault('BUILTIN_APPS', '')

    if 'HAL' not in defaults:
        error('HAL is not speicified')  # TODO
    hal = defaults['HAL']
    build_dir = defaults['BUILD_DIR']
    current_package = defaults['PACKAGE']  # a package to be built
    # applicaitons to be embedded
    builtin_apps = defaults['BUILTIN_APPS'].split()
    packages = [current_package, hal] + builtin_apps  # packages to be embeded

    # generate the build directory
    if not os.path.exists(build_dir):
        os.makedirs(build_dir, exist_ok=True)

    if load_package_yml(current_package)['category'] == 'application':
        # current_package will be embedded
        builtin_apps.append(current_package)

    if load_package_yml(current_package)['category'] == 'interface':
        # FIXME: raise an exception instead
        error("the '{}' is an interface package".format(defaults['PACKAGE']))

    # test
    if defaults.get('TEST') == 'yes':
        if not load_build_yml(current_package).get('testable', False):
            # FIXME: raise an exception instead
            error("the '{}' is not testable".format(current_package))

        # an executable file will be built even if it is 'library'
        filetype = 'application'
        objs = []
        for obj in load_build_yml(current_package).get('test_objs', []):
            objs.append(build_dir + '/' + current_package + '/' + obj)
    elif len(builtin_apps) == 0:
        # an object file (.o) will be built (as a library)
        filetype = 'library'
        objs = []
    else:
        # an executable file will be built
        filetype = 'application'
        objs = []

    # load packages
    packages = resolve_package_dependency(
        packages, all_in_one=args['all_in_one'])

    configs = {}
    langs = []
    stubs = []
    files = []
    for package in packages:
        stubs.append(package)
        # FIXME: build config
        configs[package] = {'set': {}, 'append': {}}
        for k, v in load_build_yml(package).items():
            if k not in ['objs', 'test_objs']:  # exclude those
                if k.startswith("+"):
                    if k.lstrip("+") not in configs[package]['append']:
                        configs[package]['append'][k.lstrip("+")] = v.strip()
                    else:
                        configs[package]['append'][
                            k.lstrip("+")] += ' ' + v.strip()
                else:
                    configs[package]['set'][k] = v

        for k, v in load_global_yml(package).items():
            if k.startswith("+"):
                if k.lstrip("+") not in defaults:
                    defaults[k.lstrip("+")] = v.strip()
                else:
                    defaults[k.lstrip("+")] += ' ' + v.strip()
            else:
                if k not in defaults:
                    defaults[k] = v

    for package in filter_package_by_category(['application'], packages):
        if package != current_package:
            builtin_apps.append(package)

    for package in filter_package_by_category(
            ['application', 'library'], packages):
        for obj in load_build_yml(package).get('objs', []):
            objs.append(build_dir + '/' + package + '/' + obj)

    for package in filter_package_by_category(['library'], packages):
        yml = load_package_yml(package)
        implements = yml['implements']
        if "lang" in implements:
            for lang in yml["langs"]:
                langs.append((lang['abbrev'], lang['ext'], lang['stub']))
        if "hal" in implements:
            pass

    return locals()


def generate_files(args, cs):
    """ Generate files required to build """

    if cs['filetype'] == 'application':
        cs['with_thread'] = not args['single_app']

        # generate start.c
        with open(cs['build_dir'] + '/start.c', 'w') as f:
            f.write(render(START_C_TEMPLATE, cs))

        # c_lang is required because it is essential to compile start.c
        cs['packages'].append('c_lang')
        cs['objs'] += [cs['build_dir'] + "/start.o"]

    # generate Makefile
    makefile = render(MAKEFILE_TEMPLATE, cs)
    with open(cs['build_dir'] + '/Makefile', 'w') as f:
        f.write(makefile)

    if args["dump"]:
        print(makefile)

    return cs


def build(args):
    """Builds an executable."""

    defaults = {
        'BUILD_DIR': 'build/' + args['target'],
        'MAKEFLAGS': '-j' + str(multiprocessing.cpu_count())
    }
    for default in args['defaults']:
        if '=' not in default:
            error('invalid default variable (should be'
                  "FOO=bar form): '{}'".format(default))
        k, v = default.split('=', 1)
        defaults[k] = v

    if not os.path.exists('package.yml'):
        error("'package.yml' not found (are you in a package directory?)")

    if not defaults.get('PACKAGE'):
        yml = load_yaml('package.yml', validator=validate_package_yml)
        defaults['PACKAGE'] = yml['name']

    makefile = defaults['BUILD_DIR'] + '/Makefile'
    cs = load_configs(args, defaults)
    if args['r'] or not os.path.exists(makefile):
        generate_files(args, cs)

    # execute make(1)
    env = os.environ.copy()
    env.update(dict_to_strdict(cs['defaults']))
    try:
        p = subprocess.Popen(['make', '-f', makefile],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             env=env)
    except Exception as e:
        error('failed to execute make: ' + str(e))

    if args['no_prettify']:
        while True:
            l = p.stdout.readline().decode('utf-8').rstrip()
            if l == '':
                break
            print(l)
    else:
        prettify_make_output(p)

    if p.wait() != 0:
        error('error occurred during make')

    return cs


def main(args_):
    parser = argparse.ArgumentParser(prog='reseasdk build',
                                     description='build an executable')
    parser.add_argument('-r', action='store_true', help='regenerate Makefile')
    parser.add_argument('--target', default='release', help='the build target')
    parser.add_argument('--dump', action='store_true',
                        help='dump generated files for debugging')
    parser.add_argument('--no-prettify', action='store_true',
                        help="don't prettify output")
    parser.add_argument('--all-in-one', action='store_true',
                        help='embed all required applications so that'
                             'discovery() always succeed')
    parser.add_argument('--single-app', action='store_true',
                        help='no threading')
    parser.add_argument('defaults', nargs='*',
                        help='default variables (FOO=bar)')

    build(vars(parser.parse_args(args_)))
