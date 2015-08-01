INIT_FILE = """COMPLETION_DIR="$HOME/.ohh/zsh/completions"
fpath+=$COMPLETION_DIR
compinit
"""

COMPLETION_FILE = """#compdef ohh
#autoload

local -a _1st_arguments

_1st_arguments=(
  'login:Login to the server'
  'start:Start a working session'
  'stop:Stop a working session'
  'status:Check the current status'
)

local expl

_arguments \
  '(--version)'--version'[show version]' \
  '(--help)'--help'[show help]' \
  '*:: :->subcmds' && return 0

if (( CURRENT == 1 )); then
  _describe -t commands "ohh subcommand" _1st_arguments
  return
fi

case $words[1] in
  start)
    _arguments \
      '(--help)'--help'[show help]' \
      '(--foreground)'--foreground'[run in the foreground]'
    ;;
esac
"""

INIT_CONTENT = """
# added by ohh setup
[[ -f $HOME/.ohh/zsh/ohh-init.sh ]] && . $HOME/.ohh/zsh/ohh-init.sh
"""
