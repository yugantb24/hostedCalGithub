# Calculator MCP Server

A minimal [Model Context Protocol](https://modelcontextprotocol.io) (MCP) server built with
[FastMCP](https://gofastmcp.com), exposing basic arithmetic as tools that any MCP-compatible
client (Claude Desktop, Claude Code, Cursor, etc.) can call.

## Tools

| Tool          | Description                                  |
|---------------|-----------------------------------------------|
| `add`         | Add two numbers                                |
| `subtract`    | Subtract b from a                              |
| `multiply`    | Multiply two numbers                           |
| `divide`      | Divide a by b (errors on divide-by-zero)       |
| `power`       | Raise base to an exponent                      |
| `square_root` | Square root of a number                        |
| `modulo`      | Remainder of a divided by b                    |
| `calculate`   | Evaluate a full expression, e.g. `2 + 3 * (4-1)` |

## 1. Run it locally

```bash
git clone https://github.com/<your-username>/calculator-mcp-server.git
cd calculator-mcp-server
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python server.py               # stdio transport (default)
```

You can also test it interactively without any client using the FastMCP CLI:

```bash
fastmcp dev server.py
```

This opens the MCP Inspector in your browser so you can call each tool by hand.

## 2. Push it to GitHub

```bash
cd calculator-mcp-server
git init
git add .
git commit -m "Initial commit: calculator MCP server"
git branch -M main
git remote add origin https://github.com/<your-username>/calculator-mcp-server.git
git push -u origin main
```

(Create the empty repo on GitHub first — github.com → **New repository** — then use the URL
it gives you in the `git remote add` command above.)

## 3. Connect it to an MCP client

### Claude Desktop (runs the server locally via stdio)

Edit Claude Desktop's config file:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Add an entry pointing at your cloned repo:

```json
{
  "mcpServers": {
    "calculator": {
      "command": "python",
      "args": ["/absolute/path/to/calculator-mcp-server/server.py"]
    }
  }
}
```

Restart Claude Desktop. The calculator tools will appear in the tool picker.

### Claude Code

```bash
claude mcp add calculator -- python /absolute/path/to/calculator-mcp-server/server.py
```

## 4. Host it remotely (optional)

If you want a hosted server that clients reach over HTTP instead of running the script
locally, run it with the `--http` flag:

```bash
python server.py --http --host 0.0.0.0 --port 8000
```

This starts an MCP-over-HTTP endpoint at `http://<host>:8000/mcp`. Any always-on Python
host works — a few common options:

**Render.com (free tier available)**
1. Push this repo to GitHub (step 2 above).
2. On [render.com](https://render.com) → **New** → **Web Service** → connect your GitHub repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `python server.py --http --host 0.0.0.0 --port $PORT`
5. Deploy. Render gives you a public URL like `https://calculator-mcp.onrender.com`.
6. Your MCP endpoint is `https://calculator-mcp.onrender.com/mcp`.

**Fly.io / Railway / a VPS**
Same idea: install requirements, run `python server.py --http --port <PORT>`, expose the port.

Once hosted, point a remote-capable MCP client at `https://<your-domain>/mcp` instead of a
local `command`/`args` pair (check your client's docs for its remote-server config format).

## Notes

- The `calculate` tool only evaluates arithmetic on numeric literals (no names or function
  calls are allowed), so it's safe to expose even though it uses `eval` under the hood.
- To add more tools, just write a new function in `server.py` and decorate it with `@mcp.tool`.
