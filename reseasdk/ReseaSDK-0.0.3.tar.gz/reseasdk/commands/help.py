
HELP_HEADER = """
Usage: reseasdk command ...

Commands:
  new      -- create a new package directory
  build    -- build an executable
  test     -- build and test an executable
  debug    -- build and test an executable with a debugger
  clean    -- remove files generating in builds
  log      -- print kernel log omitted in tests
  version  -- print the version
""".strip()

def main(args):
    # TODO: get help messages from each commands
    print(HELP_HEADER)

