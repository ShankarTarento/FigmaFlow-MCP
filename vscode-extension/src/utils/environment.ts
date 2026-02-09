/**
 * Environment utilities
 * Load and validate environment variables from mcp-server/.env
 */
import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import * as dotenv from 'dotenv';

export interface Environment {
    FIGMA_ACCESS_TOKEN?: string;
    AI_API_KEY?: string;
    AI_BASE_URL?: string;
    AI_MODEL?: string;
    AI_TEMPERATURE?: string;
    AI_MAX_TOKENS?: string;
    MCP_SERVER_PORT?: string;
    LOG_LEVEL?: string;
}

/**
 * Get path to mcp-server/.env file
 */
function getMcpServerEnvPath(context?: vscode.ExtensionContext): string {
    // Get extension path
    const extensionPath = context?.extensionPath || __dirname;

    // Extension is at: /path/to/FigmaFlow-MCP/vscode-extension
    // We need: /path/to/FigmaFlow-MCP/mcp-server/.env
    const projectRoot = path.dirname(extensionPath);
    return path.join(projectRoot, 'mcp-server', '.env');
}

export async function loadEnvironment(context?: vscode.ExtensionContext): Promise<Environment | null> {
    const envPath = getMcpServerEnvPath(context);

    // Check if mcp-server/.env exists
    if (!fs.existsSync(envPath)) {
        const action = await vscode.window.showErrorMessage(
            '🔑 Configuration not found. Please configure mcp-server/.env with your API keys.',
            'Open .env',
            'Show Instructions'
        );

        if (action === 'Open .env') {
            // Create .env from example if it doesn't exist
            const examplePath = path.join(path.dirname(envPath), '.env.example');
            if (fs.existsSync(examplePath) && !fs.existsSync(envPath)) {
                fs.copyFileSync(examplePath, envPath);
            }

            const doc = await vscode.workspace.openTextDocument(envPath);
            await vscode.window.showTextDocument(doc);
            vscode.window.showInformationMessage('💡 Please fill in your API keys in the .env file');
        } else if (action === 'Show Instructions') {
            const readmePath = path.join(path.dirname(envPath), 'LITELLM_SETUP.md');
            if (fs.existsSync(readmePath)) {
                const doc = await vscode.workspace.openTextDocument(readmePath);
                await vscode.window.showTextDocument(doc);
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

    // Note: These values are loaded for information purposes only
    // The MCP server loads its own .env file and doesn't use these
    return {
        FIGMA_ACCESS_TOKEN: process.env.FIGMA_ACCESS_TOKEN,
        AI_API_KEY: process.env.AI_API_KEY,
        AI_BASE_URL: process.env.AI_BASE_URL,
        AI_MODEL: process.env.AI_MODEL,
        AI_TEMPERATURE: process.env.AI_TEMPERATURE,
        AI_MAX_TOKENS: process.env.AI_MAX_TOKENS,
        MCP_SERVER_PORT: process.env.MCP_SERVER_PORT,
        LOG_LEVEL: process.env.LOG_LEVEL
    };
}
