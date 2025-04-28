# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Install the project into `/app`
WORKDIR /app

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
ADD . /app

# Install the project's dependencies using the lockfile and settings
RUN uv venv
RUN uv sync --frozen --no-dev

# Presuming there is a `my_app` command provided by the project
CMD ["uv", "run", "main.py"]