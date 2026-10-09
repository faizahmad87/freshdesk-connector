import argparse

from app.mcp.server import mcp

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Freshdesk MCP Connector")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="Transport mode: stdio (MCP Inspector / Claude Desktop) or sse (HTTP server)",
    )
    parser.add_argument("--host", default="0.0.0.0", help="Host for SSE mode (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="Port for SSE mode (default: 8000)")

    args = parser.parse_args()

    if args.transport == "sse":
        print(f"Starting Freshdesk MCP server (SSE) on http://{args.host}:{args.port}/sse")
        mcp.run(transport=args.transport, host=args.host, port=args.port)
    else:
        mcp.run(transport=args.transport)
