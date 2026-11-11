# Base Image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies first so they are cached between code changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code (PDFs are mounted at run time, not baked into the image)
COPY app.py .

# Expose the default port for Streamlit
EXPOSE 8501

# Command to run the app
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
