"""Quick start command line Q&A"""
from hitchquickstart.utils import log, warn, signals_trigger_exit
from click import command, group, argument, option, prompt
from jinja2 import FileSystemLoader, exceptions
from jinja2.environment import Environment
from sys import exit, executable
from os import path, walk, chdir
import yaml
import click


TEMPLATE_DIR = path.join(path.dirname(path.realpath(__file__)), "templates")


QUESTIONS_FILE = path.join(path.dirname(path.realpath(__file__)), "questions.yml")


TEMPLATES = [
    "all.settings",
    "hitchreqs.txt",
    "engine.py",
    "system.packages",
    "README.rst",
    "ci.settings",
    "tdd.settings",
    "stub.test",
]


@command()
def cli():
    """Runs quickstart."""

    # You didn't already initialize did you?
    for template in TEMPLATES:
        if path.exists(template):
            warn((
                "HitchQuickstart generates the following files: {}\n"
                "{} already exists. Delete everything and try again.\n"
            ).format(", ".join(TEMPLATES), template))
            exit(1)

    # Get questions
    with open(QUESTIONS_FILE, 'r') as questions_file_handle:
        questions = yaml.load(questions_file_handle.read())

    # Ask questions and get answers
    answers = {}

    for question_fulldict in questions:
        question_id = list(question_fulldict.keys())[0]
        question = list(question_fulldict.values())[0]

        answer = prompt(
            question['text'],
            default=question['default'],
            type=click.__dict__[question['type']],
        )

        if answer != False:
            answers[question_id] = answer

            for dependency in question.get('dependencies', []):
                answers[dependency] = True

            for subquestion_fulldict in question.get('subquestions', []):
                subquestion_id = list(subquestion_fulldict.keys())[0]
                subquestion = list(subquestion_fulldict.values())[0]

                subquestion_answer = prompt(
                    subquestion['text'],
                    default=subquestion['default'],
                    type=click.__dict__[subquestion['type']],
                )

                if subquestion_answer:
                    answers[subquestion_id] = subquestion_answer

                    for dependency in subquestion.get('dependencies', []):
                        answers[dependency] = True

    # Load templating environment
    env = Environment(trim_blocks=True)
    env.loader = FileSystemLoader(TEMPLATE_DIR)

    # Output files
    for template_name in TEMPLATES:
        try:
            with open(template_name, "w") as file_handle:
                file_handle.write(
                    env.get_template(template_name + ".jinja2").render(**answers)
                )
        except Exception as e:
            import IPython ; IPython.embed()
            exit(1)

def run():
    """Run hitch tests"""
    signals_trigger_exit()
    cli()

if __name__ == '__main__':
    run()
