FROM python:3.10

WORKDIR /app

# Step 1: Copy only requirements first (for caching)
COPY requirements.txt .

# Step 2: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 3: Copy rest of the project
COPY . .

# Step 4: Expose port for HF
EXPOSE 8000

# Optional: force cache rebuild
RUN echo "force rebuild v3"

# Step 5: Run app (HF multi-mode compatible)
CMD ["uvicorn", "server.app:main", "--host", "0.0.0.0", "--port", "${PORT:-8000}"]