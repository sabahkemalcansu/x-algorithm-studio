# Lightweight image for offline aha report + tooling.
# Full Phoenix/JAX demo is expected via native path or a future fat image.
FROM python:3.11-slim

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY scripts/ /app/scripts/
COPY fixtures/ /app/fixtures/
COPY templates/ /app/templates/
COPY Makefile /app/Makefile

ENV STUDIO_ROOT=/app
RUN mkdir -p /app/out/latest

# Default: fixture demo (always works, teaches the product surface)
CMD ["bash", "-lc", "python3 /app/scripts/render_aha_report.py --input /app/fixtures/sample_results.json --output /app/out/latest/report.html && cp /app/fixtures/sample_results.json /app/out/latest/results.json && echo '✔ report at /app/out/latest/report.html' && ls -la /app/out/latest"]
