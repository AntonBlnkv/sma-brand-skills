#!/bin/sh
# Install the sma-max-photo skill as a plain skill folder (no plugin system needed).
#
#   ./install.sh                 Claude Code + Codex, personal (all your projects)
#   ./install.sh claude          Claude Code only  -> ~/.claude/skills/sma-max-photo
#   ./install.sh codex           Codex only        -> ~/.agents/skills/sma-max-photo
#   ./install.sh project DIR     one project       -> DIR/.claude/skills and DIR/.agents/skills
#
# An existing copy is moved aside to sma-max-photo.bak-<timestamp>, never deleted.
# Then: pip install -r <installed folder>/scripts/requirements.txt
set -eu
HERE=$(cd "$(dirname "$0")" && pwd)
SRC="$HERE/plugins/sma-max-photo/skills/sma-max-photo"
[ -f "$SRC/SKILL.md" ] || { echo "SKILL.md not found in $SRC" >&2; exit 1; }

put() {  # put <skills dir>
  mkdir -p "$1"
  dest="$1/sma-max-photo"
  if [ -e "$dest" ]; then
    bak="$dest.bak-$(date +%Y%m%d-%H%M%S)"
    mv "$dest" "$bak"
    echo "moved old copy to $bak"
  fi
  cp -R "$SRC" "$dest"
  echo "installed: $dest"
}

case "${1:-both}" in
  claude)  put "$HOME/.claude/skills" ;;
  codex)   put "$HOME/.agents/skills" ;;
  both)    put "$HOME/.claude/skills"; put "$HOME/.agents/skills" ;;
  project) [ -n "${2:-}" ] || { echo "usage: ./install.sh project DIR" >&2; exit 1; }
           put "$2/.claude/skills"; put "$2/.agents/skills" ;;
  *)       sed -n '2,10p' "$0"; exit 1 ;;
esac
echo "Restart Claude Code / Codex so the skill is picked up."
