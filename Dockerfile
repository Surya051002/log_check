FROM python:3.14-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files first
COPY pyproject.toml uv.lock ./

# Install dependencies without installing the local project yet
RUN uv sync --no-install-project

# Copy application source code
COPY . .

# Install the project dependencies/environment
RUN uv sync

EXPOSE 8000
# Run the application
CMD ["uv", "run", "python", "src/p1/main.py"]