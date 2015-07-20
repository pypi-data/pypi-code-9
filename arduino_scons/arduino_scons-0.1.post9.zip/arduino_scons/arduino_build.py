# Copyright (C) 2012 by Christian Fobel <christian@fobel.net>

# Based on the scons script for an Arduino sketch at:
# http://code.google.com/p/arscons/
#
# Copyright (C) 2010 by Homin Lee <ff4500@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

# You'll need the serial module: http://pypi.python.org/pypi/pyserial

# Basic Usage:
# 1. make a folder which have same name of the sketch (ex. Blink/ for Blik.pde)
# 2. put the sketch and SConstruct(this file) under the folder.
# 3. to make the HEX. do following in the folder.
#     $ scons
# 4. to upload the binary, do following in the folder.
#     $ scons upload

# Thanks to:
# * Ovidiu Predescu <ovidiu@gmail.com> and Lee Pike <leepike@gmail.com>
#     for Mac port and bugfix.
#
# This script tries to determine the port to which you have an Arduino
# attached. If multiple USB serial devices are attached to your
# computer, you'll need to explicitly specify the port to use, like
# this:
#
# $ scons ARDUINO_PORT=/dev/ttyUSB0
#
# To add your own directory containing user libraries, pass EXTRA_LIB
# to scons, like this:
#
# $ scons EXTRA_LIB=<my-extra-library-dir>
#
from glob import glob
import sys
import re
import os
import platform
from itertools import imap
from subprocess import check_call, CalledProcessError
import json

import arduino_helpers.context as ah
from path_helpers import path
from SCons.Environment import Environment
from SCons.Builder import Builder


def run(cmd):
    '''
    Run a command and decipher the return code. Exit by default.
    '''
    print ' '.join(cmd)
    try:
        check_call(cmd)
    except CalledProcessError as cpe:
        print 'Error: return code: ' + str(cpe.returncode)
        sys.exit(cpe.returncode)


# WindowXP not supported os.path.samefile
def same_file(p1, p2):
    if platform.system() == 'Windows':
        ap1 = os.path.abspath(p1)
        ap2 = os.path.abspath(p2)
        return ap1 == ap2
    return os.path.samefile(p1, p2)


def get_usb_tty(rx):
    usb_ttys = glob(rx)
    if len(usb_ttys) == 1:
        return usb_ttys[0]
    else:
        return None


def gather_sources(source_root):
    source_root = path(source_root)
    return (source_root.files('*.c') + source_root.files('*.cpp') +
            source_root.files('*.S'))


def get_lib_candidate_list(sketch_path, arduino_version):
    '''
    Scan the .pde file to generate a list of included libraries.
    '''
    # Generate list of library headers included in .pde file
    lib_candidates = []
    ptn_lib = re.compile(r'^[ ]*#[ ]*include [<"](.*\.h)[>"]')
    for line in open(sketch_path):
        result = ptn_lib.findall(line)
        if result:
            lib_candidates += result

    # Hack. In version 20 of the Arduino IDE, the Ethernet library depends
    # implicitly on the SPI library.
    if arduino_version >= 20 and 'Ethernet.h' in lib_candidates:
        lib_candidates += ['SPI.h']
    return lib_candidates


class ArduinoBuildContext(object):
    def __init__(self, scons_arguments, build_root=None):
        try:
            self.config = json.load(open('arscons.json'))
        except IOError:
            self.config = None

        self.ARGUMENTS = scons_arguments
        self.VARTAB = {}

        if build_root is None:
            self.build_root = path('build')
        else:
            self.build_root = path(build_root)
        self.build_root = self.build_root.abspath()
        self.core_root = self.build_root.joinpath('core')
        if not self.core_root.isdir():
            self.core_root.makedirs_p()
        print '[build-core directory] %s (%s)' % (self.core_root,
                                                  self.core_root.isdir())
        self.resolve_config_vars()

    # Reset
    def pulse_dtr(self, target, source, env):
        import serial
        import time
        ser = serial.Serial(self.ARDUINO_PORT)
        ser.setDTR(1)
        time.sleep(0.5)
        ser.setDTR(0)
        ser.close()

    def fix_windows_arduino_avr_ld(self):
        '''
        Check `avr-ld.exe` in Arduino home and replace if necessary.

        The linker (`avr-ld.exe`) distributed with the Windows Arduino IDE version
        1.5-1.6.5rc2 crashes for certain valid compiled code.  To work around this
        issue, the `arduino-scons` package includes an older copy of `avr-ld.exe`
        from Arduino 1.0.5.

        See [here][1] for details.

        [1]: http://forum.arduino.cc/index.php?topic=310950.30
        '''
        import pkg_resources
        import warnings

        reference_root = path(pkg_resources.resource_filename('arduino_scons',
                                                              'bin/windows'))
        current_root = path(self.ARDUINO_HOME).joinpath('hardware', 'tools',
                                                        'avr')

        for file_path in (('bin', 'avr-ld.exe'), ('avr', 'bin', 'ld.exe')):
            reference_ld = reference_root.joinpath(*file_path)
            current_ld = current_root.joinpath(*file_path)

            if not current_ld.isfile():
                return

            reference_hash = reference_ld.read_hexhash('md5')
            current_hash = current_ld.read_hexhash('md5')

            if reference_hash != current_hash:
                # Rename original `avr-ld.exe` to `avr-ld.exe.original`.
                current_ld.move(current_ld.parent.joinpath(current_ld.name +
                                                           '.original'))
                # Overwrite `avr-ld.exe` with bundled `avr-ld.exe`.
                reference_ld.copy(current_ld)
                warnings.warn('Replacing "%s" in Arduino IDE.  Original '
                              'renamed to "%s.original"' % (current_ld.name,
                                                            current_ld.name))

    def resolve_config_vars(self):
        self.AVR_BIN_PREFIX = None
        self.AVRDUDE_CONF = None

        if platform.system() in ('Darwin', ):
            # For MacOS X, pick up the AVR tools from within Arduino.app
            self.ARDUINO_HOME = self.resolve_var('ARDUINO_HOME',
                                                 '/Applications'
                                                 '/Arduino.app/Contents/'
                                                 'Resources/Java')
            self.ARDUINO_PORT = self.resolve_var('ARDUINO_PORT',
                                                 get_usb_tty('/dev/'
                                                             'cu.usbserial*'))
            self.SKETCHBOOK_HOME = self.resolve_var('SKETCHBOOK_HOME', '')
        elif platform.system() == 'Windows':
            # For Windows, use environment variables.
            self.ARDUINO_HOME = self.resolve_var('ARDUINO_HOME', None)
            if self.ARDUINO_HOME is None:
                candidate_paths = [path(os.environ['ProgramFiles'])
                                   .joinpath('Arduino')]
                for p in candidate_paths:
                    if p.isdir():
                        self.ARDUINO_HOME = p
                        break
            self.ARDUINO_PORT = self.resolve_var('ARDUINO_PORT', '')
            self.SKETCHBOOK_HOME = self.resolve_var('SKETCHBOOK_HOME', '')
        else:
            # For Ubuntu Linux (12.04 or higher)
            self.ARDUINO_HOME = self.resolve_var('ARDUINO_HOME',
                                                 '/usr/share/arduino/')
            self.ARDUINO_PORT = self.resolve_var('ARDUINO_PORT',
                                                 get_usb_tty('/dev/ttyUSB*'))
            self.SKETCHBOOK_HOME = self.resolve_var('SKETCHBOOK_HOME', '')

        self.ARDUINO_BOARD = self.resolve_var('ARDUINO_BOARD', 'uno')
        # Default to 0 if nothing is specified
        self.ARDUINO_VER = self.resolve_var('ARDUINO_VER', 0)
        # use built-in pulseDTR() by default
        self.RST_TRIGGER = self.resolve_var('RST_TRIGGER', None)
        # handy for adding another arduino-lib dir
        self.EXTRA_LIB = self.resolve_var('EXTRA_LIB', None)

        if not self.ARDUINO_HOME:
            print 'ARDUINO_HOME must be defined.'
            raise KeyError('ARDUINO_HOME')

        self.context = ah.ArduinoContext(self.ARDUINO_HOME)
        self.board = ah.Board(self.context, self.ARDUINO_BOARD)
        self.uploader = ah.Uploader(self.board)
        self.compiler = ah.Compiler(self.board)

        self.ARDUINO_CORE = self.board.get_core_dir()
        self.ARDUINO_SKEL = self.ARDUINO_CORE.joinpath('main.cpp')
        self.fix_windows_arduino_avr_ld()

        if self.ARDUINO_VER == 0:
            arduinoHeader = self.ARDUINO_CORE.joinpath('Arduino.h')
            #print "No Arduino version specified. Discovered version",
            if os.path.exists(arduinoHeader):
                #print "100 or above"
                #self.ARDUINO_VER = int(self.board['{runtime.ide.version}'][0]
                                       #.replace('_', ''))
                self.ARDUINO_VER = 100
            else:
                #print "0023 or below"
                self.ARDUINO_VER = 23
        else:
            print "Arduino version " + self.ARDUINO_VER + " specified"

        # Some OSs need bundle with IDE tool-chain
        self.AVRDUDE_CONF = self.uploader.conf_path
        self.AVR_BIN_PREFIX = self.compiler.bin_prefix

        self.ARDUINO_LIBS = [str(self.context.get_libraries_dir_by_family()
                                 [self.board.family])]
        if self.EXTRA_LIB:
            self.ARDUINO_LIBS.append(self.EXTRA_LIB)
        if self.SKETCHBOOK_HOME:
            self.ARDUINO_LIBS.append(os.path.join(self.SKETCHBOOK_HOME,
                                                  'libraries'))

        # Override MCU and F_CPU
        self.MCU = self.ARGUMENTS.get('MCU', self.board['{build.mcu}'][0])
        self.F_CPU = self.ARGUMENTS.get('F_CPU',
                                        self.board['{build.f_cpu}'][0])

        # Verify that there is a file with the same name as the folder and with
        # the extension .pde
        current_working_directory = path(os.getcwd()).name

        TARGET = None

        for possible_ext in ('.ino', '.pde'):
            if os.path.exists(current_working_directory + possible_ext):
                TARGET = current_working_directory
                break
        if TARGET is None:
            for possible_ext in ('.ino', '.pde'):
                possible_files = path('.').files('*' + possible_ext)
                if len(possible_files) == 1:
                    # There is a single file that matches an Arduino file
                    # extension, so assume it is the main sketch file.
                    TARGET = possible_files[0].namebase
        assert(TARGET is not None)

        print os.getcwd(), TARGET

        self.sketch_ext = '.ino' if os.path.exists(TARGET + '.ino') else '.pde'
        self.TARGET = TARGET
        self.sketch_path = path(TARGET + self.sketch_ext).abspath()

    def resolve_var(self, varname, default_value):
        # precedence: scons argument -> env. variable -> json config -> default value
        ret = self.ARGUMENTS.get(varname, None)
        self.VARTAB[varname] = ('arg', ret)
        if ret == None:
            ret = os.environ.get(varname, None)
            self.VARTAB[varname] = ('env', ret)
        if ret == None:
            ret = self.config_get(varname, None)
            self.VARTAB[varname] = ('cnf', ret)
        if ret == None:
            ret = default_value
            self.VARTAB[varname] = ('dfl', ret)
        return ret

    def config_get(self, varname, returns):
        if self.config:
            result = self.config.get(varname, returns)
        else:
            result = returns
        return result

    def get_board_conf(self, conf):
        return self.board['{%s}' % conf][0]

    def get_env(self, **kwargs):
        c_flags = ['-ffunction-sections', '-fdata-sections', '-fno-exceptions',
                   '-funsigned-char', '-funsigned-bitfields', '-fpack-struct',
                   '-fshort-enums', '-Os', '-Wall', '-mmcu=%s' % self.MCU]

        # Add some missing paths to CFLAGS
        # Workaround for /usr/libexec/gcc/avr/ld:
        #     cannot open linker script file ldscripts/avr5.x: No such file or directory
        # Workaround for /usr/libexec/gcc/avr/ld:
        #     crtm168.o: No such file: No such file or directory
        extra_cflags = ['-L/usr/x86_64-pc-linux-gnu/avr/lib/',
                        '-B/usr/avr/lib/avr5/', ]
        c_flags += extra_cflags

        if self.ARDUINO_BOARD == "leonardo":
            c_flags += ["-DUSB_VID=" + self.board['{build.vid}'][0]]
            c_flags += ["-DUSB_PID=" + self.board['{build.pid}'][0]]

        env_defaults = dict(CC='"' + self.AVR_BIN_PREFIX + 'gcc"',
                            CXX='"' + self.AVR_BIN_PREFIX + 'g++"',
                            AS='"' + self.AVR_BIN_PREFIX + 'gcc"',
                            CPPPATH=[self.core_root],
                            CPPDEFINES={'F_CPU': self.F_CPU, 'ARDUINO':
                                        self.ARDUINO_VER},
                            CFLAGS=c_flags + ['-std=gnu99'], CCFLAGS=c_flags,
                            ASFLAGS=['-assembler-with-cpp','-mmcu=%s' %
                                     self.MCU], TOOLS=['gcc','g++', 'as'])

        hw_variant = (self.board.get_variants_dir()
                      .joinpath(self.board['{build.variant}'][0]))
        env_defaults['CPPPATH'].append(hw_variant)

        for k, v in kwargs.iteritems():
            print 'processing kwarg: %s->%s' % (k, v)
            if k in env_defaults and isinstance(env_defaults[k], dict)\
                    and isinstance(v, dict):
                env_defaults[k].update(v)
                print '  update dict'
            elif k in env_defaults and isinstance(env_defaults[k], list):
                env_defaults[k].append(v)
                print '  append to list'
            else:
                env_defaults[k] = v
                print '  set value'
        print 'kwargs:', kwargs
        print 'env_defaults:', env_defaults
        env_arduino = Environment(**env_defaults)
        # Add Arduino Processing, Elf, and Hex builders to environment
        for builder_name in ['Processing', 'CompressCore', 'Elf', 'Hex',
                             'BuildInfo']:
            env_arduino.Append(BUILDERS={builder_name: getattr(self,
                                                               'get_%s_builder'
                                                               % builder_name
                                                               .lower())()})
        return env_arduino

    def get_avrdude_options(self):
        upload_protocol = self.get_board_conf('upload.protocol')
        upload_speed = self.get_board_conf('upload.speed')

        avrdude_opts = ['-V', '-F', '-c %s' % upload_protocol,
                        '-b %s' % upload_speed, '-p %s' % self.MCU,
                        '-P %s' % self.ARDUINO_PORT,
                        '-U flash:w:$SOURCES']

        if self.AVRDUDE_CONF:
            avrdude_opts += ['-C "%s"' % self.AVRDUDE_CONF]
        return avrdude_opts

    def get_core_sources(self):
        '''
        Generate list of Arduino core source files
        '''
        core_sources = gather_sources(self.ARDUINO_CORE)
        core_sources = [x.replace(self.ARDUINO_CORE, self.core_root)
                        for x in core_sources
                        if os.path.basename(x) not in ('main.cpp',
                                                       'wiring_pulse.S')]
        return core_sources

    def get_lib_path(self, lib):
        for lib_root in self.ARDUINO_LIBS[::-1]:
            for f in path(lib_root).walk():
                if f.parent.name == f.namebase and f.name == lib:
                    return f
        raise ValueError('Library not found: %s' % lib)

    def get_lib_sources(self, env):
        '''
        Add VariantDir references for all libraries in lib_candidates to the
        corresponding paths in arduino_libs.

        Return the combined list of source files for all libraries, relative
        to the respective VariantDir.
        '''
        lib_candidates = get_lib_candidate_list(self.sketch_path,
                                                self.ARDUINO_VER)
        all_libs_sources = []

        lib_dirs = set()
        for lib in lib_candidates:
            try:
                lib_parent = self.get_lib_path(lib).parent
                lib_dirs.add(lib_parent)
                env.Append(CPPPATH=lib_parent)
            except ValueError:
                pass

        all_libs_sources = set()

        for i, lib_dir in enumerate(lib_dirs):
            lib_dir_dir = self.build_root.joinpath('lib_dir_%02d' % i)
            env.VariantDir(lib_dir_dir, lib_dir)
            lib_dir_sources = gather_sources(lib_dir)

            util_dir = path(lib_dir).joinpath('utility')
            if os.path.exists(util_dir) and os.path.isdir(util_dir):
                lib_dir_sources += gather_sources(util_dir)
                env.Append(CPPPATH=util_dir.replace(lib_dir, lib_dir_dir))

            all_libs_sources.update([x.replace(lib_dir, lib_dir_dir)
                                     for x in lib_dir_sources])

        return all_libs_sources

    # -----------------------------------
    # Builders
    # ========
    def get_processing_builder(self):
        return Builder(action=self.processing_action)

    def get_compresscore_builder(self):
        return Builder(action=self.compress_core_action)

    def get_elf_builder(self):
        return Builder(action='"%s"' % (self.AVR_BIN_PREFIX + 'gcc') +
                       ' -mmcu=%s -Os -Wl,--gc-sections -o $TARGET $SOURCES '
                       '-lm' % ( self.MCU))

    def get_hex_builder(self):
        return Builder(action='"%s"' % (self.AVR_BIN_PREFIX + 'objcopy') +
                       ' -O ihex -R .eeprom $SOURCES $TARGET')

    def get_buildinfo_builder(self):
        return Builder(action=self.print_info_action)

    def compress_core_action(self, target, source, env):
        import re
        #core_pattern = re.compile(r'build.*/core/'.replace('/', os.path.sep))
        core_pattern = re.compile(r'build.*core')

        core_files = (x for x in imap(str, source) if core_pattern.search(x))
        target_path = path(target[0]).abspath()
        if not target_path.parent.isdir():
            target_path.parent.makedirs_p()
        for core_file in core_files:
            core_file_path = path(core_file).abspath()
            print ('[compress_core_action]', core_file_path,
                    core_file_path.isfile())
            command = [self.AVR_BIN_PREFIX + 'ar', 'rcs', target_path,
                       core_file_path]
            run(command)

    def print_info_action(self, target, source, env):
        for k in self.VARTAB:
            came_from, value = self.VARTAB[k]
            print '* %s: %s (%s)' % (k, value, came_from)
        print '* avr-size:'
        run([self.AVR_BIN_PREFIX + 'size', '--target=ihex', str(source[0])])
        # TODO: check binary size
        print ('* maximum size for hex file: %s bytes' %
               self.get_board_conf('upload.maximum_size'))

    def processing_action(self, target, source, env):
        wp = open(str(target[0]), 'wb')
        wp.write(open(self.ARDUINO_SKEL).read())

        types='''void
                int char word long
                float double byte long
                boolean
                uint8_t uint16_t uint32_t
                int8_t int16_t int32_t'''
        types=' | '.join(types.split())
        re_signature = re.compile(r'''^\s* (
            (?: (%s) \s+ )?
            \w+ \s*
            \( \s* ((%s) \s+ \*? \w+ (?:\s*,\s*)? )* \)
            ) \s* {? \s* $''' % (types, types), re.MULTILINE | re.VERBOSE)

        prototypes = {}

        for file in glob(os.path.realpath(os.curdir) + '/*' + self.sketch_ext):
            for line in open(file):
                result = re_signature.search(line)
                if result:
                    prototypes[result.group(1)] = result.group(2)

        for name in prototypes.iterkeys():
            print '%s;' % name
            wp.write('%s;\n' % name)

        for file in glob(os.path.realpath(os.curdir) + '/*' + self.sketch_ext):
            print file, self.sketch_path
            if not same_file(file, self.sketch_path):
                wp.write('#line 1 "%s"\r\n' % file)
                wp.write(open(file).read())

        # Add this preprocessor directive to localize the errors.
        source_path = str(source[0]).replace('\\', '\\\\')
        wp.write('#line 1 "%s"\r\n' % source_path)
        wp.write(open(str(source[0])).read())

    # -----------------------------------
    def build(self, hex_root=None, env_dict=None, extra_sources=None,
              register_upload=False):
        '''
        Return handle to built `.hex`-file rule.
        '''
        if hex_root is None:
            hex_root = self.build_root.joinpath('hex')
        else:
            hex_root = path(hex_root)
            if not hex_root.isabs():
                hex_root = self.build_root.joinpath(hex_root)
        hex_path = hex_root.joinpath(self.TARGET + '.hex')

        if env_dict is None:
            env_dict = {}
        env = self.get_env(**env_dict)
        print env['CPPDEFINES']

        # Convert sketch(.pde) to cpp
        env.Processing(hex_root.joinpath(self.TARGET + '.cpp'),
                       hex_root.joinpath(self.sketch_path))

        sources = [hex_root.joinpath(self.TARGET+'.cpp')]
        sources += self.get_lib_sources(env)
        if extra_sources:
            sources += [hex_root.joinpath(s) for s in extra_sources]

        # Finally Build!!
        core_sources = self.get_core_sources()

        core_objs = env.Object(core_sources)
        objs = env.Object(sources)
        objs += env.CompressCore(self.core_root.joinpath('core.a').abspath(),
                                 core_objs)

        elf_path = hex_root.joinpath(self.TARGET + '.elf')
        env.Elf(elf_path, objs)
        arduino_hex = env.Hex(hex_path, hex_root.joinpath(self.TARGET + '.elf'))

        # Print Size
        # TODO: check binary size
        MAX_SIZE = self.get_board_conf('upload.maximum_size')
        print ("maximum size for hex file: %s bytes" % MAX_SIZE)
        env.BuildInfo(None, hex_path)

        if register_upload:
            fuse_cmd = '"%s" %s' % (os.path.join(os.path
                                               .dirname(self.AVR_BIN_PREFIX),
                                               'avrdude'),
                                  ' '.join(self.get_avrdude_options()))
            print fuse_cmd

            if self.RST_TRIGGER:
                reset_cmd = '%s %s' % (self.RST_TRIGGER, self.ARDUINO_PORT)
            else:
                reset_cmd = self.pulse_dtr

            upload = env.Alias('upload', hex_path, [reset_cmd, fuse_cmd])
            env.AlwaysBuild(upload)

        # Clean build directory
        env.Clean('all', 'build/')

        env.VariantDir(self.core_root, self.ARDUINO_CORE)
        env.VariantDir(hex_root, '.')
        return arduino_hex
