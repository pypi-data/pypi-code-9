import sys
import os
from abc import ABCMeta, abstractmethod

from future.utils import with_metaclass

import env2config.util as util

logger = util.create_logger()


class AbstractProcessor(with_metaclass(ABCMeta, object)):
    def __init__(self, service, config_dir, configs_to_inject, injectables):
        self.service = service
        self.config_dir = config_dir
        self.configs_to_inject = configs_to_inject
        self.injectables = injectables

    @abstractmethod
    def process(self):
        raise NotImplementedError()


class RewriteProcessor(AbstractProcessor):
    def process(self):
        '''
        Scan over all configuration files and rewrite them.
        '''
        # convert a dict like {name: (filename, value), ...}
        # to a nest dict like {filename: {name: value, ...}, ...}
        # should this be the canonical format?

        logger.debug('injectables dict %s', self.injectables)

        injectables_by_config = dict(
            (filename, {})
            for filename in self.service.default_configs()
        )

        for config_name, (config_filename, config_value) in self.injectables.items():
            injectables_by_config[config_filename][config_name] = config_value

        logger.debug('converted injectables to nest dict %s', injectables_by_config)
        logger.debug('wtf %s', self.configs_to_inject)

        for src, dest in self.configs_to_inject.items():
            default = os.path.join(self.config_dir, src)
            logger.debug('considering default config %s', default)

            with open(default) as f:
                default_content = f.read()

            default_model = self.service.parse_file(default_content)
            logger.debug('parsed default file %s into model with keys %s', default, default_model.keys())

            src_filename = os.path.basename(src)  # src might be an absolute path.
            override_model = injectables_by_config[src_filename]

            logger.debug('injecting model %s', override_model)
            new_content = str(self.service.inject_file(default_model, override_model))

            if dest == '-':
                sys.stdout.write(new_content)
            else:
                with open(dest, 'wb') as f:
                    f.write(new_content)


class LineProcessor(AbstractProcessor):
    def process(self):
        '''
        Scan over all configuration files and inject all injectables.
        Has O(N*M) complexity, where N is len(default_configs)
        and M is len(injectables).  Can we do better?
        '''
        for src, dest in self.configs_to_inject.items():
            default = os.path.join(self.config_dir, src)
            logger.debug('considering default config %s', default)
            with open(default) as f:
                default_lines = f.readlines()

            logger.debug('loaded default config with %d lines', len(default_lines))

            output_lines = []
            matched = set()
            for default_line in default_lines:
                for name, (target, value) in self.injectables.items():
                    if target != src:
                        continue

                    if self.service.match_line(default_line, name):
                        logger.debug('found matching line %r for %s', default_line, name)
                        logger.debug('injecting (name: %s, value: %s) into %s', name, value, target)
                        new_line = self.service.inject_line(default_line, name, value)
                        matched.add(name)
                        note = self.service.comment_line('Injected by env2config, replacing default: ' + default_line.strip())
                        output_lines.append(note)
                        output_lines.append(new_line)
                        break
                else:
                    output_lines.append(default_line)

            for name, (target, value) in self.injectables.items():
                if target != src:
                    continue
                    
                if name not in matched:
                    logger.debug('injecting (name: %s, value: %s) to the end of %s', name, value, target)
                    warning = self.service.comment_line('Injected by env2config, not matching any default.')
                    output_lines.append(warning)
                    line = self.service.inject_line(None, name, value)
                    output_lines.append(line)

            # Write out the new, overridden configs.  If the destination is '-',
            # write the configs to stdout instead (useful for debugging).
            # Is there a way to avoid this code deduplication?

            if dest == '-':
                f = sys.stdout
                for line in output_lines:
                    f.write(line)
            else:
                with open(dest, 'w') as f:
                    for line in output_lines:
                        f.write(line)

