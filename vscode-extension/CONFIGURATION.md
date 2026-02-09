# FigmaFlow VS Code Extension - Configuration Guide

## Quick Start

### 1. Configure API Keys

Edit `/path/to/FigmaFlow-MCP/mcp-server/.env`:

```bash
# Figma Access Token
FIGMA_ACCESS_TOKEN=your_figma_token_here

# AI Configuration (LiteLLM)
AI_BASE_URL=https://litellm.tarento.dev
AI_API_KEY=your_litellm_api_key
AI_MODEL=gemini-pro

# Optional: Model Parameters
AI_TEMPERATURE=0.3
AI_MAX_TOKENS=2000
```

### 2. Open Your Flutter Project in VS Code

### 3. Use the Extension

- **Generate Widget**: `Cmd/Ctrl + Shift + P` → `Figma: Generate Widget`
- **Generate Tests**: `Cmd/Ctrl + Shift + P` → `Figma: Generate Tests`

## Configuration Location

The extension reads from a **single centralized `.env` file**:

```
/path/to/FigmaFlow-MCP/mcp-server/.env
```

This is the SAME `.env` used for standalone testing.

## Supported AI Providers

Thanks to LiteLLM integration, you can use any AI model:

### OpenAI Models
```bash
AI_MODEL=gpt-5
AI_MODEL=gpt-4o
AI_MODEL=gpt-3.5-turbo
```

### Google Models
```bash
AI_MODEL=gemini-pro
AI_MODEL=gemini-1.5-flash
```

### Anthropic Models
```bash
AI_MODEL=claude-3-5-sonnet
AI_MODEL=claude-3-haiku
```

### Local Models (Ollama)
```bash
AI_BASE_URL=http://localhost:11434/v1
AI_MODEL=llama3
```

## How It Works

```
VS Code Extension
    ↓
Loads mcp-server/.env
    ↓
Passes credentials to MCP Server as parameters
    ↓
MCP Server uses provided keys
    ↓
Returns generated code
```

## Features

✅ **Token Filtering** - Saves 52-71% on API costs  
✅ **LLM Agnostic** - Use any AI model  
✅ **Rate Limiting** - Automatic retry with exponential backoff  
✅ **Caching** - Reduces redundant Figma API calls  
✅ **No Setup Wizard** - Just edit one `.env` file  

## Troubleshooting

### "Configuration not found"
- Make sure `mcp-server/.env` exists
- Copy from `.env.example` if needed
- Click "Open .env" to edit directly

### "FIGMA_ACCESS_TOKEN not found"
- Get token from: https://www.figma.com/settings
- Add to `mcp-server/.env`

### "AI_API_KEY not found"
- Set `AI_API_KEY` in mcp-server/.env

## Migration from Old Version

If you were using the setup wizard:

**Old way:**
- Run setup wizard for each workspace
- Keys stored in workspace `.env`

**New way:**
- Edit `mcp-server/.env` once
- All workspaces use same config

## Example Configuration

```bash
# Complete example mcp-server/.env

# Figma
FIGMA_ACCESS_TOKEN=figd_abc123xyz

# LiteLLM
AI_BASE_URL=https://litellm.tarento.dev
AI_API_KEY=your_litellm_key
AI_MODEL=gemini-pro
AI_TEMPERATURE=0.3
AI_MAX_TOKENS=2000

# Optional: Server settings
MCP_SERVER_PORT=3000
LOG_LEVEL=INFO
```

## Advanced: Switching Models

Change AI model anytime by editing `.env`:

```bash
# Use GPT-5
AI_MODEL=gpt-5

# Use Claude
AI_MODEL=claude-3-5-sonnet

# Use local Llama
AI_BASE_URL=http://localhost:11434/v1
AI_MODEL=llama3
```

No need to restart VS Code - changes take effect immediately!

## Documentation

- [LiteLLM Setup Guide](../mcp-server/LITELLM_SETUP.md)
- [AI Model Guide](../mcp-server/AI_MODEL_GUIDE.md)
- [API Key Flow](../API_KEY_FLOW.md)
