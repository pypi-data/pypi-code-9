#!/usr/bin/env python

from docker.client import Client
from docker.utils import kwargs_from_env


def main():
  client = Client(**kwargs_from_env())
  print client.version()


if __name__ == '__main__':
  main()
