# UTCP Code Mode MCP Bridge

**Execute TypeScript code with direct tool access through MCP.**

An advanced MCP server that brings UTCP Code Mode to the MCP ecosystem, allowing you to execute TypeScript code with all registered tools available as native TypeScript functions.

## 🚀 Quick Start

Add this configuration to your MCP client (Claude Desktop, etc.):

```json
{
  "mcpServers": {
    "utcp-codemode": {
      "command": "npx",
      "args": ["@utcp/code-mode-mcp"],
      "env": {
        "UTCP_CONFIG_FILE": "/path/to/your/.utcp_config.json"
      }
    }
  }
}
```

**That's it!** No installation required. The bridge will automatically:
- Download and run the latest version via npx
- Load your UTCP configuration from the specified path
- Register all your UTCP manuals as tools available in TypeScript code
- Enable TypeScript code execution with hierarchical tool access (e.g., `manual.tool()`)

## 🔧 Configuration

Create a `.utcp_config.json` file to configure your tools and services.

### Local Configuration File

Create a `.utcp_config.json` file locally:

```json
{
    "load_variables_from": [
      {
        "variable_loader_type": "dotenv",
        "env_file_path": ".env"
      }
    ],
    "manual_call_templates": [
      {
          "name": "openlibrary",
          "call_template_type": "http",
          "http_method": "GET", 
          "url": "https://openlibrary.org/static/openapi.json",
          "content_type": "application/json"
      }
    ],
    "post_processing": [
      {
          "tool_post_processor_type": "filter_dict",
          "only_include_keys": ["name", "description"],
          "only_include_tools": ["openlibrary.*"]
      }
    ],
    "tool_repository": {
      "tool_repository_type": "in_memory"
    },
    "tool_search_strategy": {
      "tool_search_strategy_type": "tag_and_description_word_match"
    }
}
```

### Remote Configuration File

You can also use a remote JSON file hosted on any HTTP/HTTPS URL:

```json
{
  "mcpServers": {
    "utcp-codemode": {
      "command": "npx",
      "args": ["@utcp/code-mode-mcp"],
      "env": {
        "UTCP_CONFIG_FILE": "https://example.com/my-utcp-config.json"
      }
    }
  }
}
```

The MCP bridge will automatically detect if `UTCP_CONFIG_FILE` is a URL (starts with `http://` or `https://`) and fetch the configuration remotely. This is useful for:
- **Shared team configurations** - Host a single config that multiple team members can use
- **Dynamic configurations** - Update tools without distributing new config files
- **Centralized management** - Manage multiple MCP instances from a central location

**Security Note:** Only use remote URLs from trusted sources, as the configuration can execute code and access your environment variables.

### Enabling CLI Support

**Important:** CLI protocol support is **disabled by default** for security reasons. To enable CLI tool execution, you need to explicitly register the CLI plugin in 'index.ts'.

```typescript
import { register as registerCli } from "@utcp/cli";

// Enable CLI support
registerCli();
```

**Security Note:** Only enable CLI if you trust the code that will be executed, as CLI tools can execute arbitrary commands on your system.

## 🛠️ Available MCP Tools

The bridge exposes these MCP tools for managing your UTCP Code Mode ecosystem:

- **`register_manual`** - Register new UTCP manuals/APIs
- **`deregister_manual`** - Remove registered manuals
- **`search_tools`** - Find tools by description with TypeScript interfaces
- **`list_tools`** - List all registered tool names
- **`get_required_keys_for_tool`** - Get required environment variables
- **`tool_info`** - Get complete tool information with TypeScript interface
- **`call_tool_chain`** - Execute TypeScript code with direct tool access

## 📁 What is UTCP?

The Universal Tool Calling Protocol (UTCP) allows you to:
- **Connect to any API** via HTTP, OpenAPI specs, or custom formats
- **Use command-line tools** with automatic argument parsing (requires explicit CLI plugin registration)
- **Process text and files** with built-in utilities
- **Chain and combine** multiple tools seamlessly

With this MCP bridge, all your UTCP tools become available in Claude Desktop and other MCP clients.
 
**Optional Protocols:** CLI requires explicit registration for security (see "Enabling CLI Support" above).

## 💻 Code Mode Example

The main feature of this bridge is the ability to execute TypeScript code with direct access to all registered tools:

```typescript
// Example using call_tool_chain
const result = await call_tool_chain(`
  // Get user data from an API
  const user = await user_service.getUserProfile({ userId: "123" });
  console.log('User data:', user);
  
  // Process the data with another tool
  const processed = await data_processor.analyzeUserBehavior({
    userData: user,
    timeframe: "30days"
  });
  
  // Generate a report
  const report = await reporting.generateInsights({
    analysis: processed,
    format: "summary"
  });
  
  return {
    userId: user.id,
    totalActions: processed.actionCount,
    topInsight: report.insights[0]
  };
`);
```

**Key Benefits:**
- **Hierarchical Access**: Use `manual.tool()` syntax to avoid naming conflicts
- **Type Safety**: Get TypeScript interfaces for all tools via `search_tools` or `tool_info`
- **Code Execution**: Chain multiple tool calls in a single code block
- **Error Handling**: Proper error handling with timeout support

## 🌟 Features

- ✅ **Zero installation** - Works via npx
- ✅ **Universal compatibility** - Works with any MCP client
- ✅ **Dynamic configuration** - Update tools without restarting
- ✅ **Environment isolation** - Each project can have its own config
- ✅ **Comprehensive tool management** - Register, search, call, and inspect tools

---

<img width="2263" height="976" alt="UTCP MCP Bridge Interface" src="https://github.com/user-attachments/assets/a6759512-1c0d-4265-9518-64916fbe1428" />
