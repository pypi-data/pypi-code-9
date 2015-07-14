from spex.bin.args import create_parser


def a(arg_str, defaulted=('test.spex', )):
    args = arg_str.split()
    if defaulted:
        args += defaulted
    return args


def test_requirements():
    parser = create_parser()
    args = parser.parse_args(a('-r requirements.txt'))
    assert args.requirement_files == ['requirements.txt']

    args = parser.parse_args(a('--requirement requirements2.txt'))
    assert args.requirement_files == ['requirements2.txt']

    args = parser.parse_args(a('-r r1.txt -r r2.txt'))
    assert args.requirement_files == ['r1.txt', 'r2.txt']

    args = parser.parse_args(a('--requirement r1.txt -r r2.txt'))
    assert args.requirement_files == ['r1.txt', 'r2.txt']


def test_verbosity():
    parser = create_parser()
    args = parser.parse_args(a(''))
    assert args.verbosity == 0

    args = parser.parse_args(a('-v'))
    assert args.verbosity == 1

    args = parser.parse_args(a('-v -v'))
    assert args.verbosity == 2

    args = parser.parse_args(a('-vv'))
    assert args.verbosity == 2

    args = parser.parse_args(a('-vvv'))
    assert args.verbosity == 3


def test_use_wheels():
    parser = create_parser()
    args = parser.parse_args(a('--wheel'))
    assert args.use_wheel

    args = parser.parse_args(a('--no-wheel'))
    assert not args.use_wheel

    args = parser.parse_args(a('--no-use-wheel'))
    assert not args.use_wheel


def test_no_pypi():
    parser = create_parser()
    args = parser.parse_args(a('--pypi'))
    assert args.use_pypi

    args = parser.parse_args(a('--no-pypi'))
    assert not args.use_pypi


def test_indicies():
    parser = create_parser()
    args = parser.parse_args(a('-i xyz'))
    assert args.indicies == ['xyz']

    args = parser.parse_args(a('-i xyz --index abc'))
    assert args.indicies == ['xyz', 'abc']

    args = parser.parse_args(a('-i xyz --index abc --index-url ghf'))
    assert args.indicies == ['xyz', 'abc', 'ghf']


def test_repos():
    parser = create_parser()
    args = parser.parse_args(a('-f 123'))
    assert args.repos == ['123']

    args = parser.parse_args(a('-f 123 --find-links 456'))
    assert args.repos == ['123', '456']

    args = parser.parse_args(a('-f 123 --find-links 456 --repo 678'))
    assert args.repos == ['123', '456', '678']


def test_reqs():
    parser = create_parser()
    args = parser.parse_args(a(''))
    assert args.reqs == []

    args = parser.parse_args(['test.spex', 'flask', 'tornado'])
    assert args.reqs == ['flask', 'tornado']


def test_name():
    parser = create_parser()
    args = parser.parse_args(['test.spex'])
    assert args.spex_name == 'test.spex'
