# User Guide - FigmaFlow MCP

Complete user guide for using FigmaFlow to generate Flutter code from Figma designs.

## What is FigmaFlow?

FigmaFlow is a VS Code extension that converts Figma designs into Flutter widgets and tests using AI. It's powered by the Model Context Protocol (MCP) and works seamlessly with GitHub Copilot.

**Key Features:**
- 🎨 Generate Flutter widgets from Figma designs
- 🧪 Auto-generate widget tests
- 🔑 Easy configuration
- 🤖 AI-powered code generation
- 🐧 Linux-first, works everywhere

## Getting Started

### 1. Installation

**Prerequisites:**
- VS Code 1.85 or later
- Figma account ([sign up free](https://www.figma.com))
- OpenAI account ([sign up](https://platform.openai.com/signup))

**Install Extension:**
1. Open VS Code
2. Go to Extensions (Cmd+Shift+X)
3. Search for "FigmaFlow MCP"
4. Click Install

Or install from VSIX:
```bash
code --install-extension figmaflow-mcp-0.1.0.vsix
```

### 2. Get API Keys

#### Figma Access Token

1. Go to [Figma Settings](https://www.figma.com/settings)
2. Scroll to **Personal Access Tokens**
3. Click **Generate new token**
4. Name it (e.g., "FigmaFlow")
5. Copy the token (starts with `figd_`)

#### OpenAI API Key

1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Click **Create new secret key**
3. Name it (e.g., "FigmaFlow")
4. Copy the key (starts with `sk-`)

### 3. Configure FigmaFlow

**First-Time Setup:**
1. Open your Flutter project in VS Code
2. Press `Cmd+Shift+P` (or `Ctrl+Shift+P` on Windows/Linux)
3. Type: **FigmaFlow: Setup API Keys**
4. Enter your Figma token when prompted
5. Enter your OpenAI key when prompted

Done! A `.env` file is created in your workspace with your keys (automatically added to `.gitignore`).

## Using FigmaFlow

### Generate a Flutter Widget

**Step 1: Prepare Your Figma Design**

1. Open your Figma file
2. Select the frame/component you want to convert
3. Copy the URL from your browser

The URL should look like:
```
https://www.figma.com/file/ABC123/MyDesign?node-id=1-2
```

**Step 2: Generate Widget**

1. In VS Code, press `Cmd+Shift+P`
2. Type: **FigmaFlow: Generate Flutter Widget from Figma**
3. Paste your Figma URL
4. Enter a widget name (e.g., `LoginButton`)
   - Must be PascalCase (e.g., `MyWidget`, not `mywidget`)
5. Wait for generation (usually 10-20 seconds)

**Step 3: Review Generated Code**

The generated widget code will appear in your editor:

```dart
import 'package:flutter/material.dart';

class LoginButton extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      // Generated layout based on your Figma design
      ...
    );
  }
}
```

**Step 4: Save or Insert**

- If you have a Dart file open, the code is inserted at cursor
- Otherwise, a new file is created - save it to `lib/` folder

### Generate Widget Tests

**Step 1: Generate Tests**

1. Press `Cmd+Shift+P`
2. Type: **FigmaFlow: Generate Widget Tests from Figma**
3. Enter the same Figma URL
4. Enter the widget name being tested

**Step 2: Review Tests**

Generated test file includes:

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter/material.dart';

void main() {
  testWidgets('LoginButton renders correctly', (tester) async {
    await tester.pumpWidget(
      MaterialApp(home: LoginButton()),
    );
    
    expect(find.byType(Container), findsOneWidget);
    // Additional tests...
  });
}
```

**Step 3: Save Tests**

Save the test file to your `test/` directory (e.g., `test/login_button_test.dart`).

**Step 4: Run Tests**

```bash
flutter test test/login_button_test.dart
```

## Tips & Best Practices

### Design Guidelines

**For Best Results:**

1. **Use Frames** - Organize your design in frames
2. **Name Layers** - Use descriptive names (e.g., "Title Text", "Submit Button")
3. **Group Elements** - Group related elements in frames
4. **Use Components** - Figma components → reusable widgets
5. **Set Constraints** - Use Auto Layout for responsive designs

**Example Good Structure:**
```
LoginScreen (Frame)
├── Header (Frame)
│   └── Title (Text)
├── Form (Frame)
│   ├── EmailInput (Component)
│   └── PasswordInput (Component)
└── Actions (Frame)
    ├── LoginButton (Component)
    └── ForgotLink (Text)
```

### Widget Naming

**Valid Names:**
- ✅ `MyWidget`
- ✅ `LoginButton`
- ✅ `UserProfileCard`
- ✅ `Home_Screen` (underscores ok)

**Invalid Names:**
- ❌ `mywidget` (must start with uppercase)
- ❌ `123Widget` (can't start with number)
- ❌ `My Widget` (no spaces)

### Code Refinement

**Use GitHub Copilot:**

After generation, use Copilot to refine:
- Add interactivity: "Add onPressed callback"
- Add state: "Convert to StatefulWidget"
- Customize styling: "Make button rounded with shadow"
- Add animations: "Add fade-in animation"

**Manual Edits:**

Common edits you might make:
- Add custom colors from your theme
- Connect to state management
- Add error handling
- Implement callbacks

## Common Workflows

### Workflow 1: New Screen

1. Design screen in Figma
2. Generate widget: `FigmaFlow: Generate Flutter Widget`
3. Save to `lib/screens/my_screen.dart`
4. Generate tests: `FigmaFlow: Generate Widget Tests`
5. Save to `test/my_screen_test.dart`
6. Import and use in your app
7. Run tests: `flutter test`

### Workflow 2: Component Library

1. Design all components in one Figma file
2. Generate each component separately
3. Save to `lib/components/` folder
4. Create barrel file: `lib/components/components.dart`
5. Generate tests for each
6. Use throughout your app

### Workflow 3: Iterative Design

1. Generate initial widget
2. Review in app
3. Update design in Figma
4. Regenerate widget
5. Compare using git diff
6. Merge desired changes

## Troubleshooting

### Issue: "FIGMA_ACCESS_TOKEN not found"

**Solution:**
1. Run `FigmaFlow: Setup API Keys` again
2. Check `.env` file exists in workspace root
3. Verify token format (should start with `figd_`)

### Issue: "Invalid Figma URL"

**Solution:**
- URL must contain `/file/`
- Example: `https://www.figma.com/file/ABC123/Design`
- Include `?node-id=X-Y` to select specific frame

### Issue: "OpenAI API error: insufficient credits"

**Solution:**
1. Check your OpenAI balance: https://platform.openai.com/usage
2. Add payment method if needed
3. Consider using a different model in `.env`:
   ```
   AI_MODEL=gpt-4  # or gpt-3.5-turbo for lower cost
   ```

### Issue: Generated code doesn't compile

**Solution:**
1. Check import statements are correct
2. Run `flutter pub get` to ensure dependencies
3. Use GitHub Copilot to fix syntax errors
4. Report issue with your Figma URL for improvement

### Issue: Widget doesn't match design exactly

**Remember:** AI does its best approximation. You may need to:
- Adjust colors manually
- Fine-tune spacing
- Add custom styling
- Implement interactions

## Configuration Options

Edit `.env` in your workspace to customize:

```bash
# Required
FIGMA_ACCESS_TOKEN=figd_xxx
OPENAI_API_KEY=sk-xxx

# Optional
AI_MODEL=gpt-4o              # AI model to use
AI_TEMPERATURE=0.3           # Creativity (0.0-2.0)
AI_MAX_TOKENS=2000          # Response length
LOG_LEVEL=INFO              # Logging detail
```

## Keyboard Shortcuts

Add custom shortcuts in VS Code:

1. `Cmd+K Cmd+S` to open Keyboard Shortcuts
2. Search for "FigmaFlow"
3. Add your preferred shortcuts

Example:
- `Cmd+Shift+F G` - Generate Widget
- `Cmd+Shift+F T` - Generate Tests
- `Cmd+Shift+F S` - Setup API Keys

## Need Help?

- 📖 [Setup Guide](SETUP.md)
- 🧪 [Testing Guide](TESTING.md)
- 🐛 [Report an Issue](https://github.com/yourusername/figmaflow-mcp/issues)
- 💬 [Discussions](https://github.com/yourusername/figmaflow-mcp/discussions)

---

**Happy coding with FigmaFlow!** 🎨→💙
