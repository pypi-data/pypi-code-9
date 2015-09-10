import logging
import os.path

from .base import BaseAction, stack_template_key_name
from ..plan import Plan

logger = logging.getLogger(__name__)


class Action(BaseAction):
    """Dump json templates into a given directory."""
    def _dump_template(self, stack, **kwargs):
        filename = stack_template_key_name(stack.blueprint)
        directory = stack.context.args.output_dir
        full_path = os.path.join(directory, filename)
        logger.info("Dumping stack %s to %s", stack.name, full_path)
        with open(full_path, 'w') as fd:
            fd.write(stack.blueprint.rendered)

    def _generate_plan(self):
        plan = Plan(description="Dump cloudformation templates to files.")
        stacks = self.context.get_stacks_dict()
        for stack_name, stack in stacks.items():
            plan.add(
                stack_name,
                run_func=self._dump_template
            )

    def run(self, outline=False, *args, **kwargs):
        """Kicks off the build/update of the stacks in the stack_definitions.

        This is the main entry point for the Builder.

        """
        plan = self._generate_plan()
        plan.execute()
