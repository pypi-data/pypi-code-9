## -*- coding: utf-8 -*-

import os

_HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(_HERE, 'template')

TEMPLATE_OUTPUT_CELLS_ONLY = 'html_output.tpl'
TEMPLATE_OUTPUT_CELLS_TOGGLE_INPUT_CELLS = 'html_output_toggle_input.tpl'

TEMPLATE_INPUT_CELLS_ONLY = 'html_input.tpl'
TEMPLATE_INPUT_CELLS_TOGGLE_OUTPUT_CELLS = 'html_input_toggle_output.tpl'

TEMPLATE_INPUT_AND_OUTPUT_CELLS = 'html_input_output.tpl'
