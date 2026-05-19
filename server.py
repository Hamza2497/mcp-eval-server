from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mcp-eval-server")

@mcp.tool()
def hello(name: str) -> str:
    """Say hello — just a smoke test."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()