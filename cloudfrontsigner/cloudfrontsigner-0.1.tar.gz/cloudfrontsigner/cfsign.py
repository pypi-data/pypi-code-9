#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import argparse
from . import CannedPolicySigner


def main():
    parser = argparse.ArgumentParser(
        description='Generate AWS CloudFront\'s Signed URLs',
    )
    parser.add_argument('key_pair_id')
    parser.add_argument('secret_key_path')
    parser.add_argument('expire_seconds', type=int)
    parser.add_argument('url')
    args = parser.parse_args()
    signer = CannedPolicySigner(
        key_pair_id=args.key_pair_id,
        key_path=args.secret_key_path,
        expire_seconds=args.expire_seconds,
    )
    signed = signer.sign(args.url)
    print(signed)


if __name__ == '__main__':
    main()
