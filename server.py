"""
Calculator MCP Server
----------------------
A simple Model Context Protocol (MCP) server, built with FastMCP, that
exposes basic arithmetic operations as tools an MCP client (e.g. Claude
Desktop, Claude Code, or any MCP-compatible app) can call.

Run locally (stdio transport, used by Claude Desktop / Claude Code):
    python server.py

Run as an HTTP server (useful for remote hosting):
    python server.py --http --port 8000
"""

import argparse
import math

from fastmcp import FastMCP

# Create the MCP server. The name shows up in client UIs.
mcp = FastMCP("Calculator")


@mcp.tool
def add(a: float, b: float) -> float:
    """Add two numbers together and return the sum."""
    return a + b


@mcp.tool
def subtract(a: float, b: float) -> float:
    """Subtract b from a and return the difference."""
    return a - b


@mcp.tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers and return the product."""
    return a * b


@mcp.tool
def divide(a: float, b: float) -> float:
    """Divide a by b and return the quotient. Raises an error if b is 0."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


@mcp.tool
def power(base: float, exponent: float) -> float:
    """Raise base to the power of exponent."""
    return base ** exponent


@mcp.tool
def square_root(a: float) -> float:
    """Return the square root of a. Raises an error if a is negative."""
    if a < 0:
        raise ValueError("Cannot take the square root of a negative number.")
    return math.sqrt(a)


@mcp.tool
def modulo(a: float, b: float) -> float:
    """Return the remainder of a divided by b."""
    if b == 0:
        raise ValueError("Cannot compute modulo with a divisor of zero.")
    return a % b


@mcp.tool
def calculate(expression: str) -> float:
    """
    Evaluate a simple arithmetic expression (e.g. "2 + 3 * (4 - 1)").
    Supports +, -, *, /, **, %, parentheses, and decimals. No variables,
    function calls, or names are allowed, for safety.
    """
    allowed_chars = set("0123456789+-*/.() %\t")
    if not set(expression) <= allowed_chars:
        raise ValueError("Expression contains characters that are not allowed.")
    try:
        # eval with no builtins/names available -> only arithmetic on literals works
        result = eval(expression, {"__builtins__": {}}, {})
    except ZeroDivisionError:
        raise ValueError("Cannot divide by zero.")
    except Exception as exc:
        raise ValueError(f"Could not evaluate expression: {exc}")
    return float(result)


def main():
    parser = argparse.ArgumentParser(description="Calculator MCP Server")
    parser.add_argument("--http", action="store_true", help="Run as an HTTP server instead of stdio")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind when using --http")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind when using --http")
    args = parser.parse_args()

    if args.http:
        # Streamable HTTP transport - good for hosting on a server/cloud platform
        mcp.run(transport="http", host=args.host, port=args.port)
    else:
        # stdio transport - used when a local client (Claude Desktop, Claude Code)
        # launches this script as a subprocess
        mcp.run()


if __name__ == "__main__":
    main()
