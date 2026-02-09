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

    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('figmaflow.generateWidget', async () => {
            await generateWidgetCommand(context);  // Pass context
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('figmaflow.generateTests', async () => {
            await generateTestsCommand(context);  // Pass context
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('figmaflow.setupConfiguration', async () => {
            await setupConfigurationCommand(context);
        })
    );

    // Show welcome message on first activation
    const hasShownWelcome = context.globalState.get('hasShownWelcome');
    if (!hasShownWelcome) {
        vscode.window.showInformationMessage(
            '🎨 FigmaFlow MCP is ready! Configure mcp-server/.env to get started.',
            'Open Config',
            'View Docs'
        ).then(action => {
            if (action === 'Open Config') {
                vscode.commands.executeCommand('figmaflow.setupConfiguration');
            } else if (action === 'View Docs') {
                vscode.env.openExternal(vscode.Uri.parse('https://github.com/your-repo/FigmaFlow-MCP'));
            }
        });
        context.globalState.update('hasShownWelcome', true);
    }
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
