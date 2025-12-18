# Repository Setup Instructions

## Current Status

✅ Repository cloned to: `e:\Unity\3rdPartyProjects\UnityMCPExtraTools`
✅ Forked on GitHub: `https://github.com/FoePawStudios/unity-mcp-extra-tools`
✅ Origin remote configured: `FoePawStudios/unity-mcp-extra-tools`
✅ Upstream remote configured: `CoplayDev/unity-mcp`
✅ Feature branch created: `feature/simplified-tools`

## Setup Complete! 🎉

Your repository is fully configured and ready for development. You can now start implementing the simplified tools on the `feature/simplified-tools` branch.

---

## Setting Up the Simplified Tools Branch for Use

If you want to use the simplified tools in your Unity project, follow these steps:

### Step 1: Install Unity Package from Fork

1. Open your Unity project.
2. Go to `Window > Package Manager`.
3. Click `+` -> `Add package from git URL...`.
4. Enter your fork's URL with the feature branch:
   ```
   https://github.com/FoePawStudios/unity-mcp-extra-tools.git?path=/MCPForUnity#feature/simplified-tools
   ```
5. Click `Add`.

**Note:** The `#feature/simplified-tools` at the end tells Unity Package Manager to use that branch instead of the default `main` branch.

### Step 2: Configure Server Source in Unity

1. In Unity, go to `Window > MCP for Unity`.
2. Go to the **Settings** section (if not visible, it may be collapsed).
3. Expand **Advanced Settings**.
4. Find the **Server Path/URL** field under **Server Source Override**.
5. Enter your fork's Git URL with the feature branch and Server subdirectory:
   ```
   git+https://github.com/FoePawStudios/unity-mcp-extra-tools@feature/simplified-tools#subdirectory=Server
   ```
6. The Unity window will update to show the command that will be used to launch the server.

**Verification:** Check that the command shown in the **Connection** section includes your fork URL and branch:
```
uvx --from git+https://github.com/FoePawStudios/unity-mcp-extra-tools@feature/simplified-tools#subdirectory=Server mcp-for-unity --transport ...
```

### Step 3: Switch to Stdio Transport (Recommended)

**Why Stdio?** The simplified tools work best with stdio transport. HTTP transport has known issues with FastMCP session management that can prevent tools from appearing in Cursor.

1. In Unity, go to `Window > MCP for Unity`.
2. In the **Connection** section, find the **Transport** dropdown.
3. Change it from `HTTP` to `Stdio`.
4. Note the **Unity Socket Port** (default is usually 6400).

### Step 4: Configure Cursor MCP Client

1. Open Cursor's MCP configuration file. The location depends on your OS:
   - **Windows:** `%APPDATA%\Cursor\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json`
   - **macOS:** `~/Library/Application Support/Cursor/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
   - **Linux:** `~/.config/Cursor/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`

2. Add or update the `unityMCP` server configuration to use stdio:

```json
{
  "mcpServers": {
    "unityMCP": {
      "command": "C:\\Users\\YOUR_USERNAME\\.local\\bin\\uvx.exe",
      "args": [
        "--from",
        "git+https://github.com/FoePawStudios/unity-mcp-extra-tools@feature/simplified-tools#subdirectory=Server",
        "mcp-for-unity",
        "--transport",
        "stdio"
      ]
    }
  }
}
```

**Important:**
- Replace `YOUR_USERNAME` with your actual Windows username.
- Replace `uvx.exe` path with your actual `uvx` installation path (Unity may show this in the connection section).
- Replace the GitHub URL with your fork if different.

**Alternative:** If Unity shows the exact command in the Connection section, you can copy that command and convert it to the Cursor config format.

3. Save the configuration file.
4. **Restart Cursor** for the changes to take effect.

### Step 5: Verify Setup

1. **Start Unity** (if not already running).
2. In Unity, go to `Window > MCP for Unity`.
3. Click **Start Session** (or the connection button - it should start automatically with stdio).
4. **Restart Cursor** (if you haven't already).
5. In Cursor, check that the MCP server is connected. You should see:
   - Connection status indicating the server is running
   - All tools available (should be 50 tools total: 23 original + 27 new simplified tools)

**Verify Tools:** You can verify the new simplified tools are available by checking for tools like:
- `create_gameobject`
- `find_gameobject`
- `modify_gameobject`
- `delete_gameobject`
- `add_component`
- `remove_component`
- `create_prefab`
- `create_scene`
- `set_play_mode`
- And 18 more!

### Troubleshooting

**Tools not appearing?**
- Make sure you've set the **Server Path/URL** override in Unity's Advanced Settings.
- Verify the Git URL includes `@feature/simplified-tools#subdirectory=Server`.
- Check Unity's console for any errors when starting the server.
- Try clearing Unity's package cache and reinstalling the package.

**Connection issues?**
- Ensure Unity is running and the session is started.
- Check that the Unity Socket Port matches (default 6400).
- Verify `uvx` is installed and accessible: `uvx --version`
- Check Cursor's MCP logs for connection errors.

**Still having issues?**
- Check the server terminal output in Unity for any error messages.
- Verify the fork's `feature/simplified-tools` branch has all the tool files committed.
- Try using the local path instead of Git URL (browse to your local `Server` folder).

---

## Remote Configuration

Current remotes:
- `origin` → Your fork: `https://github.com/FoePawStudios/unity-mcp-extra-tools.git`
- `upstream` → Original repo: `https://github.com/CoplayDev/unity-mcp.git`

Verify remotes:
```bash
git remote -v
```

---

## Development Workflow

### Start Development

You're now ready to implement the simplified tools! The feature branch `feature/simplified-tools` is ready for your changes.

### Sync with Upstream (When Needed)

When the main repository releases updates:

```bash
# Fetch latest from upstream
git fetch upstream

# Switch to main branch
git checkout main

# Merge upstream changes
git merge upstream/main

# Switch back to feature branch
git checkout feature/simplified-tools

# Rebase on updated main
git rebase main

# Resolve any conflicts if they occur
# Test your tools still work
```

## Quick Reference

**Current remotes:**
- `origin`: Your fork (update URL after forking)
- `upstream`: Original repository (CoplayDev/unity-mcp)

**Current branch:** `feature/simplified-tools`

**Repository location:** `e:\Unity\3rdPartyProjects\UnityMCPExtraTools`

