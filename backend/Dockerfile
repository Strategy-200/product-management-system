
# 1. Select Python base image
FROM python:3.11-slim

# 2. Set working directory
WORKDIR /app

# 3. Set Python environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. Copy requirements file
COPY requirements.txt .

# 5. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy backend application files
COPY . .

# 7. Expose FastAPI port
EXPOSE 8000

# 8. Start FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
