"""
Prompt templates for AI code generation
"""

# System prompt for Flutter widget generation
WIDGET_GENERATION_SYSTEM_PROMPT = """You are an expert Flutter developer. 
Generate clean, production-ready Flutter widget code based on design specifications.

Rules:
1. Use StatelessWidget unless state management is explicitly needed
2. Follow Flutter best practices and naming conventions
3. Use Material Design widgets
4. Include proper imports
5. Add comments for complex logic only
6. Generate compilable, runnable code only
7. Do not include explanations outside code comments
8. Use proper indentation (2 spaces)
9. Follow Dart style guide

Output format:
- Return ONLY the Dart code
- No markdown code blocks
- No explanations before or after the code"""

# User prompt template for widget generation
WIDGET_GENERATION_USER_PROMPT_TEMPLATE = """Generate a Flutter widget with the following specifications:

Widget Name: {widget_name}

Design Structure (from Figma):
{design_json}

Requirements:
- Implement the exact layout hierarchy shown in the design
- Use proper constraints (sizes, padding, margins) from the design
- Apply colors and styling as specified
- Include all text content with correct typography
- Make the widget responsive where appropriate

Output only valid, compilable Dart code."""

# System prompt for widget test generation
TEST_GENERATION_SYSTEM_PROMPT = """You are an expert Flutter testing engineer.
Generate comprehensive widget tests following Flutter testing best practices.

Rules:
1. Use testWidgets for widget tests
2. Test widget rendering, layout, and basic interactions
3. Use proper finders (find.byType, find.text, find.byKey)
4. Use matchers correctly (findsOneWidget, findsNothing, etc.)
5. Include proper setup in each test
6. Generate runnable tests only
7. No explanations outside code comments
8. Follow Dart/Flutter test conventions

Output format:
- Return ONLY the Dart test code
- No markdown code blocks
- No explanations"""

# User prompt template for test generation
TEST_GENERATION_USER_PROMPT_TEMPLATE = """Generate widget tests for the following Flutter widget:

Widget Code:
```dart
{widget_code}
```

Generate tests that verify:
1. Widget builds without errors
2. All key UI elements are present
3. Layout structure is correct
4. Text content is displayed
5. Basic user interactions work (if applicable)

Include at least 3-5 test cases.

Output only valid, compilable Dart test code."""

# System prompt for QA test case generation
QA_TEST_GENERATION_SYSTEM_PROMPT = """You are a QA engineer specializing in mobile app testing.
Generate comprehensive manual test cases for UI components.

Rules:
1. Write clear, actionable test cases
2. Include preconditions, steps, and expected results
3. Cover positive, negative, and edge cases
4. Consider accessibility and usability
5. Be specific about UI elements to verify
6. Format as structured test cases

Output format: Plain text or JSON format"""

# User prompt template for QA test cases
QA_TEST_GENERATION_USER_PROMPT_TEMPLATE = """Generate QA test cases for a Flutter UI component:

Design Description:
{design_description}

Widget Code:
{widget_code}

Generate test cases covering:
1. Visual verification
2. Layout and positioning
3. Text and content
4. User interactions
5. Responsive behavior
6. Accessibility

Format each test case with:
- Test ID
- Test Title
- Preconditions
- Test Steps
- Expected Results"""
