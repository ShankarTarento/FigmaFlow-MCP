/**
 * Generate Widget Command
 * Main command to generate Flutter widget from Figma design
 */
import * as vscode from 'vscode';
import * as path from 'path';
import { MCPClient } from '../mcp/client';
import { loadEnvironment } from '../utils/environment';

export async function generateWidgetCommand(context: vscode.ExtensionContext): Promise<void> {
    try {
        // Step 1: Load environment variables
        const env = await loadEnvironment();
        if (!env) return;

        // Step 2: Get Figma URL from user
        const figmaUrl = await vscode.window.showInputBox({
            prompt: 'Enter Figma file URL',
            placeHolder: 'https://www.figma.com/file/...',
            validateInput: (value) => {
                if (!value.includes('figma.com')) {
                    return 'Please enter a valid Figma URL';
                }
                return null;
            }
        });

        if (!figmaUrl) return;

        // Step 3: Get widget name
        const widgetName = await vscode.window.showInputBox({
            prompt: 'Enter widget name (PascalCase)',
            placeHolder: 'MyCustomWidget',
            validateInput: (value) => {
                if (!value) return 'Widget name is required';
                if (!/^[A-Z][a-zA-Z0-9]*$/.test(value)) {
                    return 'Widget name must be in PascalCase (e.g., MyWidget)';
                }
                return null;
            }
        });

        if (!widgetName) return;

        // Step 4: Show progress and generate widget
        await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: 'Generating Flutter widget...',
            cancellable: false
        }, async (progress) => {
            try {
                // Connect to MCP server
                const mcpClient = new MCPClient();
                const serverPath = getServerPath(context);

                progress.report({ message: 'Connecting to MCP server...', increment: 10 });
                await mcpClient.connect(serverPath);

                // Fetch design data from Figma
                progress.report({ message: 'Fetching Figma design...', increment: 30 });
                const designResult = await mcpClient.callTool('get_figma_design', {
                    fileUrl: figmaUrl,
                    accessToken: env.FIGMA_ACCESS_TOKEN
                });

                const designData = JSON.parse(designResult.content[0].text);

                // Check for errors
                if (designData.error) {
                    throw new Error(designData.error);
                }

                // Generate widget code
                progress.report({ message: 'Generating widget code...', increment: 40 });
                const widgetResult = await mcpClient.callTool('generate_flutter_widget', {
                    designData: designData,
                    widgetName: widgetName,
                    options: {
                        includeImports: true,
                        stateful: false
                    }
                });

                const widgetCode = widgetResult.content[0].text;
                progress.report({ message: 'Widget generated!', increment: 20 });

                // Insert code into editor
                await insertCodeIntoEditor(widgetCode, widgetName);

                // Cleanup
                await mcpClient.disconnect();

            } catch (error: any) {
                throw error;
            }
        });

        vscode.window.showInformationMessage(`✅ Widget "${widgetName}" generated successfully!`);

    } catch (error: any) {
        vscode.window.showErrorMessage(`Failed to generate widget: ${error.message}`);
    }
}

function getServerPath(context: vscode.ExtensionContext): string {
    // Get custom server path from settings or use bundled
    const config = vscode.workspace.getConfiguration('figmaflow');
    const customPath = config.get<string>('mcpServerPath');

    if (customPath) {
        return customPath;
    }

    // Default to workspace mcp-server
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (workspaceFolder) {
        return path.join(workspaceFolder.uri.fsPath, 'mcp-server', 'src', 'mcp', 'server.py');
    }

    // Fallback to bundled server
    return path.join(context.extensionPath, 'mcp-server', 'src', 'mcp', 'server.py');
}

async function insertCodeIntoEditor(code: string, widgetName: string): Promise<void> {
    const editor = vscode.window.activeTextEditor;

    if (editor && editor.document.languageId === 'dart') {
        // Insert at current cursor position
        await editor.edit(editBuilder => {
            editBuilder.insert(editor.selection.active, code);
        });
    } else {
        // Create new file
        const fileName = `${widgetName.toLowerCase()}.dart`;
        const doc = await vscode.workspace.openTextDocument({
            content: code,
            language: 'dart'
        });
        await vscode.window.showTextDocument(doc);

        // Suggest saving
        const action = await vscode.window.showInformationMessage(
            `Save as ${fileName}?`,
            'Save',
            'Cancel'
        );

        if (action === 'Save') {
            const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
            if (workspaceFolder) {
                const filePath = path.join(workspaceFolder.uri.fsPath, 'lib', fileName);
                await vscode.window.showSaveDialog({
                    defaultUri: vscode.Uri.file(filePath),
                    filters: {
                        'Dart files': ['dart']
                    }
                });
            }
        }
    }
}
