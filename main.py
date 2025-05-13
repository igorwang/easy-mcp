import asyncio
import json
import os
import sys

from fastmcp import Client, FastMCP
from fastmcp.client.transports import NpxStdioTransport, UvxStdioTransport
from starlette.requests import Request
from starlette.responses import JSONResponse

# 1. Ensure your src/ path is on Python's import path
sys.path.append("./src")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Create the FastMCP instance
main_mcp = FastMCP()


async def setup_servers():
    # 3. Define an async setup function to load & mount your servers_config.json
    config_path = os.path.join(BASE_DIR, "servers_config.json")
    if not os.path.isfile(config_path):
        raise FileNotFoundError(f"Servers config not found at {config_path}")
    with open(config_path, "r") as f:
        config = json.load(f)

    for key, value in config["mcpServers"].items():
        # NPX-based transport
        if value.get("command") == "npx":
            pkg = value["args"][1]
            raw_args = value["args"][1:] if len(value["args"]) > 1 else None
            transport = NpxStdioTransport(
                package=pkg,
                # args=raw_args,
                # env_vars=value.get("env", None),
            )
            client = Client(transport)
            server_mcp = FastMCP.from_client(client)
            main_mcp.mount(key, server_mcp)
        # UVX-based transport
        elif value.get("command") == "uvx":
            tool = value["args"][0]
            raw_args = value["args"][1:] if len(value["args"]) > 1 else None
            transport = UvxStdioTransport(tool_name=tool, tool_args=None)
            client = Client(transport)
            # server_mcp = FastMCP.from_client(client)
            main_mcp.mount(key, server_mcp)

        # HTTP proxy transport
        elif value.get("url"):
            client = Client(value["url"])
            server_mcp = FastMCP.from_client(client)
            main_mcp.mount(key, server_mcp, as_proxy=True)
        else:
            raise ValueError(f"Invalid server config for {key}: {value}")


@main_mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> JSONResponse:
    return JSONResponse({"status": "healthy"})


if __name__ == "__main__":
    asyncio.run(setup_servers())
    transport = os.getenv("TRANSPORT", "streamable-http")
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    log_level = os.getenv("LOG_LEVEL", "INFO").lower()

    main_mcp.run(transport=transport, host=host, port=port, log_level=log_level)

    # This call creates the TaskGroup *before* handling any requests, so
    # by the time setup_mcp_servers() runs, all internals are ready.
