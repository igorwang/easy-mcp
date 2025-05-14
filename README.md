# Easy MCP

A streamlined server deployment solution for Model Context Protocol (MCP) using FastMCP. This project simplifies the process of running and managing multiple MCP servers with different transport methods.

## Features

- 🚀 Quick setup of multiple MCP servers
- 🔄 Support for multiple transport types:
  - NPX-based transport
  - UVX-based transport
  - HTTP proxy transport
- ⚡️ Built on FastMCP for high performance
- 🛠 Configurable through JSON
- 🐳 Docker support included

## Requirements

- Python >= 3.13
- FastMCP >= 2.3.3
- UV >= 0.7.3

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/easy-mcp.git
cd easy-mcp
```

2. Set up your Python environment with UV:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

## Configuration

Create a `servers_config.json` file (you can copy from `servers_config.json.example`):

```json
{
    "mcpServers": {
       "sequential-thinking": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
        },
        "fetch": {
            "command": "uvx",
            "args": ["mcp-server-fetch"]
        },
        "local": {
            "url": "http://host.docker.internal:12010/mcp/"
        }
    }
}
```

## Usage

### Running with Python

```bash
python main.py
```

### Environment Variables

- `TRANSPORT`: Transport method (default: "streamable-http")
- `HOST`: Server host (default: "0.0.0.0")
- `PORT`: Server port (default: 8000)
- `LOG_LEVEL`: Logging level (default: "INFO")

### Docker Support

Build and run using Docker Compose:

```bash
docker-compose up --build
```

## API Endpoints

- `/health` - GET: Health check endpoint
- Additional endpoints provided by mounted MCP servers

## Project Structure

```
.
├── main.py              # Main server application
├── servers_config.json  # Server configuration
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose configuration
├── pyproject.toml     # Python project metadata
└── src/               # Source code directory
```

## Development

The project uses UV for dependency management and FastMCP for server implementation. The main application supports multiple transport methods and can be extended with additional MCP servers through configuration.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

---

Made with ❤️ by the Techower.Inc team
