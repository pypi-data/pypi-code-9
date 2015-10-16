#! /usr/bin/env python3

import os
import sys
import configparser
import subprocess

import jinja2

from qudb import models
from qudb import commands

try:
    import yaml
except ImportError:
    yaml = None


class UnreadableFile(Exception):
    pass


class QuestionFileMissing(Exception):
    pass


class InvalidYAMLSchema(Exception):
    pass


class UnknownEntity(Exception):
    pass


def check_readable_file(file, path='.'):
    fullpath = os.path.join(path, file)
    if not (os.path.isfile(fullpath) and os.access(fullpath, os.R_OK)):
        raise UnreadableFile


def preprocess_question(question, path):
    check_readable_file(question, path)
    question = os.path.normpath(question)

    # extract info
    mcq = '{0}mcq{0}'.format(os.sep) in question
    # TODO: chapter
    return mcq


def do_list(session, what, term=None, atype=None, question=None, mcq=None):
    # TODO: show more data when possible, e.g. assessment-questions
    if what == 'questions':
        # TODO: filter by chapter
        if term is not None:
            question_model = models.AssessmentQuestion
        else:
            question_model = models.Question
        result = question_model.filter(
                session, term, atype, question, mcq)
    elif what == 'assessments':
        result = models.Assessment.filter(session, term, atype, question)
    elif what == 'assessment-types':
        result = models.AssessmentType.filter(session, term, question)
    elif what == 'terms':
        result = models.Term.filter(session, atype)
    else:
        raise UnknownEntity
    return result.all()


def do_add(session, term, atype, question, questions_directory='.',
           bonus=False, points=None, order=None, date=None, commit=True):
    mcq = preprocess_question(question, questions_directory)
    models.Assessment.add_question(session, term, atype, question,
                                   mcq, bonus, points, order, date, commit)


def do_update(session, term, atype, question=None, questions_directory='.',
              bonus=False, points=None, order=None, date=None):
    if question is None:
        models.Assessment.update_assessment(session, term, atype,
                                            date)
    else:
        mcq = preprocess_question(question, questions_directory)
        models.Assessment.update_question(session, term, atype,
            question, mcq, bonus, points, order, date)


def do_remove(session, term, atype, question):
    models.Assessment.remove_question(session, term, atype, question)


def parse_config_file(config_file):
    default = 'qudb.conf'
    if not config_file and os.path.exists(default):
        config_file = default
    else:
        return {}
    config = configparser.ConfigParser()
    check_readable_file(config_file)
    config.read(config_file)
    return dict(config['templates'])


def _atype_to_title(atype):
    if atype == 'final':
        return 'Final Exam'
    title = atype[:-1].title() + ' ' + atype[-1:]
    if title.startswith('Major'):
        title = 'Major Exam' + title[5:]
    return title


def do_render(session, term, atype, template, solution, questions_directory,
              out_dir, material, config):
    a = models.Assessment.get(session, term, atype)

    values = parse_config_file(config)
    values['term'] = term
    values['title'] = _atype_to_title(atype)
    values['solution'] = solution
    values['material'] = material
    values['date'] = a.date.strftime('{%d}{%m}{%Y}')
    values['qs'] = a.aqs
    values['mcqs'] = a.amcqs
    values['questions_relpath'] = os.path.relpath(questions_directory, out_dir)
    values['questions_directory'] = questions_directory

    loader = jinja2.FileSystemLoader(os.getcwd())
    env = jinja2.Environment(
        block_start_string='<%'   , block_end_string='%>',
        variable_start_string='<<', variable_end_string='>>',
        comment_start_string='<#' , comment_end_string='#>',
        loader=loader)
    template = env.get_template(template)
    # TODO: warn when there are undefined template variables
    return template.render(values)


def create_db(db='qu.db'):
    return models.init(db)


def connect(db='qu.db'):
    '''connect to an existing db only, unless it's in-memory'''
    if db is not None:  # None creates an in-memory db
        check_readable_file(db)
    return models.init(db)


def pdflatex(filenames, outdir):
    for filename in filenames:
        print('Running pdflatex', filename, end=' ', flush=True)
        for i in range(4):
            subprocess.call(['pdflatex', '-interaction', 'batchmode', os.path.basename(filename)],
                            cwd=outdir, stdout=subprocess.DEVNULL)
            print('.', end='', flush=True)
        for ext in ['.aux', '.log', '.out']:
            os.remove(os.path.splitext(filename)[0] + ext)
        print()


def do_import(session, yml_doc, update=False, questions_directory='.'):
    '''
    Raises:
      yaml.YAMLError: if a mal-formed YAML file is imported
      QuestionFileMissing: if a question is missing the file key
      models.AssessmentDateExists, models.AssessmentQuestionExists:
        if imported data includes data already present in the database
      InvalidYAMLSchema: if the YAML data is not in the expected format
    '''
    doc = yaml.safe_load(yml_doc)
    try:
        for term, atypes in doc.items():
            for atype, questions in atypes.items():
                for q in questions:
                    do_add(session, term, atype, q['file'], questions_directory,
                           bonus=q.get('bonus'), points=q.get('points'),
                           date=q.get('date'), commit=False)
    except KeyError:
        session.rollback()
        raise QuestionFileMissing
    except (models.AssessmentDateExists, models.AssessmentQuestionExists):
        session.rollback()
        raise
    except Exception:
        session.rollback()
        raise InvalidYAMLSchema
    else:
        session.commit()


def do_export(session):
    doc = {}
    for t in models.Term.all(session).all():
        doc[t.code] = {}
        for a in t.assessments:
            doc[t.code][a.type.name] = []
            for q in a.amcqs + a.aqs:
                qdict = {}
                qdict['file'] = q.question.file
                if q.question.chapter:
                    qdict['chapter'] = q.question.chapter
                if q.bonus:
                    qdict['bonus'] = q.bonus
                for attr in ['points', 'student_count', 'avg_score',
                             'max_score', 'min_score']:
                    if getattr(q, attr) is not None:
                        qdict[attr] = getattr(q, attr)
                doc[t.code][a.type.name].append(qdict)
            # add assessment attributes to the first questions
            if a.date is not None:
                doc[t.code][a.type.name][0]['date'] = a.date
    return yaml.dump(doc, default_flow_style=False)


###################################################
#                      Main                       #
###################################################

def main(cmd_args=None):
    cmd_args = cmd_args or sys.argv[1:]
    args = commands.parse_command(cmd_args)
    if args.cmd is None:
        return

    if args.cmd == 'init':
        create_db(args.database)
    else:
        try:
            session = connect(args.database)
        except UnreadableFile:
            print('Error: database file \'{}\' is unreadable.'.format(args.database))
            print('\nYou may want to do one of the following:')
            print(' 1. Use the -D (or --database) option to specify the path of an existing database')
            print('    By default, qm looks for ./qu.db')
            print(' 2. Use the \'init\' command, optionally with the -D option, to create a new database')
            print(' 3. Make sure the database file is readable, e.g. you have sufficient privileges')
            return

    if args.cmd in ['import', 'export'] and yaml is None:
        print('Error: PyYAML not found. Install PyYAML for import/export support')
        return

    if args.cmd == 'list':
        try:
            result = do_list(session, args.what, args.term,
                             args.assessment_type, args.question, args.mcq)
        except models.AssessmentDoesNotExist:
            print('Error: Assessment does not exist')
        except UnknownEntity:
            print('Error: Trying to list an unknown entity: {}', args.what)
        else:
            print('Listing {} ({} found):'.format(
                args.what.replace('-', ' '), len(result)))
            for i in result:
                print('- {}'.format(i))

    elif args.cmd == 'add':
        try:
            do_add(session, args.term, args.assessment_type, args.question,
                   args.questions_directory, args.bonus, args.points,
                   args.order, args.date)
        except models.AssessmentQuestionExists:
            print('Error: This question already exists in the specified assessment. '
                  'Cannot add. Try update!')
            print('    >> {}-{}: {}'.format(
                args.term, args.assessment_type, args.question))
        except models.AssessmentDateExists:
            print('Error: This assessment already has a date')

    elif args.cmd == 'update':
        try:
            do_update(session, args.term, args.assessment_type, args.question,
                      args.questions_directory, args.bonus, args.points,
                      args.order, args.date)
        except models.AssessmentQuestionDoesNotExist:
            print('Error: This question does not exist in the specified assessment. '
                  'Cannot update. Try add!')

    elif args.cmd == 'render':
        base_filename = os.path.join(args.output_directory,
            '{}-{}'.format(args.term, args.assessment_type))
        filenames = [
            base_filename + '.tex',
            base_filename + '-solution.tex'
        ]
        for filename, solution in zip(filenames, (False, True)):
            try:
                print('Rendering {}..'.format(filename))
                output = do_render(session, args.term,
                    args.assessment_type, args.template, solution=solution,
                    questions_directory=args.questions_directory,
                    out_dir=args.output_directory, material=args.material,
                    config=args.config)
            except UnreadableFile:
                print('Error: Configuration file \'{}\' is unreadable'.format(args.config))
                return
            except models.AssessmentDoesNotExist:
                print('Error: Assessment does not exist')
                return
            except jinja2.exceptions.TemplateNotFound as e:
                raise
                print('Error: Template file \'{}\' not found'.format(args.template))
                return
            else:
                os.makedirs(args.output_directory, exist_ok=True)
                with open(filename, 'w') as outfile:
                    outfile.write(output)

        if args.pdflatex:
            pdflatex(filenames, args.output_directory)

    elif args.cmd == 'import':
        try:
            check_readable_file(args.file)
            with open(args.file, 'r') as ymlfile:
                yml_doc = ymlfile.read()
            do_import(session, yml_doc, args.update, args.questions_directory)
        except UnreadableFile:
            print('Error: YAML file not found or unreadable')
            return
        except yaml.YAMLError as exc:
            print('Error: YAML syntax error', end='')
            if hasattr(exc, 'problem_mark'):
                mark = exc.problem_mark
                print(' at line {}, column {}'.format(mark.line+1, mark.column+1))
            else:
                print()
            return
        except QuestionFileMissing:
            print('Error: found a question without a file while importing')
            return
        except (models.AssessmentDateExists, models.AssessmentQuestionExists):
            print('Error: importing data that already exists. '
                  'Consider using --update to update the existing data')
            return
        except InvalidYAMLSchema:
            print('Error: YAML data is not in the expected format')
            return

    elif args.cmd == 'export':
        if os.path.exists(args.file) and not args.overwrite:
            print('Error: export file exists. Use --overwrite to overwrite it')
            return
        with open(args.file, 'w') as ymlfile:
            ymlfile.write(do_export(session))


if __name__ == '__main__':
    main()
