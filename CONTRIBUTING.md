# Contributing to FigmaFlow-MCP

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Development Setup

See [SETUP.md](SETUP.md) for complete setup instructions.

Quick start:
```bash
# Clone repository
git clone https://github.com/yourusername/FigmaFlow-MCP.git
cd FigmaFlow-MCP

# Install dependencies
cd mcp-server && poetry install && cd ..
cd vscode-extension && npm install && cd ..
```

## Project Structure

- `mcp-server/` - Python MCP server (AI + Figma integration)
- `vscode-extension/` - TypeScript VS Code extension
- `plan/` - Product documentation (PRD, development plan)

## Making Changes

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

Follow the coding standards:

**Python (MCP Server):**
- Use type hints
- Follow PEP 8
- Document functions with docstrings
- Run formatters:
  ```bash
  cd mcp-server
  poetry run black src/
  poetry run ruff check src/
  poetry run mypy src/
  ```

**TypeScript (VS Code Extension):**
- Use TypeScript types
- Follow ES6+ conventions
- Add JSDoc comments
- Run linter:
  ```bash
  cd vscode-extension
  npm run lint
  ```

### 3. Test Your Changes

```bash
# Python tests
cd mcp-server
poetry run pytest

# TypeScript compilation
cd vscode-extension
npm run compile
npm test

# Quick validation
cd mcp-server
poetry run python quick_test.py
```

### 4. Commit Your Changes

Use conventional commits:
```bash
git commit -m "feat: add new widget generator option"
git commit -m "fix: correct color conversion bug"
git commit -m "docs: update setup guide"
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `test`: Tests
- `refactor`: Code refactoring
- `chore`: Maintenance

### 5. Submit Pull Request

- Push to your fork
- Create PR with description of changes
- Link related issues
- Wait for review

## Areas for Contribution

### High Priority
- [ ] Additional AI model support (Claude, Gemini)
- [ ] More Flutter widget types
- [ ] Better error handling
- [ ] Performance optimizations

### Medium Priority
- [ ] Additional test coverage
- [ ] UI/UX improvements in VS Code extension
- [ ] Configuration options
- [ ] Documentation improvements

### Good First Issues
- [ ] Add more test cases
- [ ] Improve error messages
- [ ] Update documentation
- [ ] Fix typos

## Code Review Process

1. All PRs require review
2. Tests must pass
3. Code must follow style guidelines
4. Documentation must be updated

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

- Open an issue for bugs
- Start a discussion for feature ideas
- Check existing documentation first

Thank you for contributing! 🙏
