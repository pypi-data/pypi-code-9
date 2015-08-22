#!/usr/local/bin/python
import sys
from .cli import parse_args
from .eclipse import write_metadata_files
from .git import GitCloneError, Repository


def main():
    args = parse_args()
    repo = Repository(args.remote_url)
    try:
        repo.clone(outdir=args.destination)
    except GitCloneError:
        sys.exit(1)
    write_metadata_files(args.destination, repo.name)

if __name__ == "__main__":
    main()