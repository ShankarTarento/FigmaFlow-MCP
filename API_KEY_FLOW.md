# API Key Configuration: Extension vs MCP Server

## Quick Answer

**The VS Code extension uses the keys provided by the user during initialization**, NOT the `.env` file in the `mcp-server` directory.

## The Two `.env` Files

There are **two separate `.env` files** in this project:

### 1. **Workspace `.env`** (Used by Extension)
- **Location**: Your workspace root (e.g., your Flutter project)
- **Created by**: Extension setup wizard
- **Used by**: VS Code extension
- **Created via**: `FigmaFlow: Setup Configuration` command

### 2. **MCP Server `.env`** (Used for standalone testing)
- **Location**: `/home/shankarganeshi/PlayGround/FigmaFlow-MCP/mcp-server/.env`
- **Used by**: Standalone Python scripts and direct server testing
- **Not used by**: VS Code extension

## Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ VS Code Extension Flow                                          │
└─────────────────────────────────────────────────────────────────┘

Step 1: User runs "FigmaFlow: Setup Configuration"
   ↓
Step 2: Extension prompts for:
   • Figma Access Token
   • OpenAI API Key
   ↓
Step 3: Extension creates .env in WORKSPACE ROOT
   /your-flutter-project/.env
   FIGMA_ACCESS_TOKEN=user_provided_token
   OPENAI_API_KEY=user_provided_key
   ↓
Step 4: User runs "Generate Widget"
   ↓
Step 5: Extension loads .env from WORKSPACE
   (NOT from mcp-server/.env)
   ↓
Step 6: Extension passes keys DIRECTLY to MCP server as parameters:
   mcpClient.callTool('get_figma_design', {
       fileUrl: "https://...",
       accessToken: env.FIGMA_ACCESS_TOKEN  ← From workspace .env
   })
   
   mcpClient.callTool('generate_flutter_widget', {
       designData: {...},
       openaiApiKey: env.OPENAI_API_KEY  ← From workspace .env
   })
   ↓
Step 7: MCP Server receives keys as tool parameters
   (Does NOT read from its own .env file)
   ↓
Step 8: MCP Server uses provided keys to:
   • Create FigmaClient(args["accessToken"])
   • Create AIClient(api_key=args["openaiApiKey"])
```

## Code Evidence

### Extension: Loads from Workspace `.env`

**File**: `vscode-extension/src/utils/environment.ts`
```typescript
export async function loadEnvironment(): Promise<Environment | null> {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    const envPath = path.join(workspaceFolder.uri.fsPath, '.env');  // ← Workspace .env
    
    dotenv.config({ path: envPath });
    
    return {
        FIGMA_ACCESS_TOKEN: process.env.FIGMA_ACCESS_TOKEN,
        OPENAI_API_KEY: process.env.OPENAI_API_KEY
    };
}
```

### Extension: Passes Keys to MCP Server

**File**: `vscode-extension/src/commands/generateWidget.ts`
```typescript
// Load from workspace .env
const env = await loadEnvironment();

// Pass to MCP server as parameters
await mcpClient.callTool('get_figma_design', {
    fileUrl: figmaUrl,
    accessToken: env.FIGMA_ACCESS_TOKEN  // ← Passed as parameter
});

await mcpClient.callTool('generate_flutter_widget', {
    designData: designData,
    openaiApiKey: env.OPENAI_API_KEY,   // ← Passed as parameter
});
```

### MCP Server: Receives Keys as Parameters

**File**: `mcp-server/src/mcp/server.py`
```python
Tool(
    name="get_figma_design",
    inputSchema={
        "properties": {
            "fileUrl": {...},
            "accessToken": {              # ← Required parameter
                "type": "string",
                "description": "Figma API access token"
            }
        },
        "required": ["fileUrl", "accessToken"]
    }
)
```

**File**: `mcp-server/src/mcp/tools.py`
```python
async def handle_get_figma_design(self, args):
    # Uses accessToken from args, NOT from environment
    figma_client = FigmaClient(args["accessToken"])  # ← From parameter
```

## When Each `.env` is Used

### Workspace `.env` (Your Project Root)
**Used when:**
- ✅ Running "Generate Widget" from VS Code
- ✅ Running "Generate Tests" from VS Code
- ✅ Using the extension in any way

**Contains:**
```bash
FIGMA_ACCESS_TOKEN=from_setup_wizard
OPENAI_API_KEY=from_setup_wizard
```

### MCP Server `.env` (`mcp-server/.env`)
**Used when:**
- ✅ Running standalone Python tests: `python3 test_litellm.py`
- ✅ Running token filter demo: `python3 demo_token_filter.py`
- ✅ Testing MCP server directly without extension

**Contains:**
```bash
FIGMA_ACCESS_TOKEN=your_figma_token
AI_BASE_URL=https://litellm.tarento.dev
AI_API_KEY=your_litellm_key
AI_MODEL=gemini-pro
```

## Summary Table

| Scenario | Which .env? | How Keys are Used |
|----------|-------------|-------------------|
| **VS Code Extension** | Workspace `.env` | Keys passed as tool parameters |
| **Standalone Python Testing** | `mcp-server/.env` | Keys loaded from environment |
| **Direct API Testing** | `mcp-server/.env` | Keys loaded from environment |

## Important Notes

1. **Keys are NEVER hardcoded** in the MCP server
2. **Extension controls the keys** - server just uses what it receives
3. **Two separate configurations** exist for different use cases
4. **MCP server is stateless** - doesn't store any credentials

## To Configure for Extension Use

```bash
# 1. Open your Flutter project in VS Code
# 2. Run: FigmaFlow: Setup Configuration
# 3. Enter your Figma token
# 4. Enter your OpenAI/LiteLLM key
# 5. Done! Extension creates workspace .env
```

## To Configure for Standalone Testing

```bash
# 1. Edit mcp-server/.env
nano /home/shankarganeshi/PlayGround/FigmaFlow-MCP/mcp-server/.env

# 2. Set your keys
FIGMA_ACCESS_TOKEN=your_token
AI_API_KEY=your_key
AI_BASE_URL=https://litellm.tarento.dev
AI_MODEL=gemini-pro

# 3. Run tests
python3 test_litellm.py
```

---

**Bottom Line**: The extension uses **user-provided keys from workspace `.env`**, passing them as parameters to the MCP server. The `mcp-server/.env` is only for standalone testing and development.
