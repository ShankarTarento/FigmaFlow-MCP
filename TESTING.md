# Testing Guide

How to test FigmaFlow-MCP end-to-end.

## Quick Test Checklist

- [ ] MCP Server starts successfully
- [ ] VS Code extension loads
- [ ] Setup wizard creates .env
- [ ] Figma design fetches successfully  
- [ ] Widget code generates
- [ ] Generated code compiles
- [ ] Widget tests generate
- [ ] Tests run successfully

## Test 1: MCP Server Standalone

Test the MCP server independently:

```bash
cd mcp-server

# Create test .env
cp .env.example .env
# Add your actual tokens to .env

# Start server
poetry run python src/mcp/server.py
```

**Expected:** Server starts, waits for MCP protocol messages over stdio

**Test manually with MCP Inspector (optional):**
```bash
npx @modelcontextprotocol/inspector poetry run python src/mcp/server.py
```

## Test 2: Unit Tests

### Python Tests

```bash
cd mcp-server
poetry run pytest -v

# Test specific module
poetry run pytest tests/test_figma_client.py -v

# With coverage
poetry run pytest --cov=src tests/
```

**Expected:** All tests pass

### TypeScript Tests

```bash
cd vscode-extension
npm test
```

**Expected:** All tests pass

## Test 3: Integration Test - Widget Generation

### Prerequisites
- Valid Figma access token
- Valid AI API key
- Test Figma file URL

### Steps

1. **Create test Figma design:**
   - Go to Figma
   - Create new file
   - Add a simple frame:
     ```
     Container (Frame)
     ├── Background (Rectangle, color #2196F3)
     └── Label (Text, "Click Me")
     ```
   - Copy the file URL

2. **Launch extension:**
   ```bash
   cd vscode-extension
   code .
   # Press F5
   ```

3. **In Extension Development Host:**
   - Create empty folder or open Flutter project
   - `Cmd+Shift+P` → "FigmaFlow: Setup API Keys"
   - Enter your tokens
   - `Cmd+Shift+P` → "FigmaFlow: Generate Flutter Widget from Figma"
   - Enter Figma URL
   - Enter widget name: `TestButton`

4. **Verify output:**
   - Widget code appears in editor
   - Code includes:
     ```dart
     import 'package:flutter/material.dart';
     
     class TestButton extends StatelessWidget {
       @override
       Widget build(BuildContext context) {
         return Container(
           // ... generated layout
         );
       }
     }
     ```

## Test 4: Integration Test - Test Generation

1. **Generate tests:**
   - `Cmd+Shift+P` → "FigmaFlow: Generate Widget Tests from Figma"
   - Use same Figma URL
   - Enter widget name: `TestButton`

2. **Verify output:**
   - Test code appears
   - Includes:
     ```dart
     import 'package:flutter_test/flutter_test.dart';
     import 'package:flutter/material.dart';
     
     void main() {
       testWidgets('TestButton renders correctly', (tester) async {
         // ... generated tests
       });
     }
     ```

## Test 5: Flutter Code Validation

If you have Flutter SDK installed:

1. **Create Flutter project:**
   ```bash
   flutter create test_figmaflow
   cd test_figmaflow
   ```

2. **Add generated widget:**
   - Copy generated widget code to `lib/test_button.dart`

3. **Compile check:**
   ```bash
   flutter analyze
   ```

4. **Run widget:**
   - Use the widget in `lib/main.dart`
   ```bash
   flutter run
   ```

5. **Run tests:**
   - Copy generated tests to `test/test_button_test.dart`
   ```bash
   flutter test
   ```

**Expected:**
- ✅ Code analyzes with no errors
- ✅ App compiles and runs
- ✅ Widget displays correctly
- ✅ Tests pass

## Test 6: Error Handling

Test error scenarios:

### Invalid Figma Token
1. Set wrong token in .env
2. Try generating widget
3. **Expected:** Clear error message about authentication

### Invalid Figma URL
1. Enter URL: `https://example.com/notfigma`
2. **Expected:** Validation error "Please enter a valid Figma URL"

### Missing AI API Key
1. Remove `AI_API_KEY` from .env
2. Try generating widget
3. **Expected:** Error about missing API key

### Invalid Widget Name
1. Enter widget name: `lowercase`
2. **Expected:** Validation error about PascalCase

## Performance Tests

### Measure Generation Time

```bash
# Time widget generation
time poetry run python src/mcp/server.py < test_input.json
```

**Expected:** 
- Figma fetch: < 2 seconds
- AI generation: 5-15 seconds
- Total end-to-end: < 20 seconds

## Continuous Testing

### Watch mode for development

**Terminal 1 - Python:**
```bash
cd mcp-server
poetry run pytest-watch
```

**Terminal 2 - TypeScript:**
```bash
cd vscode-extension
npm run watch
```

## Test Data

### Sample Figma URLs

Create your own test files with these patterns:

1. **Simple Button:** Single frame with rectangle + text
2. **Card:** Frame with image, title, description
3. **Form:** Multiple text inputs and button
4. **List Item:** Repeatable component with icon + text
5. **Complex Layout:** Nested frames, multiple widgets

### Sample Widget Names

Test these for validation:
- ✅ `MyWidget` - Valid
- ✅ `CustomButton` - Valid
- ✅ `User_Profile_Card` - Valid
- ❌ `mywidget` - Should fail (lowercase)
- ❌ `123Widget` - Should fail (starts with number)
- ❌ `Widget Name` - Should fail (spaces)

## Automated Testing Script

Create `test_e2e.sh`:

```bash
#!/bin/bash
set -e

echo "🧪 Running FigmaFlow-MCP Tests..."

echo "✅ Python unit tests..."
cd mcp-server
poetry run pytest

echo "✅ TypeScript compilation..."
cd ../vscode-extension
npm run compile

echo "✅ All tests passed!"
```

Make executable:
```bash
chmod +x test_e2e.sh
./test_e2e.sh
```

## Debugging

### Enable Debug Logging

In `.env`:
```bash
LOG_LEVEL=DEBUG
```

### VS Code Debug

In `vscode-extension`:
1. Set breakpoint in TypeScript code
2. Press F5
3. Trigger command
4. Debug in Extension Development Host

### Python Debug

```python
# Add to server.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Test Coverage

Generate coverage reports:

```bash
# Python
cd mcp-server
poetry run pytest --cov=src --cov-report=html
open htmlcov/index.html

# TypeScript (if configured)
cd vscode-extension
npm run coverage
```

## Reporting Issues

When reporting bugs, include:
1. Steps to reproduce
2. Expected vs actual behavior
3. Error messages
4. Environment (OS, Python version, Node version)
5. Figma URL used (if possible)
6. Generated code snippet

---

Happy testing! 🧪
