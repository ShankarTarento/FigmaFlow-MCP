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
        // Step 1: Load environment variables from mcp-server/.env
        const env = await loadEnvironment(context);
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

                // Parse response with error handling
                let designData;
                const responseText = designResult.content[0]?.text || '';
                try {
                    designData = JSON.parse(responseText);
                } catch (parseError) {
                    // Show the actual response that failed to parse
                    throw new Error(`Failed to parse Figma response: ${responseText.substring(0, 200)}`);
                }

                // Check for errors
                if (designData.error) {
                    throw new Error(designData.error);
                }

                // Generate widget code
                progress.report({ message: 'Generating widget code...', increment: 40 });
                const widgetResult = await mcpClient.callTool('generate_flutter_widget', {
                    designData: designData,
                    widgetName: widgetName,
                    // Use AI_API_KEY if available (for LiteLLM), fallback to OPENAI_API_KEY
                    openaiApiKey: env.AI_API_KEY || env.OPENAI_API_KEY,
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
    // Get custom server path from settings if configured
    const config = vscode.workspace.getConfiguration('figmaflow');
    const customPath = config.get<string>('mcpServerPath');

    if (customPath) {
        return customPath;
    }

    // mcp-server is at project root, one level UP from vscode-extension
    // extensionPath = /path/to/FigmaFlow-MCP/vscode-extension
    // we need = /path/to/FigmaFlow-MCP/mcp-server/src/mcp/server.py
    const projectRoot = path.dirname(context.extensionPath);
    return path.join(projectRoot, 'mcp-server', 'src', 'mcp', 'server.py');
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
