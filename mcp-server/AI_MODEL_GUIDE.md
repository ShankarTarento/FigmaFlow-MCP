# Using Any AI Model with FigmaFlow

FigmaFlow is **completely LLM-agnostic**. You can use any AI model by simply changing the `.env` file.

## Quick Model Switch

### To use GPT-5 (or any OpenAI model):

**Option 1: Via LiteLLM proxy**
```bash
# .env
AI_BASE_URL=https://litellm.tarento.dev
AI_API_KEY=your_litellm_api_key
AI_MODEL=gpt-5  # Just change this!
```

**Option 2: Direct OpenAI**
```bash
# .env
# Remove or comment out AI_BASE_URL
OPENAI_API_KEY=your_openai_api_key
AI_MODEL=gpt-5  # Just change this!
```

That's it! No code changes needed.

## Supported Models

### Via LiteLLM Proxy (Recommended)

LiteLLM supports 100+ models. Just change `AI_MODEL`:

**OpenAI Models:**
```bash
AI_MODEL=gpt-5
AI_MODEL=gpt-4o
AI_MODEL=gpt-4-turbo
AI_MODEL=gpt-3.5-turbo
```

**Google Models:**
```bash
AI_MODEL=gemini-pro
AI_MODEL=gemini-1.5-pro
AI_MODEL=gemini-1.5-flash
```

**Anthropic Models:**
```bash
AI_MODEL=claude-3-5-sonnet
AI_MODEL=claude-3-opus
AI_MODEL=claude-3-sonnet
AI_MODEL=claude-3-haiku
```

**Other Models:**
```bash
AI_MODEL=llama-3-70b
AI_MODEL=mistral-large
AI_MODEL=command-r-plus
```

### Direct Provider Access

You can also connect directly to any provider:

**OpenAI Direct:**
```bash
# .env
OPENAI_API_KEY=sk-...
AI_MODEL=gpt-5
# Don't set AI_BASE_URL
```

**Custom OpenAI-compatible API:**
```bash
# .env
AI_BASE_URL=https://your-custom-api.com/v1
AI_API_KEY=your_api_key
AI_MODEL=your-model-name
```

## Configuration Examples

### Example 1: Using GPT-5
```bash
# .env
AI_BASE_URL=https://litellm.tarento.dev
AI_API_KEY=your_key
AI_MODEL=gpt-5
AI_TEMPERATURE=0.3
AI_MAX_TOKENS=2000
```

### Example 2: Using Claude 3.5 Sonnet
```bash
# .env
AI_BASE_URL=https://litellm.tarento.dev
AI_API_KEY=your_key
AI_MODEL=claude-3-5-sonnet
AI_TEMPERATURE=0.3
AI_MAX_TOKENS=2000
```

### Example 3: Using Local LLM (Ollama)
```bash
# .env
AI_BASE_URL=http://localhost:11434/v1
AI_API_KEY=ollama  # Ollama doesn't require real key
AI_MODEL=llama3
AI_TEMPERATURE=0.3
AI_MAX_TOKENS=2000
```

### Example 4: Using Azure OpenAI
```bash
# .env
AI_BASE_URL=https://your-resource.openai.azure.com
AI_API_KEY=your_azure_key
AI_MODEL=gpt-4
AI_TEMPERATURE=0.3
AI_MAX_TOKENS=2000
```

## How It Works

The FigmaFlow AI client is built on OpenAI's SDK, which is compatible with:
- ✅ OpenAI API
- ✅ LiteLLM proxy (supports 100+ models)
- ✅ Any OpenAI-compatible API endpoint
- ✅ Azure OpenAI
- ✅ Local models (Ollama, LocalAI, etc.)

**No code changes needed** - just update `.env`!

## Testing Different Models

Use the test script to verify any model:

```bash
cd /home/shankarganeshi/PlayGround/FigmaFlow-MCP/mcp-server
python3 test_litellm.py
```

This will:
1. Load your `.env` configuration
2. Connect to the specified model
3. Generate a test Flutter widget
4. Confirm the model is working

## Model Selection Guide

### For Code Generation (Widgets):

**Best Quality:**
- `gpt-5` (if available)
- `claude-3-5-sonnet`
- `gpt-4o`

**Best Value:**
- `gemini-1.5-flash` (fast & cheap)
- `gpt-3.5-turbo`
- `gemini-pro`

**Local/Private:**
- `llama-3-70b` (via Ollama)
- `mistral-large`

### For QA Test Generation:

**Best Quality:**
- `claude-3-5-sonnet` (excellent at test cases)
- `gpt-4o`

**Best Value:**
- `gemini-1.5-flash`
- `gpt-3.5-turbo`

## Advanced: Multiple Models

You can even use different models for different tasks by setting them programmatically:

```python
from src.ai.client import AIClient

# Use GPT-5 for widgets
widget_client = AIClient(model="gpt-5")

# Use cheaper model for QA
qa_client = AIClient(model="gemini-pro")
```

## Cost Optimization Tips

1. **Use token filtering** (already implemented!) - saves 52-71% on input tokens
2. **Choose efficient models**:
   - `gemini-1.5-flash` - Best price/performance
   - `gpt-3.5-turbo` - Fast and cheap
   - `claude-3-haiku` - Anthropic's cheapest

3. **Adjust parameters**:
   ```bash
   AI_MAX_TOKENS=1500  # Reduce if widgets are simple
   AI_TEMPERATURE=0.1  # Lower = more deterministic, fewer retries
   ```

## Switching Models: Step-by-Step

1. **Edit `.env` file:**
   ```bash
   nano /home/shankarganeshi/PlayGround/FigmaFlow-MCP/mcp-server/.env
   ```

2. **Change AI_MODEL line:**
   ```bash
   AI_MODEL=gpt-5  # or any other model
   ```

3. **Save and close**

4. **Test the change:**
   ```bash
   python3 test_litellm.py
   ```

5. **Done!** All widget and QA generation now uses the new model.

---

**🎯 Bottom Line:** FigmaFlow is fully LLM-agnostic. Switch models anytime by editing one line in `.env`!
