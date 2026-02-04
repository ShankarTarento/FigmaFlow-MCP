# FigmaFlow MCP Server

Backend MCP server that converts Figma designs into Flutter UI code and tests using AI.

## Features

- 🎨 Fetch design data from Figma API
- 🤖 AI-powered Flutter widget generation
- 🧪 Automatic widget test generation
- 📋 QA test case generation
- 🔌 MCP protocol support

## Setup

### Prerequisites

- Python 3.10 or higher
- Poetry (for dependency management)
- Figma API access token
- OpenAI API key

### Installation

1. Install dependencies:
```bash
poetry install
```

2. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

3. Run the server:
```bash
poetry run python src/mcp/server.py
```

## Development

### Running Tests

```bash
poetry run pytest
```

### Code Formatting

```bash
poetry run black src/
poetry run ruff check src/
```

### Type Checking

```bash
poetry run mypy src/
```

## MCP Tools

### get_figma_design
Fetches design data from a Figma file or specific node.

**Input:**
- `fileUrl`: Figma file URL
- `nodeId` (optional): Specific node ID
- `accessToken`: Figma API token

**Output:** Parsed design data in JSON format

### generate_flutter_widget
Generates Flutter widget code from design data.

**Input:**
- `designData`: Parsed Figma design
- `widgetName`: Name for the widget
- `options`: Generation options (stateful, includeImports)

**Output:** Flutter widget code

### generate_widget_tests
Generates widget tests from widget code.

**Input:**
- `widgetCode`: Generated widget code
- `designData`: Design data for test scenarios

**Output:** Flutter test code

## Project Structure

```
mcp-server/
├── src/
│   ├── mcp/           # MCP server core
│   ├── figma/         # Figma API integration
│   ├── generators/    # Code generators
│   ├── ai/            # AI client
│   └── utils/         # Utilities
├── tests/             # Test suite
└── pyproject.toml     # Project config
```

## Environment Variables

See `.env.example` for all available configuration options.

## License

MIT
