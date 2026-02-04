/**
 * VS Code Extension Entry Point
 */
import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { generateWidgetCommand } from './commands/generateWidget';
import { generateTestsCommand } from './commands/generateTests';
import { setupConfigurationCommand } from './commands/setupConfiguration';

export function activate(context: vscode.ExtensionContext) {
    console.log('FigmaFlow MCP extension activated');

    // Check if .env exists on activation
    checkEnvironmentSetup();

    // Register commands
    const setupConfig = vscode.commands.registerCommand(
        'figmaflow.setupConfiguration',
        () => setupConfigurationCommand(context)
    );

    const generateWidget = vscode.commands.registerCommand(
        'figmaflow.generateWidget',
        () => generateWidgetCommand(context)
    );

    const generateTests = vscode.commands.registerCommand(
        'figmaflow.generateTests',
        () => generateTestsCommand(context)
    );

    context.subscriptions.push(setupConfig, generateWidget, generateTests);
}

export function deactivate() {
    console.log('FigmaFlow MCP extension deactivated');
}

async function checkEnvironmentSetup() {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) return;

    const envPath = path.join(workspaceFolder.uri.fsPath, '.env');

    // Check if .env exists
    if (!fs.existsSync(envPath)) {
        const action = await vscode.window.showInformationMessage(
            '🔑 FigmaFlow: No .env file found. Would you like to set up your API keys?',
            'Setup Now',
            'Later'
        );

        if (action === 'Setup Now') {
            vscode.commands.executeCommand('figmaflow.setupConfiguration');
        }
    }
}
