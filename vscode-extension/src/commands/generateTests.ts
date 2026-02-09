/**
 * Generate Tests Command
 * Generate Flutter widget tests from Figma design
 */
import * as vscode from 'vscode';
import * as path from 'path';
import { MCPClient } from '../mcp/client';
import { loadEnvironment } from '../utils/environment';

export async function generateTestsCommand(context: vscode.ExtensionContext): Promise<void> {
    try {
        // Load environment from mcp-server/.env
        const env = await loadEnvironment(context);
        if (!env) return;

        // Get Figma URL
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

        // Get widget name for test file
        const widgetName = await vscode.window.showInputBox({
            prompt: 'Enter widget name being tested',
            placeHolder: 'MyCustomWidget'
        });

        if (!widgetName) return;

        await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: 'Generating widget tests...',
            cancellable: false
        }, async (progress) => {
            const mcpClient = new MCPClient();
            const serverPath = getServerPath(context);

            progress.report({ message: 'Connecting...', increment: 10 });
            await mcpClient.connect(serverPath);

            // Fetch design
            progress.report({ message: 'Fetching design...', increment: 20 });
            const designResult = await mcpClient.callTool('get_figma_design', {
                fileUrl: figmaUrl,
                accessToken: env.FIGMA_ACCESS_TOKEN
            });

            const designData = JSON.parse(designResult.content[0].text);

            if (designData.error) {
                throw new Error(designData.error);
            }

            // Generate widget first
            progress.report({ message: 'Generating widget...', increment: 30 });
            const widgetResult = await mcpClient.callTool('generate_flutter_widget', {
                designData: designData,
                widgetName: widgetName,
                options: { includeImports: true }
            });

            const widgetCode = widgetResult.content[0].text;

            // Check if widget generation returned an error
            try {
                const possibleError = JSON.parse(widgetCode);
                if (possibleError.error) {
                    throw new Error(possibleError.error);
                }
            } catch (parseError) {
                // Not JSON or doesn't have error property - this is expected for valid code
                if (parseError instanceof Error && parseError.message.startsWith('Failed to generate')) {
                    throw parseError;
                }
            }

            // Generate tests
            progress.report({ message: 'Generating tests...', increment: 30 });
            const testResult = await mcpClient.callTool('generate_widget_tests', {
                widgetCode: widgetCode,
                designData: designData
            });

            const testCode = testResult.content[0].text;

            // Check if test generation returned an error
            let isJsonError = false;
            try {
                const possibleError = JSON.parse(testCode);
                // If we can parse it as JSON, it's an error (valid code should be Dart, not JSON)
                if (possibleError.error) {
                    // JSON response with error property - this is definitely an error
                    isJsonError = true;
                    throw new Error(possibleError.error);
                }
                // Successfully parsed JSON without error property - still invalid
                isJsonError = true;
                throw new Error('Received unexpected JSON response instead of Flutter test code');
            } catch (parseError) {
                // If we marked it as JSON error, or if parsing succeeded, re-throw
                if (isJsonError || !(parseError instanceof SyntaxError)) {
                    throw parseError;
                }
                // Otherwise, JSON parse failed with SyntaxError - good! It's Dart code
            }
            progress.report({ increment: 10 });

            // Insert test code
            await insertTestCode(testCode, widgetName);

            await mcpClient.disconnect();
        });

        vscode.window.showInformationMessage(`✅ Tests for "${widgetName}" generated successfully!`);

    } catch (error: any) {
        vscode.window.showErrorMessage(`Failed to generate tests: ${error.message}`);
    }
}

function getServerPath(context: vscode.ExtensionContext): string {
    const config = vscode.workspace.getConfiguration('figmaflow');
    const customPath = config.get<string>('mcpServerPath');

    if (customPath) return customPath;

    // mcp-server is at project root, one level UP from vscode-extension
    const projectRoot = path.dirname(context.extensionPath);
    return path.join(projectRoot, 'mcp-server', 'src', 'mcp', 'server.py');
}

async function insertTestCode(testCode: string, widgetName: string): Promise<void> {
    const fileName = `${widgetName.toLowerCase()}_test.dart`;
    const doc = await vscode.workspace.openTextDocument({
        content: testCode,
        language: 'dart'
    });
    await vscode.window.showTextDocument(doc);

    // Suggest saving to test directory
    const action = await vscode.window.showInformationMessage(
        `Save as ${fileName}?`,
        'Save',
        'Cancel'
    );

    if (action === 'Save') {
        const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
        if (workspaceFolder) {
            const filePath = path.join(workspaceFolder.uri.fsPath, 'test', fileName);
            await vscode.window.showSaveDialog({
                defaultUri: vscode.Uri.file(filePath),
                filters: { 'Dart files': ['dart'] }
            });
        }
    }
}
