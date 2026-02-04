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
        // Create transport for MCP server
        this.transport = new StdioClientTransport({
            command: 'python',
            args: [serverPath],
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
