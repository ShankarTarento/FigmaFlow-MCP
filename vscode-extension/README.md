# FigmaFlow MCP - VS Code Extension

Generate Flutter widgets and tests from Figma designs using AI, powered by MCP.

## Features

- 🎨 Convert Figma designs to Flutter widgets
- 🧪 Auto-generate widget tests  
- 🔑 Easy configuration with setup wizard
- 🐧 Linux-first, works everywhere
- 🤖 AI-powered code generation
- 🔗 Seamless VS Code integration

## Installation

1. **Install from VS Code Marketplace** (coming soon)
   
   Or install from VSIX:
   ```bash
   code --install-extension figmaflow-mcp-0.1.0.vsix
   ```

2. **Open a Flutter project** in VS Code

3. **Run the setup wizard:**
   - Press `Cmd+Shift+P` (or `Ctrl+Shift+P`)
   - Type: **FigmaFlow: Setup API Keys**
   - Follow the prompts

## Getting API Keys

### Figma Access Token
1. Go to [Figma Settings](https://www.figma.com/settings)
2. Scroll to **Personal Access Tokens**
3. Click **Generate new token**
4. Copy the token (starts with `figd_`)

### OpenAI API Key
1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Click **Create new secret key**
3. Copy the key (starts with `sk-`)

## Quick Start

1. **Configure API keys** (first time only):
   ```
   Cmd+Shift+P → "FigmaFlow: Setup API Keys"
   ```

2. **Generate a widget:**
   ```
   Cmd+Shift+P → "FigmaFlow: Generate Flutter Widget from Figma"
   ```

3. **Enter Figma URL** and widget name

4. **Code appears in your editor!**

## Commands

- `FigmaFlow: Setup API Keys` - Configure your API tokens
- `FigmaFlow: Generate Flutter Widget from Figma` - Generate widget code
- `FigmaFlow: Generate Widget Tests from Figma` - Generate widget tests

## Configuration

Your API keys are stored in `.env` in your workspace root:

```bash
# .env (automatically created by setup wizard)
FIGMA_ACCESS_TOKEN=figd_your_token_here
OPENAI_API_KEY=sk_your_key_here
```

## Development

### Setup

```bash
npm install
```

### Build

```bash
npm run compile
```

### Watch Mode

```bash
npm run watch
```

### Package Extension

```bash
npm install -g @vscode/vsce
vsce package
```

## Requirements

- VS Code 1.85+
- Python 3.10+ (bundled with extension)
- Figma account with API access
- OpenAI account with API access

## Support

For issues and feature requests, visit [GitHub Issues](https://github.com/yourusername/figmaflow-mcp/issues)

## License

MIT
