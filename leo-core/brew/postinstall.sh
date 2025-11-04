#!/usr/bin/env bash
set -euo pipefail

CONFIG_DIR="$HOME/.leo"
CONFIG_FILE="$CONFIG_DIR/config"

mkdir -p "$CONFIG_DIR"

echo "💡 Leo Core post-install"

if [ -t 0 ]; then
  read -r -p "Enter OpenAI API key (leave blank to skip): " OPENAI_KEY
  if [ -n "$OPENAI_KEY" ]; then
    cat > "$CONFIG_FILE" <<CONFIG
OPENAI_API_KEY=$OPENAI_KEY
CONFIG
    echo "Saved OpenAI API key to $CONFIG_FILE"
  else
    echo "Skipped storing OpenAI API key."
  fi
else
  echo "Non-interactive session detected; skipping API key prompt."
fi
