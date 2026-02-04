# Changelog

All notable changes to FigmaFlow-MCP will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-02-04

### Added

**Core Features:**
- 🎨 Flutter widget generation from Figma designs using AI
- 🧪 Automatic widget test generation
-  QA test case generation for manual testing
- 🔑 Interactive API key setup wizard
- 🔗 MCP (Model Context Protocol) server integration
- 🤖 OpenAI GPT-4o integration for code generation

**VS Code Extension:**
- Command: `FigmaFlow: Setup API Keys` - Configure Figma and OpenAI tokens
- Command: `FigmaFlow: Generate Flutter Widget from Figma` - Convert designs to code
- Command: `FigmaFlow: Generate Widget Tests from Figma` - Create automated tests
- Automatic .env file creation and .gitignore management
- Environment validation and helpful error messages
- Progress indicators for long-running operations

**MCP Server:**
- Three MCP tools: `get_figma_design`, `generate_flutter_widget`, `generate_widget_tests`
- Figma API client with URL parsing and node fetching
- Design parser that converts Figma nodes to Flutter-compatible structure
- Color conversion (Figma RGBA → Flutter Color)
- Type mapping (Figma types → Flutter widgets)
- Comprehensive prompt engineering for high-quality code generation
- Input validation utilities

**Developer Experience:**
- Complete setup guide (SETUP.md)
- Comprehensive testing guide (TESTING.md)
- User guide with workflows and best practices (USER_GUIDE.md)
- Contributing guidelines (CONTRIBUTING.md)
- Quick test script for validation
- Type-safe code with Python type hints and TypeScript types

**Documentation:**
- Product Requirements Document (PRD)
- 10-week development plan with detailed implementation
- README files for all components
- MIT License

### Dependencies

**VS Code Extension:**
- @modelcontextprotocol/sdk ^1.0.0
- axios ^1.6.0
- dotenv ^16.4.0
- TypeScript ^5.3.0

**MCP Server:**
- mcp ^1.26.0
- httpx ^0.27.0
- pydantic ^2.0.0
- openai ^1.109.1
- python-dotenv ^1.0.0
- pytest ^8.4.2 (dev)
- black ^24.10.0 (dev)
- ruff ^0.3.7 (dev)

### Requirements

- VS Code 1.85 or later
- Python 3.10 or later
- Node.js 18 or later
- Figma account with API access
- OpenAI account with API access

### Known Limitations

- Supports Flutter Material Design widgets only
- Requires  internet connection for API calls
- AI generation time: 10-20 seconds per widget
- Complex nested layouts may need manual refinement
- StatelessWidget by default (StatefulWidget requires manual conversion)

### Security

- API keys stored in local .env file (git-ignored)
- No telemetry or data collection
- Tokens never sent to third parties except Figma/OpenAI APIs
- No persistent storage of API responses

---

## Version History

### [0.1.0] - 2026-02-04
Initial release with core functionality.

---

## Future Roadmap

### [0.2.0] - Planned
- Support for Claude and Gemini AI models
- StatefulWidget generation option
- Component library detection and reuse
- Batch generation for multiple screens
- Improved error messages

### [0.3.0] - Planned
- Design drift detection
- Auto-update on Figma changes
- Custom widget templates
- Theme integration
- Cupertino widgets support

### [1.0.0] - Future
- CI/CD integration
- Team collaboration features
- Analytics dashboard
- Premium AI models
- Enterprise support

---

[Unreleased]: https://github.com/yourusername/figmaflow-mcp/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/figmaflow-mcp/releases/tag/v0.1.0
