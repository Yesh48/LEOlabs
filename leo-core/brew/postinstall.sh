#!/bin/bash
set -e

CONFIG_DIR="$HOME/.leo"
CONFIG_FILE="$CONFIG_DIR/config"

mkdir -p "$CONFIG_DIR"

if [ ! -f "$CONFIG_FILE" ]; then
  echo "🔧 Setting up LEO Core configuration..."
  read -p "Enter your OpenAI API key (or leave blank for offline mode): " KEY
  echo "OPENAI_API_KEY=$KEY" > "$CONFIG_FILE"
  echo "✅ Configuration saved to $CONFIG_FILE"
else
  echo "ℹ️ Existing configuration found at $CONFIG_FILE"
fi

echo ""
echo "🎉 LEO Core installation complete!"
echo "You can now run audits like:"
echo "  leo audit https://openai.com"
