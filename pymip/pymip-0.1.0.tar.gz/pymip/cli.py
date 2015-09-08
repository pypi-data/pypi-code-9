# -*- coding: utf-8 -*-
import logging

import click

from pymip import __version__
from pymip.log import LEVELS, setup_logging
from pymip.scripts.utils import parse_config
from pymip.utils import start_analysis

logger = logging.getLogger(__name__)


@click.group()
@click.option('-c', '--config', default='~/.clinical/config.yaml',
              type=click.Path(exists=True), help='path to config file')
@click.option('-l', '--log-dir', default='/tmp', type=click.Path(exists=True),
              help='path to log file directory')
@click.option('-v', '--verbose', count=True)
@click.version_option(__version__)
@click.pass_context
def cli(ctx, config, log_dir, verbose):
    """MIP and downstream processing of data at Clinical Genomics."""
    # setup logging handlers
    setup_logging(log_dir, stderr_level=LEVELS.get(verbose))

    # read in config values
    ctx.obj = parse_config(config)

    logger.info("Running v%s", __version__)
    ctx.obj['mongo_db'] = ctx.obj.get('mongo_db', 'scoutProd')
    ctx.obj['mongo_port'] = ctx.obj.get('mongo_port', 27017)
    ctx.obj['mongo_host'] = ctx.obj.get('mongo_host', 'localhost')
    ctx.obj['madeline_exe'] = ctx.obj.get('madeline_exe', '/usr/bin/madeline2')


@cli.command()
@click.argument('family', type=str)
@click.option('-cc', '--clusterconstant', type=click.Path(exists=True))
@click.option('-c', '--config', type=click.Path(exists=True))
@click.option('-g', '--gene-list', type=str)
@click.option('-m', '--mip', type=click.Path(exists=True))
@click.pass_context
def start(ctx, family, clusterconstant, config, gene_list, mip):
    """Start a new MIP analysis for a family."""
    return_code = start_analysis(family, clusterconstant, config,
                                 gene_list=gene_list, mip_path=mip)
