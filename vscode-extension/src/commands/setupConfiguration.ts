/**
 * Setup Configuration Command
 * Interactive wizard to configure API keys
 */
import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

export async function setupConfigurationCommand(context: vscode.ExtensionContext): Promise<void> {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) {
        vscode.window.showErrorMessage('Please open a workspace folder first');
        return;
    }

    const envPath = path.join(workspaceFolder.uri.fsPath, '.env');

    // Step 1: Get Figma Access Token
    const figmaToken = await vscode.window.showInputBox({
        prompt: '🎨 Enter your Figma Access Token',
        password: true,
        placeHolder: 'figd_...',
        ignoreFocusOut: true,
        validateInput: (value) => {
            if (!value) return 'Token is required';
            if (!value.startsWith('figd_')) {
                return 'Figma tokens typically start with "figd_"';
            }
            return null;
        }
    });

    if (!figmaToken) {
        vscode.window.showWarningMessage('Setup cancelled');
        return;
    }

    // Step 2: Get OpenAI API Key
    const openaiKey = await vscode.window.showInputBox({
        prompt: '🤖 Enter your OpenAI API Key',
        password: true,
        placeHolder: 'sk-...',
        ignoreFocusOut: true,
        validateInput: (value) => {
            if (!value) return 'API key is required';
            if (!value.startsWith('sk-')) {
                return 'OpenAI keys typically start with "sk-"';
            }
            return null;
        }
    });

    if (!openaiKey) {
        vscode.window.showWarningMessage('Setup cancelled');
        return;
    }

    // Step 3: Create .env file
    const envContent = `# FigmaFlow MCP Configuration
# DO NOT commit this file to version control!

# Get your Figma token from: https://www.figma.com/settings
FIGMA_ACCESS_TOKEN=${figmaToken}

# Get your OpenAI key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=${openaiKey}

# Optional: MCP Server Configuration
MCP_SERVER_PORT=3000
LOG_LEVEL=INFO
`;

    try {
        fs.writeFileSync(envPath, envContent);

        // Step 4: Update .gitignore
        const gitignorePath = path.join(workspaceFolder.uri.fsPath, '.gitignore');
        if (fs.existsSync(gitignorePath)) {
            const gitignoreContent = fs.readFileSync(gitignorePath, 'utf8');
            if (!gitignoreContent.includes('.env')) {
                fs.appendFileSync(gitignorePath, '\n# FigmaFlow MCP secrets\n.env\n');
            }
        } else {
            fs.writeFileSync(gitignorePath, '.env\n');
        }

        // Step 5: Show success message
        const action = await vscode.window.showInformationMessage(
            '✅ Configuration saved successfully!',
            'View .env',
            'Generate Widget'
        );

        if (action === 'View .env') {
            const doc = await vscode.workspace.openTextDocument(envPath);
            await vscode.window.showTextDocument(doc);
        } else if (action === 'Generate Widget') {
            vscode.commands.executeCommand('figmaflow.generateWidget');
        }

    } catch (error: any) {
        vscode.window.showErrorMessage(`Failed to create .env file: ${error.message}`);
    }
}
