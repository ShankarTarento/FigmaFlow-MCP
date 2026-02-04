# FigmaFlow-MCP Setup Guide

Complete guide to set up and run FigmaFlow-MCP locally.

## Prerequisites

✅ Already installed:
- Python 3.10+ 
- Node.js 18+
- Poetry (Python package manager)
- npm (Node package manager)

You'll also need:
- Figma account with API access
- OpenAI account with API access
- Flutter SDK (optional, for testing generated code)

## Step 1: Get API Keys

### Figma Access Token

1. Go to [Figma Account Settings](https://www.figma.com/settings)
2. Scroll to **Personal Access Tokens** section
3. Click **Generate new token**
4. Give it a name (e.g., "FigmaFlow MCP")
5. Copy the token (starts with `figd_`)

### OpenAI API Key

1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Click **Create new secret key**
3. Give it a name (e.g., "FigmaFlow")
4. Copy the key (starts with `sk-`)

## Step 2: Configure MCP Server

```bash
cd mcp-server

# Copy environment template
cp .env.example .env

# Edit .env and add your keys
nano .env  # or use your preferred editor
```

Your `.env` file should look like:
```bash
FIGMA_ACCESS_TOKEN=figd_your_actual_token_here
OPENAI_API_KEY=sk-your_actual_key_here
MCP_SERVER_PORT=3000
LOG_LEVEL=INFO
AI_MODEL=gpt-4o
AI_TEMPERATURE=0.3
AI_MAX_TOKENS=2000
```

## Step 3: Test MCP Server

```bash
# Make sure you're in mcp-server directory
cd mcp-server

# Run the server
poetry run python src/mcp/server.py
```

The server should start without errors. Press `Ctrl+C` to stop it.

## Step 4: Install VS Code Extension (Dev Mode)

```bash
cd ../vscode-extension

# Dependencies already installed
# Open VS Code in this directory
code .
```

In VS Code:
1. Press `F5` to launch Extension Development Host
2. A new VS Code window will open with the extension loaded

## Step 5: Test the Complete Workflow

In the Extension Development Host window:

1. **Open a Flutter project** (or create a test directory)

2. **Run setup wizard:**
   - Press `Cmd+Shift+P` (or `Ctrl+Shift+P`)
   - Type: `FigmaFlow: Setup API Keys`
   - Enter your Figma token
   - Enter your OpenAI key

3. **Generate a widget:**
   - Press `Cmd+Shift+P`
   - Type: `FigmaFlow: Generate Flutter Widget from Figma`
   - Enter a Figma URL (see test URLs below)
   - Enter widget name (e.g., `TestButton`)
   - Wait for generation...

## Test Figma URLs

You can use these public Figma files for testing:

### Simple Button
```
https://www.figma.com/file/ABC123/Button
```
(Replace with your own Figma file URL)

### To create a test design:
1. Go to [Figma](https://www.figma.com)
2. Create a new design file
3. Add a simple frame with:
   - Rectangle (background)
   - Text (label)
   - Maybe an icon
4. Copy the file URL
5. Optionally, select a specific frame and copy the node-id from URL

## Troubleshooting

### Issue: "MCP server failed to start"
**Solution:** 
- Make sure you're in the right directory
- Check that Python 3.10+ is installed: `python3 --version`
- Check poetry virtual environment: `poetry env info`

### Issue: "Cannot find module 'vscode'"
**Solution:**
- Run `npm install` in vscode-extension directory
- Restart VS Code
- Try F5 again

### Issue: "FIGMA_ACCESS_TOKEN not found"
**Solution:**
- Make sure .env file exists in workspace root
- Run the setup wizard: `FigmaFlow: Setup API Keys`
- Check that .env has correct format (no quotes around values)

### Issue: "OpenAI API error"
**Solution:**
- Verify your OpenAI key is valid
- Check you have enough credits: https://platform.openai.com/usage
- Try a different model in .env: `AI_MODEL=gpt-4`

### Issue: "Invalid Figma URL"
**Solution:**
- Make sure URL contains `/file/` in it
- URL should look like: `https://www.figma.com/file/ABC123/Name`
- If selecting specific node, URL should have `?node-id=1-2`

## Running Tests

### Python Tests (MCP Server)
```bash
cd mcp-server
poetry run pytest
```

### TypeScript Tests (VS Code Extension)
```bash
cd vscode-extension
npm test
```

## Next Steps

Once everything is working:
1. Try generating widgets from your own Figma designs
2. Test generated code in a real Flutter project
3. Experiment with different Figma layouts
4. Provide feedback on generated code quality

## Development Workflow

When developing:

**Terminal 1 - MCP Server:**
```bash
cd mcp-server
poetry run python src/mcp/server.py
```

**Terminal 2 - VS Code Extension:**
```bash
cd vscode-extension
npm run watch  # Auto-recompile on changes
# Then press F5 in VS Code
```

## Project Structure

```
FigmaFlow-MCP/
├── mcp-server/          # Python MCP server
│   ├── src/             # Source code
│   ├── tests/           # Tests
│   └── .env            # Your API keys (gitignored)
│
└── vscode-extension/    # TypeScript extension
    ├── src/             # Source code
    ├── out/             # Compiled JS
    └── package.json     # Dependencies

# Workspace .env created by setup wizard
.env                     # Your API keys (gitignored)
```

## Support

- 📖 [Development Plan](plan/development_plan.md)
- 📋 [PRD](plan/prd.txt)
- 🐛 Report issues on GitHub
- 💬 Check existing documentation in README files

---

Happy coding! 🚀
