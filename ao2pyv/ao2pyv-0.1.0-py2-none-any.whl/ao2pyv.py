""" Converts Archive.org video searches into PyVideo.org API submissions.
"""

import json

import requests
import click


class Processor(object):
    """ Processor in a pipeline. """
    def __init__(self, f):
        self.f = f


class Source(Processor):
    """ Processor that takes no arguments and returns a list of videos. """
    def __call__(self):
        return self.f()


class Sink(Processor):
    """ Processor that takes a list of videos and returns nothing. """
    def __call__(self, videos):
        self.f(videos)


class Transform(Processor):
    """ Processor that takes a list of videos and returns a modified list . """
    def __call__(self, videos):
        return self.f(videos)


@click.group(chain=True, invoke_without_command=True)
@click.version_option()
@click.option('--query', '-q', help='Archive.org search query')
@click.option('--category', '-c', help="Pyvideo category")
@click.option('--language', '-l', help="Pyvideo language")
def cli(*args, **kw):
    pass


@cli.resultcallback()
@click.pass_context
def process_pipeline(ctx, processors, query, category, language):
    if not processors and query is None:
        click.echo(ctx.get_help())
        ctx.exit(1)

    sources = [p for p in processors if isinstance(p, Source)]
    if not sources:
        sources.append(ctx.invoke(source_archive_dot_org, query=query))
    if len(sources) != 1:
        raise click.UsageError("Only one source may be specified.")

    transforms = [p for p in processors if isinstance(p, Transform)]
    if not transforms:
        transforms.append(ctx.invoke(
            transform_ao2pyv, category=category, language=language))

    sinks = [p for p in processors if isinstance(p, Sink)]
    if not sinks:
        sinks.append(ctx.invoke(
            sink_json, output=click.utils.LazyFile('-', mode='wb'),
            final_newline=True))
    if len(sinks) != 1:
        raise click.UsageError("Only one sink may be specified.")

    [source] = sources
    [sink] = sinks

    videos = source()
    for t in transforms:
        videos = t(videos)
    sink(videos)


#########
# Sources

@cli.command('source.archive-org')
@click.option('--query', '-q', help='Archive.org search query')
@click.option('--api-url', default='https://archive.org/advancedsearch.php')
def source_archive_dot_org(query, api_url):
    """ Search archive.org for a query and return a list of results.

    See https://archive.org/help/json.php for information on the API.
    """
    def search():
        r = requests.get(api_url, params={
            "q": query,
            "output": "json",
        })
        j = r.json()
        return j["response"]["docs"]
    return Source(search)


@cli.command('source.json')
@click.option('--input', '-f', type=click.File('rb', lazy=True))
def source_json_file(input):
    """ Return results from a JSON file.
    """
    def read_json():
        with input:
            return json.loads(input.read())
    return Source(read_json)


############
# Transforms

@cli.command('transform.none')
def transform_none():
    """ Transform a video result not at all.
    """
    return Transform(lambda videos: videos)


@cli.command('transform.ao2pyv')
@click.option('--category', '-c', help="Pyvideo category")
@click.option('--draft', 'state', flag_value=2, default=True)
@click.option('--live', 'state', flag_value=1)
@click.option('--language', '-l', help="Pyvideo language")
@click.option('--base-url', default='https://archive.org/details/')
def transform_ao2pyv(category, state, language, base_url):
    """ Transform a video result from archive.org to pyvideo.org format.

    See http://richard.readthedocs.org/en/latest/admin/api.html#videos for
    a description of the pyvideo.org format.
    """
    if category is None:
        raise click.UsageError("Please specify a category.")

    def ao2pyv(videos):
        # TODO: truncate description to first paragraph
        return [{
            "category": category,
            "title": video["title"],
            "language": language or video["language"][0],
            "state": state,
            "speakers": video["creator"],
            "tags": video["subject"],
            "summary": video["description"],
            "description": video["description"],
            "source_url": base_url + video["identifier"],
        } for video in videos]
    return Transform(ao2pyv)


#######
# Sinks

@cli.command('sink.json')
@click.option('--output', '-f', type=click.File('wb', lazy=True))
@click.option('--indent', default=2)
@click.option('--final-newline', default=False)
def sink_json(output, indent, final_newline):
    """ Output results to a file.
    """
    def write_json(videos):
        with output:
            output.write(json.dumps(videos, indent=indent))
            if final_newline:
                output.write("\n")
    return Sink(write_json)


if __name__ == "__main__":
    cli()
