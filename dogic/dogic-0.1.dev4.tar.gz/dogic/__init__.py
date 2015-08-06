#!/usr/bin/env python
from __future__ import print_function

from docker.client import Client
from docker.utils import kwargs_from_env
import requests
import errno


def main():
  client = Client(**kwargs_from_env())
  try:
    version = client.version()
    print(version)
  except requests.exceptions.ConnectionError as error:
    print(error)
    print(error.errno)


if __name__ == '__main__':
  main()
