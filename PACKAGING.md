# Packaging & Distribution Guide

How to package and publish FigmaFlow-MCP.

## Prerequisites

- VS Code Extension Manager (vsce)
- Poetry (for Python packaging)
- GitHub account
- VS Code Marketplace account (for publishing)

## Install Tools

```bash
# Install vsce globally
npm install -g @vscode/vsce

# Verify installation
vsce --version
```

## Package VS Code Extension

### 1. Update Version

Edit `vscode-extension/package.json`:
```json
{
  "version": "0.1.0",  // Update this
  ...
}
```

### 2. Build Extension

```bash
cd vscode-extension

# Install dependencies
npm install

# Compile TypeScript
npm run compile

# Package extension
vsce package
```

This creates: `figmaflow-mcp-0.1.0.vsix`

### 3. Test VSIX Locally

```bash
code --install-extension figmaflow-mcp-0.1.0.vsix
```

### 4. Publish to Marketplace

**First time setup:**
1. Create publisher: https://marketplace.visualstudio.com/manage
2. Create Personal Access Token in Azure DevOps
3. Login with vsce:
   ```bash
   vsce login <publisher-name>
   ```

**Publish:**
```bash
vsce publish
```

Or publish specific version:
```bash
vsce publish minor  # 0.1.0 -> 0.2.0
vsce publish patch  # 0.1.0 -> 0.1.1
vsce publish major  # 0.1.0 -> 1.0.0
```

## Package MCP Server

### 1. Update Version

Edit `mcp-server/pyproject.toml`:
```toml
[tool.poetry]
version = "0.1.0"  # Update this
```

### 2. Build Package

```bash
cd mcp-server

# Build distribution
poetry build
```

This creates:
- `dist/figmaflow_mcp_server-0.1.0.tar.gz` (source)
- `dist/figmaflow_mcp_server-0.1.0-py3-none-any.whl` (wheel)

### 3. Test Install

```bash
# In a test environment
pip install dist/figmaflow_mcp_server-0.1.0-py3-none-any.whl
```

### 4. Publish to PyPI

**First time setup:**
```bash
poetry config pypi-token.pypi <your-pypi-token>
```

**Publish:**
```bash
poetry publish
```

Or use TestPyPI first:
```bash
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry publish -r testpypi
```

## Bundle MCP Server with Extension

For easier distribution, bundle the MCP server with the extension:

### 1. Copy MCP Server

```bash
cd vscode-extension

# Create mcp-server directory
mkdir -p mcp-server

# Copy MCP server files
cp -r ../mcp-server/src mcp-server/
cp ../mcp-server/pyproject.toml mcp-server/
```

### 2. Update .vscodeignore

Edit `vscode-extension/.vscodeignore`:
```
# Don't exclude mcp-server
!mcp-server/**
```

### 3. Update package.json

Add installation script:
```json
{
  "scripts": {
    "postinstall": "cd mcp-server && poetry install"
  }
}
```

### 4. Package

```bash
vsce package
```

Now the extension includes the MCP server!

## GitHub Release

### 1. Create Tag

```bash
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

### 2. Create Release on GitHub

1. Go to https://github.com/yourusername/figmaflow-mcp/releases
2. Click "Draft a new release"
3. Select tag: v0.1.0
4. Title: "FigmaFlow MCP v0.1.0"
5. Description:
   ```markdown
   ## Features
   - Generate Flutter widgets from Figma designs
   - Auto-generate widget tests
   - Easy API key configuration
   
   ## Installation
   Download `figmaflow-mcp-0.1.0.vsix` and install in VS Code:
   ```
   code --install-extension figmaflow-mcp-0.1.0.vsix
   ```
   
   ## Documentation
   See [User Guide](USER_GUIDE.md) for complete instructions.
   ```
6. Upload files:
   - `vscode-extension/figmaflow-mcp-0.1.0.vsix`
   - `mcp-server/dist/` files
7. Click "Publish release"

## Distribution Checklist

Before publishing:

- [ ] All tests pass
- [ ] Version numbers updated
- [ ] CHANGELOG.md updated
- [ ] README.md accurate
- [ ] Screenshots/demo added
- [ ] License file present
- [ ] Dependencies reviewed
- [ ] Security audit done
- [ ] Documentation complete

## Update Changelog

Create/update `CHANGELOG.md`:

```markdown
# Changelog

## [0.1.0] - 2026-02-04

### Added
- Initial release
- Flutter widget generation from Figma
- Widget test generation
- API key configuration wizard
- MCP server integration

### Dependencies
- VS Code 1.85+
- Python 3.10+
- OpenAI API
- Figma API
```

## Security Considerations

**Before publishing:**

1. **Remove secrets:**
   ```bash
   # Check for exposed secrets
   git log -p | grep -i "api_key\|token\|secret"
   ```

2. **Audit dependencies:**
   ```bash
   # Python
   cd mcp-server
   poetry show --tree
   
   # Node.js
   cd vscode-extension
   npm audit
   ```

3. **Review permissions:**
   - Extension only needs workspace file access
   - No network calls except to APIs
   - No telemetry without consent

## Automated Publishing

### GitHub Actions

Create `.github/workflows/release.yml`:

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install vsce
        run: npm install -g @vscode/vsce
      
      - name: Build Extension
        run: |
          cd vscode-extension
          npm install
          npm run compile
          vsce package
      
      - name: Create Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          files: vscode-extension/*.vsix
```

## Marketplace Optimization

### Extension Icon

Create `vscode-extension/assets/icon.png`:
- Size: 128x128 pixels
- Format: PNG
- Transparent background
- Represents Figma → Flutter

### Screenshots

Add to `vscode-extension/assets/`:
- `screenshot-1.png` - Setup wizard
- `screenshot-2.png` - Widget generation
- `screenshot-3.png` - Generated code

### README Polish

Ensure `vscode-extension/README.md` includes:
- Clear feature list
- Screenshots
- Quick start guide
- Link to full documentation

## Post-Release

1. **Announce:**
   - Twitter/X
   - Dev.to blog post
   - Reddit r/FlutterDev
   - LinkedIn

2. **Monitor:**
   - GitHub issues
   - Marketplace reviews
   - Download stats

3. **Support:**
   - Respond to issues quickly
   - Update documentation based on questions
   - Plan next release

---

Congrats on your release! 🎉
