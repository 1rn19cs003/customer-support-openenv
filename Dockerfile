FROM python:3.10

WORKDIR /app

# Copy only requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port for HF Spaces
EXPOSE 8000

# Run the app using main()
CMD ["python", "-m", "server.app"]