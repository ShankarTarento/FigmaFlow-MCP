# FigmaFlow-MCP

<div align="center">

**AI-powered Figma to Flutter converter**

Generate Flutter widgets and tests from Figma designs directly in VS Code

[Features](#features) • [Installation](#installation) • [Quick Start](#quick-start) • [Documentation](#documentation)

</div>

---

## Overview

FigmaFlow-MCP is an AI-powered tool that bridges the gap between design and development. It converts Figma designs into production-ready Flutter widgets and tests, all within your VS Code workspace.

### Key Features

- 🎨 **Figma Integration** - Fetch designs directly from Figma API
- 🤖 **AI-Powered Generation** - Uses GPT-4 to generate clean Flutter code
- 🧪 **Test Generation** - Automatically create widget tests
- 🔌 **MCP Protocol** - Built on Model Context Protocol for reliability
- 🐧 **Linux-First** - Native support for Linux developers
- 🔑 **Secure Configuration** - Local .env file for API keys

## Architecture

```
┌─────────────────┐
│  VS Code        │
│  Extension      │
└────────┬────────┘
         │ MCP Protocol
┌────────▼────────┐
│  MCP Server     │◄──── Figma API
│  (Python)       │
└────────┬────────┘
         │
     ┌───▼───┐
     │  AI   │
     │ Model │
     └───────┘
```

## Project Structure

```
FigmaFlow-MCP/
├── mcp-server/          # Python MCP server
│   ├── src/
│   │   ├── mcp/         # Server core
│   │   ├── figma/       # Figma integration
│   │   ├── generators/  # Code generators
│   │   ├── ai/          # AI client
│   │   └── utils/       # Utilities
│   └── tests/
├── vscode-extension/    # TypeScript extension
│   └── src/
│       ├── commands/    # VS Code commands
│       ├── mcp/         # MCP client
│       ├── ui/          # User interface
│       └── utils/
└── plan/                # Project documentation
```

## Installation

### For Users

1. Install from VS Code Marketplace (coming soon)
2. Run setup wizard to configure API keys
3. Start generating!

### For Developers

1. Clone the repository:
```bash
git clone https://github.com/yourusername/FigmaFlow-MCP.git
cd FigmaFlow-MCP
```

2. Set up MCP server:
```bash
cd mcp-server
poetry install
cp .env.example .env
# Edit .env with your API keys
```

3. Set up VS Code extension:
```bash
cd ../vscode-extension
npm install
npm run compile
```

4. Open in VS Code and press F5 to launch Extension Development Host

## Quick Start

### 1. Configure API Keys

Run the setup wizard in VS Code:
```
Cmd+Shift+P → "FigmaFlow: Setup API Keys"
```

### 2. Generate Widget

```
Cmd+Shift+P → "FigmaFlow: Generate Flutter Widget from Figma"
```

Enter your Figma URL and widget name, and the code will be generated!

## Documentation

- [Development Plan](plan/development_plan.md) - Comprehensive implementation guide
- [PRD](plan/prd.txt) - Product requirements document
- [MCP Server README](mcp-server/README.md) - Server documentation
- [Extension README](vscode-extension/README.md) - Extension documentation

## Development Roadmap

- [x] Phase 0: Planning & Architecture
- [/] Phase 1: Foundation & Setup
- [ ] Phase 2: MCP Server Core
- [ ] Phase 3: Code Generation
- [ ] Phase 4: VS Code Extension
- [ ] Phase 5: Integration & Testing
- [ ] Phase 6: Documentation & Launch

## Requirements

- **VS Code**: 1.85 or higher
- **Python**: 3.10 or higher
- **Node.js**: 18 or higher
- **Flutter SDK**: For testing generated code
- **Figma Account**: With API access
- **OpenAI Account**: With API access

## Configuration

The project uses `.env` files for configuration:

```bash
# .env
FIGMA_ACCESS_TOKEN=figd_xxxxx
AI_API_KEY=sk-xxxxx
MCP_SERVER_PORT=3000
LOG_LEVEL=INFO
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details

## Support

- 🐛 [Report a bug](https://github.com/yourusername/figmaflow-mcp/issues)
- 💡 [Request a feature](https://github.com/yourusername/figmaflow-mcp/issues)
- 📧 Email: support@figmaflow.dev

## Acknowledgments

- Built with [Model Context Protocol](https://modelcontextprotocol.io)
- Powered by [OpenAI](https://openai.com)
- Design data from [Figma API](https://www.figma.com/developers/api)

---

<div align="center">
Made with ❤️ for the Flutter community
</div>
