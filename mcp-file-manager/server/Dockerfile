FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY . /app
ENV SANDBOX_ROOT=/app/sandbox
EXPOSE 8765
# Rode o servidor FastAPI direto via Uvicorn
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8765"]
