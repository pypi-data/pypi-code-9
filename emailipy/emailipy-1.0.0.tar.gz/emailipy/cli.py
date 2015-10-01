import click
import os
import sys

from linter import lint_css
from inliner import inline_css


@click.command()
@click.argument('css_file', required=True, type=click.File('r'))
def lint(css_file):
    """Lints email css and prints issues per client."""
    css = css_file.read()

    issues = lint_css(css) or []
    for issue in issues:
        click.echo(issue)


@click.command()
@click.option('--allow_invalid_css', '-i', is_flag=True, help="Allows css that doesn't lint.")
@click.option('--remove_classes', '-c', is_flag=True, help="Strip all class attributes after inlining")
@click.argument('html_file', required=True, type=click.File('r'))
@click.argument('css_file', required=True, type=click.File('r'))
def inline(html_file, css_file, allow_invalid_css, remove_classes):
    """Inlines css into html to make it safe for email."""
    files = {}
    for extension, f in [("html", html_file), ("css", css_file)]:
        files[extension] = f.read()

    html = inline_css(*files.values(),
                      strip_unsupported_css=(not allow_invalid_css),
                      remove_classes=remove_classes)
    click.echo(html)
