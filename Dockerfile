FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

COPY ["pyproject.toml", "uv.lock", "./"]

RUN uv sync --frozen --no-install-project --no-dev 

ENV PATH="/app/.venv/bin:$PATH"

COPY ["pred_app.py", "final_model.bin", "./"]

EXPOSE 9696

ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "pred_app:web_app"]
