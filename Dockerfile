FROM python:3.10-bookworm as builder

RUN pip install poetry==1.4.2
WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:3.10-slim-bookworm as runtime

# Install only necessary runtime dependencies
# Remove unnecessary packages like vim and sudo for security
RUN apt-get update && \
    apt-get -y install --no-install-recommends libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
WORKDIR /app

# Create a dedicated non-root user with minimal privileges
# Do NOT grant sudo access or any elevated privileges
RUN useradd -m -u 1000 -s /bin/bash app && \
    chown -R app:app /app

# Switch to non-root user BEFORE any application files are accessible
USER app

# Add security labels
LABEL security.no-sudo="true" \
      security.runs-as="non-root" \
      maintainer="security@restaurant.com"
