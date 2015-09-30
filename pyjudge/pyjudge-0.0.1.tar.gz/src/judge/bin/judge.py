'''
Created on 29/09/2015

@author: chips
'''
import os
import argparse
from collections import namedtuple
from judge import runners

Grade = namedtuple('Grade', ['value', 'message'])


def parser():
    '''Returns the parser object for script.'''

    parser = argparse.ArgumentParser(
        description='Automatically grade the input file')
    parser.add_argument('file', help='input file to grade')
    parser.add_argument('--template', '-t',
                        help='grader template file')
    parser.add_argument('--grade', '-g', action='store_true',
                        help=('simply return the final grade without '
                              'showing messages'))
    return parser


def grade_file(src_path, template_path):
    '''Return a Grade object corresponding to the given grading job'''

    with open(template_path) as F:
        template = F.read()

    with open(src_path) as F:
        src = F.read()
        src_ext = os.path.splitext(src_path)[1]

    if src_ext == '.py':
        result = runners.run_template_python(template, src)
        result = result.with_grades(template)
        grade = result.get_grade()
        message = result.get_message(format='text')
        return Grade(grade, message)
    else:
        raise ValueError(
            0,
            'file with extension %s is not supported' %
            src_ext)


def main():
    '''Executes the main script'''

    # Fetch parameters from argparse
    args = parser().parse_args()
    src = args.file
    template = args.template
    grade_only = args.grade
    if template is None:
        template = os.path.splitext(src)[0] + '.io'

    try:
        grade = grade_file(src, template)
    except Exception as ex:
        # Handle errors
        if ex.args[0] == 0:
            print('Error:', ex)
            raise SystemExit
        else:
            value = input('An unknown error was found, '
                          'do you wish to see the traceback? [y/N] ')

            ex = ex if value.lower() in ['y', 'yes'] else SystemExit
            raise ex

    if not grade_only and grade.message:
        print(grade.message)
    if grade.value == 1:
        print('Final grade: 100%, congratulations!')
    else:
        print('Final grade: %s%%' % (grade.value * 100))
