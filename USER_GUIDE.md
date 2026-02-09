# FigmaFlow MCP - Complete User Guide

## Quick Start

### 1. Install Dependencies
```bash
cd /home/shankarganeshi/PlayGround/FigmaFlow-MCP/mcp-server
pip install -r pyproject.toml
```

### 2. Configure API Keys

Edit `mcp-server/.env`:
```bash
# Figma API
FIGMA_ACCESS_TOKEN=your_figma_token_here

# AI Configuration (supports any LLM via LiteLLM)
AI_BASE_URL=https://litellm.tarento.dev
AI_API_KEY=your_api_key
AI_MODEL=gemini-pro

# Optional: Adjust parameters
AI_TEMPERATURE=0.3
AI_MAX_TOKENS=2000
```

### 3. Use the VS Code Extension

Open your Flutter project in VS Code and use:
- `Figma: Generate Widget` - Generate Flutter widgets from Figma
- `Figma: Generate Tests` - Generate widget tests

## Supported AI Models

FigmaFlow is **100% LLM-agnostic**. Simply change `AI_MODEL` in `.env`:

**Popular choices:**
- `gpt-5`, `gpt-4o` (OpenAI)
- `gemini-pro`, `gemini-1.5-flash` (Google)
- `claude-3-5-sonnet`, `claude-3-haiku` (Anthropic)
- `llama3` (Local via Ollama)

### Using Different Providers

**LiteLLM Proxy (Recommended):**
```bash
AI_BASE_URL=https://litellm.tarento.dev
AI_API_KEY=your_litellm_key
AI_MODEL=gemini-pro
```

**Direct OpenAI:**
```bash
# Remove AI_BASE_URL or comment it out
OPENAI_API_KEY=sk-your_openai_key
AI_MODEL=gpt-4o
```

**Local Models (Ollama):**
```bash
AI_BASE_URL=http://localhost:11434/v1
AI_API_KEY=ollama
AI_MODEL=llama3
```

## Features

### 🎯 Token Filtering (52-71% savings)
Intelligently removes Figma metadata while preserving design essentials, reducing API costs.

### 🔄 Rate Limiting Protection
Automatic retry with exponential backoff when hitting API limits.

### 💾 Response Caching
24-hour cache for Figma responses reduces redundant API calls.

### 🤖 LLM Agnostic
Use any AI model - switch by changing one line in `.env`.

## Testing Configuration

Test your setup:

```bash
cd mcp-server

# Test LiteLLM connection
python3 test_litellm.py

# Test specific model
python3 test_model_switch.py gpt-5
python3 test_model_switch.py claude-3-5-sonnet

# Test token filtering
python3 test_token_filter.py
```

## Configuration Files

**Single source of truth:** `mcp-server/.env`

This file is used by:
- VS Code extension
- Standalone Python scripts
- All test utilities

## Getting API Keys

**Figma Token:**
1. Go to https://www.figma.com/settings
2. Scroll to "Personal Access Tokens"
3. Create new token
4. Copy to `FIGMA_ACCESS_TOKEN` in `.env`

**AI API Key:**
- **LiteLLM**: Contact your LiteLLM provider
- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/
- **Google**: https://makersuite.google.com/app/apikey

## Troubleshooting

### "Configuration not found"
- Make sure `mcp-server/.env` exists
- Copy from `.env.example` if needed

### "429 Too Many Requests"
- Wait a few seconds and retry
- System has automatic retry with backoff
- Response caching reduces API calls

### "Model not found"
- Check model name matches your provider
- Verify `AI_BASE_URL` is correct
- Test with `python3 test_model_switch.py your-model`

## Advanced: Token Optimization

The token filter is pre-configured for optimal savings:

**Filter Levels:**
- `AGGRESSIVE` - Maximum savings (70%+)
- `BALANCED` - Good balance (50-60%) - **Default**
- `CONSERVATIVE` - Minimal filtering (30-40%)

To change filter level, edit `src/utils/token_filter.py`.

## Architecture

```
VS Code Extension
    ↓
Loads mcp-server/.env
    ↓
MCP Server (Python)
    ↓
┌─────────────┬─────────────────┐
│ Figma API   │ AI Provider     │
│ (cached)    │ (via LiteLLM)   │
└─────────────┴─────────────────┘
```

- **Token Filter**: Reduces Figma data by 52-71%
- **Rate Limiter**: Handles 429 errors automatically
- **Cache**: 24-hour TTL for Figma responses

## Project Structure

```
FigmaFlow-MCP/
├── mcp-server/           # Backend server
│   ├── .env             # ← API keys here
│   ├── .env.example     # Template
│   ├── src/
│   │   ├── figma/       # Figma API client
│   │   ├── ai/          # AI client (LiteLLM)
│   │   └── utils/       # Token filter, caching
│   └── test_*.py        # Test scripts
│
└── vscode-extension/    # VS Code extension
    └── src/
```

## Documentation

- **This file** - Complete user guide
- `API_KEY_FLOW.md` - How credentials flow through the system
- `vscode-extension/CONFIGURATION.md` - Extension-specific setup

---

**Questions?** Check existing documentation or raise an issue in the project repository.
