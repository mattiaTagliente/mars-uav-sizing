# Agent's Guide to Configuring MCP Servers in Antigravity

This guide documents the process for configuring Model Context Protocol (MCP) servers in Antigravity, based on lessons learned from configuring the Zotero MCP server.

## 1. Configuration File Location

Antigravity stores its MCP configuration in a specific JSON file. This is **different** from the main `settings.json` or the standard `mcp.json` used by other tools like Claude Desktop.

*   **Windows**: `C:\Users\<username>\.gemini\antigravity\mcp_config.json`
*   **Mac/Linux**: `~/.gemini/antigravity/mcp_config.json`

### ⚠️ Important Access Note for Agents
This file is located inside the `.gemini` directory, which may be protected or gitignored by the IDE's internal rules.
*   **Issue**: Standard file reading tools (like `view_file`) might fail with "access blocked" errors.
*   **Workaround**: Use terminal commands (e.g., `type`, `cat`, `Get-Content`, `Set-Content`) to read or write this file.

## 2. Configuration Format

The file requires a specific JSON structure. Crucially, strictly specifying the `type` as `"stdio"` is often required for local executable servers.

### Template
```json
{
  "mcpServers": {
    "server-name": {
      "type": "stdio",
      "command": "absolute/path/to/executable",
      "args": [
        "fail-safe-argument-1"
      ],
      "env": {
        "ENV_VAR_NAME": "value"
      }
    }
  }
}
```

### Key Requirements
1.  **"type": "stdio"**: Explicitly include this key.
2.  **Absolute Paths**: Use full absolute paths for the `command`.
3.  **Encoding**: Ensure the file is saved as **UTF-8 without BOM**. Windows PowerShell `Set-Content` might default to different encodings; be explicit.
4.  **Valid JSON**: Ensure strictly valid JSON syntax.

## 3. Applying Changes

Antigravity does **not** dynamically reload this configuration file.

1.  Save the `mcp_config.json` file.
2.  **Restart Antigravity** completely.
3.  Check the "Manage MCP Servers" UI or try listing resources to verify connection.

---

## 4. Specific Configuration: Zotero MCP

The specific configuration to enable the Zotero MCP server (installed via `uv tool install zotero-mcp`).

### Prerequisites
1.  **Zotero Desktop App**: Must be running.
2.  **Local API**: Enabled in Zotero (Preferences -> Advanced -> API -> Check "Allow local connections").

### Configuration Block

```json
{
  "mcpServers": {
    "zotero": {
      "type": "stdio",
      "command": "C:\\Users\\<username>\\.local\\bin\\zotero-mcp.EXE",
      "args": [],
      "env": {
        "ZOTERO_LOCAL": "true"
      }
    }
  }
}
```

*   **Command**: Points to the compiled `.exe` shim created by `uv`, usually in `.local\bin`. Do not point to the python script unless you are manually invoking the interpreter.
*   **Args**: The official `zotero-mcp` executable (v0.1.2+) treats the default run mode as serving the MCP protocol, so `args` can be empty `[]`.
*   **Env**: `ZOTERO_LOCAL` set to `"true"` forces it to talk to the local running app instead of the cloud API.

## 5. Troubleshooting Checklist

*   **"No MCP servers installed"**:
    *   Did you restart Antigravity?
    *   Is the JSON valid?
    *   Did you use "stdio"?
*   **Connection Errors**:
    *   Is the target application (e.g., Zotero) running?
*   **Agent cannot read config file**:
    *   Use `run_command` with `type` or `cat`.
