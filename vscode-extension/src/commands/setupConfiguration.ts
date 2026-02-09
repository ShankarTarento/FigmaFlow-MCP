/**
 * Setup Configuration Command
 * Opens the mcp-server/.env file for editing
 */
import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

export async function setupConfigurationCommand(context: vscode.ExtensionContext): Promise<void> {
    // Find the mcp-server/.env file
    const extensionPath = context.extensionPath;
    const projectRoot = path.dirname(extensionPath);
    const envPath = path.join(projectRoot, 'mcp-server', '.env');
    const examplePath = path.join(projectRoot, 'mcp-server', '.env.example');

    // Check if .env exists
    if (!fs.existsSync(envPath)) {
        const action = await vscode.window.showWarningMessage(
            '⚙️ Configuration file not found. Would you like to create it from the example?',
            'Create from Example',
            'Cancel'
        );

        if (action === 'Create from Example' && fs.existsSync(examplePath)) {
            fs.copyFileSync(examplePath, envPath);
            vscode.window.showInformationMessage('✓ Created .env file from example');
        } else {
            return;
        }
    }

    // Open the .env file for editing
    const doc = await vscode.workspace.openTextDocument(envPath);
    await vscode.window.showTextDocument(doc);

    await vscode.window.showInformationMessage(
        '💡 Edit the API keys in mcp-server/.env file.\n' +
        'Required: FIGMA_ACCESS_TOKEN, AI_API_KEY\n' +
        'Optional: AI_BASE_URL, AI_MODEL',
        'Got it'
    );

}

