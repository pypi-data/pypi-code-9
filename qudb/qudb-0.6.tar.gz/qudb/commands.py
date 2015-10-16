import argparse
import datetime


def valid_date(s):
    try:
        return datetime.datetime.strptime(s, '%Y-%m-%d')
    except ValueError:
        msg = 'Not a valid date: {0}.'.format(s)
        raise argparse.ArgumentTypeError(msg)

#######################################
# Parent parsers (for common arguments)
#######################################

def setup_db_parser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-D', '--database', default='qu.db',
                        help='SQLite database file path')
    return parser


def setup_qpath_parser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-Q', '--questions-directory', default='.',
        help='where to look for questions. Question paths stored in the '
                        'database are relative to this path')
    return parser


def setup_question_parser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('question', help='path to the question file')
    return parser


def setup_term_atype_parser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-t', '--term', required=True,
        help='academic semester (3 digits)')
    parser.add_argument('-y', '--assessment-type', required=True,
        help='examples: major1, assignment2, quiz3')
    return parser


def setup_add_update_parser():
    # add/update-only options
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-b', '--bonus', action='store_true',
        help='this is a bonus question')
    parser.add_argument('-p', '--points', help='default points for question')
    parser.add_argument('-o', '--order', type=int,
        help='the order of the question in this assessment; defaults to last')
    # student_count
    # avg_score
    # max_score
    # min_score
    parser.add_argument('-d', '--date', type=valid_date,
        help='assessment date; format YYYY-MM-DD')
    return parser

#################
# Command parsers
#################

def setup_init_parser(subparsers, parent_parsers):
    help='Create a new database file as specified by the -D option. ' \
         'Defaults to ./qu.db. If the database exists, do nothing'
    init_parser = subparsers.add_parser('init', parents=parent_parsers,
        help=help, description=help)


def setup_list_parser(subparsers, parent_parsers):
    help='List existing entities: terms, assessment-types, assessments, or questions'
    list_parser = subparsers.add_parser('list', parents=parent_parsers,
        help=help, description=help)
    list_parser.add_argument('what',
        choices=('terms','assessment-types','assessments', 'questions'),
        help='what to list')
    list_parser.add_argument('-t', '--term',
        help='academic semester code, e.g. 142')
    list_parser.add_argument('-y', '--assessment-type',
        help='examples: major1, assignment2, quiz3')
    list_parser.add_argument('-q', '--question',
        help='include results related to this question only')
    list_parser.add_argument('-m', '--mcq', action='store_true',
        help='whether to retrieve MCQs or non-MCQs. cannot retrieve both at once')


def setup_add_parser(subparsers, parent_parsers):
    help='Add a question file to a given assessment, ' \
         'specified by a term and an assessment-type (required options)'
    add_parser = subparsers.add_parser('add', parents=parent_parsers,
        help=help, description=help)


def setup_update_parser(subparsers, parent_parsers):
    help='Update an existing assessment or question'
    update_parser = subparsers.add_parser('update', parents=parent_parsers,
        help=help, description=help)


def setup_remove_parser(subparsers, parent_parsers):
    help='Remove a question from an assessment'
    remove_parser = subparsers.add_parser('remove', parents=parent_parsers,
        aliases=['rm'], help=help, description=help)


def setup_render_parser(subparsers, parent_parsers):
    help=r'Generate assessment documents using the specified template. ' \
         'Two documents are generated: TERM-ASSESSMENT_TYPE.tex and ' \
         'TERM-ASSESSMENT_TYPE-solution.tex, with the template variable ' \
         '"solution" set to False and True, respectively. Templates are ' \
         'rendered using the Jinja2 template engine, with the following ' \
         'delimiters: <%% block %%><%% endblock %%>, << variable >>, <# comment #>'
    render_parser = subparsers.add_parser('render', parents=parent_parsers,
        help=help, description=help)
    render_parser.add_argument('template',
                               help='path to the jinja2 template file')
    render_parser.add_argument('-O', '--output-directory', default='output',
        help='the directory in which the rendered files will be saved')
    render_parser.add_argument('-C', '--config', help='ini-style configuration '
        'file defining additional template variables. (Use section [templates])')
    render_parser.add_argument('-P', '--pdflatex', action='store_true',
        help='process rendered file with pdflatex (4 runs)')
    render_parser.add_argument('-l', '--material',
        help='specify the material to which this assessment pertains. '
             'Available to the template in the "material" variable')


def setup_import_parser(subparsers, parent_parsers):
    help='Import data from a YAML file into the database. ' \
         'To learn the YAML schema, export a minimal database, ' \
         'or see the README.md file'
    import_parser = subparsers.add_parser('import', parents=parent_parsers,
        help=help, description=help)
    import_parser.add_argument('file', help='YAML file to import')
    import_parser.add_argument('-u', '--update', action='store_true',
                   help='ignore existing, identical questions')


def setup_export_parser(subparsers, parent_parsers):
    help='Export the database to a YAML file ' \
         '(does not include the contents of question files)'
    export_parser = subparsers.add_parser('export', parents=parent_parsers,
        help=help, description=help)
    export_parser.add_argument('file', help='YAML file to export to')
    export_parser.add_argument('--overwrite', action='store_true',
                               help='overwrite the file if it already exists')

####################
# Create main parser
####################

def parse_command(args_str):
    parser = argparse.ArgumentParser(description='Assemble assessments out of existing questions, e.g. exams, quizzes, assignments')

    # create parent parsers
    db_parser = setup_db_parser()
    qpath_parser = setup_qpath_parser()
    term_atype_parser = setup_term_atype_parser()
    add_update_parser = setup_add_update_parser()
    question_parser = setup_question_parser()

    subparsers = parser.add_subparsers(title='commands', dest='cmd',
        help='For command-specific options, run "qm COMMAND -h"')

    # create command parsers
    setup_init_parser(subparsers, [db_parser])
    setup_list_parser(subparsers, [db_parser, qpath_parser])
    setup_add_parser(subparsers,
        [db_parser, qpath_parser, term_atype_parser, add_update_parser, question_parser])
    setup_update_parser(subparsers,
        [db_parser, qpath_parser, term_atype_parser, add_update_parser, question_parser])
    setup_remove_parser(subparsers, [db_parser, qpath_parser, term_atype_parser])
    # TODO: rename/mv, copy assessment
    setup_render_parser(subparsers, [db_parser, qpath_parser, term_atype_parser])
    setup_import_parser(subparsers, [db_parser, qpath_parser])
    setup_export_parser(subparsers, [db_parser])

    args = parser.parse_args(args=args_str)
    if args.cmd is None:
        parser.print_help()
    return args
