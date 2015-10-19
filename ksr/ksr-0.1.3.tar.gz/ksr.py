#!/usr/bin/env python3
import click
import sys
import re
from tinydb import TinyDB, where

db = TinyDB('db.json')
projects = db.table('projects')
backings = db.table('backings')

@click.group()
def cli():
  """ksr is a command line tool to manage crowdfunding campaigns"""
  pass

def error(string):
  print("ERROR: " + string)
  sys.exit(1)

def get_project(name):
  return projects.get(where('name') == name) or error("Project %r not found" % name)

@cli.command()
@click.argument('name')
@click.argument('target', type=float)
def project(name, target):
  """Create a new project NAME with goal $TARGET"""
  if projects.search(where('name') == name):
    error("Project %s already exists, please choose a unique name" % name)
  else:
    projects.insert({'name': name, 'target': target})
    print("Added %s project with target of $%s" % (name, smooth(target)) )

def smooth(number):
  """Returns an integer if the float is a whole number"""
  return int(number) if number.is_integer() else number

@cli.command('list')
@click.argument('name', required=False)
def list_project(name):
  """List project NAME's details, or all projects if no name is specified"""
  if name == None:
    all_projects = projects.all()
    if len(all_projects):
      print("Projects:\n-- " + "\n-- ".join([p['name'] for p in all_projects]))
  else:
    project = get_project(name)
    total = 0.0
    for backing in backings.search(where('project')==name):
      amount = smooth(backing['amount'])
      total = total + amount
      print("-- %s backed for $%s" % (backing['person'], amount) )
    if total >= project['target']:
      print("%s is successful!" % name)
    else:
      print("%s needs $%s more dollars to be successful" % (name, smooth(project['target'] - total)))

def validate_name(ctx, param, value):
  """Backer and project names must be alphanumeric + underscore + dash, from 4 to 20 chars"""
  if len(value) > 20:
    raise click.BadParameter("%s must be shorter than 20 characters" % param.human_readable_name)
  if len(value) < 4:
    raise click.BadParameter("%s must be longer than 4 characters" % param.human_readable_name)
  if re.match('^[\w-]+$', value) is None:
    raise click.BadParameter("%s contains non-alphanumeric or -_ characters" % param.human_readable_name)
  return value


@cli.command()
@click.argument('name', callback=validate_name)
def backer(name):
  """List backings for NAME"""
  if backings.contains(where("person")==name):
    for backing in backings.search(where("person")==name):
      print("-- Backed %s for $%s" % ( backing['project'], smooth(backing['amount']) ))

@cli.command('back')
@click.argument('person', callback=validate_name)
@click.argument('project', callback=validate_name)
@click.argument('credit_card', type=click.IntRange(0,9999999999999999999))
@click.argument('amount', type=float)
def back(person, project, credit_card, amount):
  """Have PERSON back PROJECT with CREDIT_CARD for AMOUNT

  If AMOUNT is 0, the backing is removed
  """
  def luhn10(card):
    odd = [ int(x) for x in str(card)[1::2] ]
    even = "".join([ str(2 * int(x)) for x in str(card)[::2] ])
    checksum = sum(odd + [int(x) for x in even])
    return checksum % 10

  if luhn10(credit_card):
    error("This card is invalid")
  if backings.contains( (where('person')!=person) & (where('credit_card')==credit_card)):
    error("That card has already been added by another user!")

  project = get_project(project)
  backing = {
    'person': person,
    'project': project['name'],
    'credit_card': credit_card,
    'amount': amount}

  if backings.contains((where('person')==person) & (where('project')==project['name'])):
    if amount <= 0:
      backings.remove((where('person')==person) & (where('project')==project['name']))
      print("%s is no longer backing %s" % (person, project['name']))
    else:
      backings.update(backing, (where('person')==person) & (where('project')==project['name']))
  else:
    backings.insert(backing)
    print("%s backed project %s for $%s" % (person, project['name'], smooth(amount)) )

if __name__ == "__main__":
    cli()
