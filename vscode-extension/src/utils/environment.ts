/**
 * Environment utilities
 * Load and validate environment variables
 */
import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import * as dotenv from 'dotenv';

export interface Environment {
    FIGMA_ACCESS_TOKEN: string;
    OPENAI_API_KEY: string;
    MCP_SERVER_PORT?: string;
    LOG_LEVEL?: string;
}

export async function loadEnvironment(): Promise<Environment | null> {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) {
        vscode.window.showErrorMessage('Please open a workspace folder');
        return null;
    }

    const envPath = path.join(workspaceFolder.uri.fsPath, '.env');

    // Check if .env exists
    if (!fs.existsSync(envPath)) {
        const action = await vscode.window.showErrorMessage(
            '🔑 No .env file found. Please configure your API keys.',
            'Configure Now'
        );

        if (action === 'Configure Now') {
            await vscode.commands.executeCommand('figmaflow.setupConfiguration');
            // Try loading again
            if (fs.existsSync(envPath)) {
                return loadEnvironmentFile(envPath);
            }
        }

        return null;
    }

    return loadEnvironmentFile(envPath);
}

function loadEnvironmentFile(envPath: string): Environment | null {
    // Load .env file
    const result = dotenv.config({ path: envPath });

    if (result.error) {
        vscode.window.showErrorMessage(`Failed to load .env: ${result.error.message}`);
        return null;
    }

    // Validate required variables
    const figmaToken = process.env.FIGMA_ACCESS_TOKEN;
    const openaiKey = process.env.OPENAI_API_KEY;

    if (!figmaToken) {
        vscode.window.showErrorMessage('FIGMA_ACCESS_TOKEN not found in .env file');
        return null;
    }

    if (!openaiKey) {
        vscode.window.showErrorMessage('OPENAI_API_KEY not found in .env file');
        return null;
    }

    return {
        FIGMA_ACCESS_TOKEN: figmaToken,
        OPENAI_API_KEY: openaiKey,
        MCP_SERVER_PORT: process.env.MCP_SERVER_PORT,
        LOG_LEVEL: process.env.LOG_LEVEL
    };
}
