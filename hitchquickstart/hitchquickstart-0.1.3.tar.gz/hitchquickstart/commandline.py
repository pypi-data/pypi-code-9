"""Quick start command line Q&A"""
from hitchquickstart.utils import log, warn, signals_trigger_exit
from click import command, group, argument, option, prompt
from jinja2 import FileSystemLoader, exceptions
from jinja2.environment import Environment
from subprocess import check_call
from sys import exit, executable
from os import path, walk, chdir
import signal
import click
import yaml


TEMPLATE_DIR = path.join(path.dirname(path.realpath(__file__)), "templates")


QUESTIONS_FILE = path.join(path.dirname(path.realpath(__file__)), "questions.yml")


TEMPLATES = [
    "all.settings",
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
    dependencies = []

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
                dependencies.append(dependency)

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
                        dependencies.append(dependency)


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
            exit(1)


    # Install dependencies via hitch install

    # If the user hits ctrl-C during an apt-get, let hitch install deal with it
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    for dependency in dependencies:
        check_call(["hitch", "install", dependency])


def run():
    """Run hitch tests"""
    signals_trigger_exit()
    cli()

if __name__ == '__main__':
    run()
