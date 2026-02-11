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

        // Debug: Log what we loaded (without exposing full keys)
        console.log('[FigmaFlow] Environment loaded:', {
            hasApiKey: !!env.AI_API_KEY,
            hasBaseUrl: !!env.AI_BASE_URL,
            hasModel: !!env.AI_MODEL,
            baseUrl: env.AI_BASE_URL,
            model: env.AI_MODEL
        });

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

                // Fetch design from Figma
                progress.report({ message: 'Fetching Figma design...', increment: 30 });

                console.log('[FigmaFlow] STEP 1: Fetching Figma design');
                console.log('[FigmaFlow] URL:', figmaUrl);
                console.log('[FigmaFlow] Token present:', !!env.FIGMA_ACCESS_TOKEN);

                const designResult = await mcpClient.callTool('get_figma_design', {
                    fileUrl: figmaUrl,
                    accessToken: env.FIGMA_ACCESS_TOKEN
                });

                console.log('[FigmaFlow] STEP 2: Figma design fetched');
                console.log('[FigmaFlow] Design result type:', typeof designResult);
                console.log('[FigmaFlow] Design result:', JSON.stringify(designResult).substring(0, 200));

                // Parse response with error handling
                let designData;
                const responseText = designResult.content[0]?.text || '';
                console.log('[FigmaFlow] Response text length:', responseText.length);

                try {
                    designData = JSON.parse(responseText);
                    console.log('[FigmaFlow] Parsed design data successfully');
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

                console.log('[FigmaFlow] STEP 3: Calling generate_flutter_widget tool');
                console.log('[FigmaFlow] Widget name:', widgetName);
                console.log('[FigmaFlow] Design data type:', typeof designData);
                console.log('[FigmaFlow] Design data keys:', Object.keys(designData).slice(0, 5));

                // Don't pass AI config - let MCP server use its own .env file
                // The server runs as a separate process and loads /mcp-server/.env
                console.log('[FigmaFlow] STEP 4: Preparing tool call arguments');
                const toolArgs = {
                    designData: designData,
                    widgetName: widgetName,
                    options: {
                        includeImports: true,
                        stateful: false
                    }
                };
                console.log('[FigmaFlow] Tool args prepared, type:', typeof toolArgs);
                console.log('[FigmaFlow] Tool args keys:', Object.keys(toolArgs));

                console.log('[FigmaFlow] STEP 5: Calling MCP client...');
                const widgetResult = await mcpClient.callTool('generate_flutter_widget', toolArgs);

                console.log('[FigmaFlow] STEP 6: Tool call returned');
                console.log('[FigmaFlow] Result type:', typeof widgetResult);
                console.log('[FigmaFlow] Result keys:', widgetResult ? Object.keys(widgetResult) : 'null');
                console.log('[FigmaFlow] Result:', JSON.stringify(widgetResult).substring(0, 200));

                // Validate response structure
                if (typeof widgetResult === 'string') {
                    const strResult = widgetResult as string;
                    throw new Error(`MCP server returned invalid response format (string): ${strResult.substring(0, 200)}`);
                }

                console.log('[FigmaFlow] STEP 7: Checking result.content');
                if (!widgetResult.content || !Array.isArray(widgetResult.content) || widgetResult.content.length === 0) {
                    throw new Error(`MCP server returned invalid response structure: ${JSON.stringify(widgetResult).substring(0, 200)}`);
                }

                console.log('[FigmaFlow] STEP 8: Extracting widget code');
                console.log('[FigmaFlow] content[0] type:', typeof widgetResult.content[0]);
                const widgetCode = widgetResult.content[0].text;

                // Debug: Log what we received
                console.log('[FigmaFlow] Widget code received:', {
                    length: widgetCode.length,
                    lines: widgetCode.split('\n').length,
                    firstLine: widgetCode.split('\n')[0],
                    lastLine: widgetCode.split('\n').slice(-1)[0]
                });

                // Check if the response is an error JSON
                let isJsonError = false;
                try {
                    const possibleError = JSON.parse(widgetCode);
                    // If we can parse it as JSON, it's an error (valid code should be Dart, not JSON)
                    if (possibleError.error) {
                        // JSON response with error property - this is definitely an error
                        isJsonError = true;
                        throw new Error(possibleError.error);
                    }
                    // Successfully parsed JSON without error property - still invalid
                    isJsonError = true;
                    throw new Error('Received unexpected JSON response instead of Flutter code');
                } catch (parseError) {
                    // If we marked it as JSON error, or if parsing succeeded, re-throw
                    if (isJsonError || !(parseError instanceof SyntaxError)) {
                        throw parseError;
                    }
                    // Otherwise, JSON parse failed with SyntaxError - good! It's Dart code
                }

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
    // Debug: Log insertion details
    console.log('[FigmaFlow] Inserting code:', {
        codeLength: code.length,
        codeLines: code.split('\n').length,
        widgetName: widgetName,
        firstChars: code.substring(0, 100)
    });

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
