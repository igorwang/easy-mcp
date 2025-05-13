FROM python:3.13-slim

ARG NODE_VERSION=20.18.0

# Install Node.js and npm with architecture awareness
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl xz-utils \
    && ARCH=$(dpkg --print-architecture) \
    && if [ "$ARCH" = "arm64" ]; then \
          NODE_ARCH="arm64"; \
       else \
          NODE_ARCH="x64"; \
       fi \
    && curl -fsSL https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-${NODE_ARCH}.tar.xz \
       | tar -xJ --strip-components=1 -C /usr/local \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install uv && uv sync --locked
