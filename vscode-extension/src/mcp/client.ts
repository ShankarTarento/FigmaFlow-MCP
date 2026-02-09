/**
 * MCP Client for communicating with the MCP server
 */
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';

export interface MCPToolResult {
    content: Array<{
        type: string;
        text: string;
    }>;
}

export class MCPClient {
    private client: Client | null = null;
    private transport: StdioClientTransport | null = null;

    async connect(serverPath: string): Promise<void> {
        // Extract directory from server path for poetry to find pyproject.toml
        const path = require('path');
        const serverDir = path.dirname(path.dirname(path.dirname(serverPath))); // Go up to mcp-server root

        // Create transport for MCP server
        // Use shell wrapper for more reliable execution
        const runScript = path.join(serverDir, 'run_server.sh');
        this.transport = new StdioClientTransport({
            command: runScript,
            args: []
        });

        // Create client
        this.client = new Client({
            name: 'figmaflow-vscode',
            version: '1.0.0',
        }, {
            capabilities: {}
        });

        // Connect to server
        await this.client.connect(this.transport);
    }

    async callTool(
        name: string,
        args: Record<string, any>
    ): Promise<MCPToolResult> {
        if (!this.client) {
            throw new Error('MCP client not connected. Call connect() first.');
        }

        const result = await this.client.callTool({
            name,
            arguments: args,
        });

        return result as MCPToolResult;
    }

    async disconnect(): Promise<void> {
        if (this.client) {
            await this.client.close();
            this.client = null;
            this.transport = null;
        }
    }

    isConnected(): boolean {
        return this.client !== null;
    }
}
