import json
import yaml


PROCESS_FIELDS = ['id', 'label', 'description', 'inputs',
                  'outputs', 'requirements', 'hints', 'class']

TOOL_FIELDS = PROCESS_FIELDS + [
    'baseCommand', 'arguments', 'stdin', 'stdout', 'successCodes',
    'temporaryFailCodes', 'permanentFailCode'
]

EXPRESSION_FIELDS = PROCESS_FIELDS + [
    'expression', 'script', 'engine'
]

WORKFLOW_FIELDS = PROCESS_FIELDS + ['steps']


# Tool

def remove_unknown_tool_fields(tool):
    pass


def add_expr_req(tool):
    pass


def move_to_hints(tool):
    pass


def fix_sbg_stuff(tool):
    pass


def require_outputs(tool):
    pass


# WF

def extract_tools_from_workflow(tool):
    pass


def remove_unknown_wf_fields(tool):
    pass


# Common

def remove_id(tool):
    del tool['id']


def write_output(tool, format='yaml'):
    formats = {
        'json': json,
        'yaml': yaml
    }
    fmt = formats.get(format)
    if not fmt:
        raise RuntimeError('Unknown format: %s' % format)
    fmt.dump(tool)


def format_tool(tool, passes):
    if tool['class'] == 'Workflow':
        format_workflow(tool, options)
        return
    pass


def format_workflow(tool, options):
    pass
