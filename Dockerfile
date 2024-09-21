# Base Image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy necessary files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the default port for Streamlit
EXPOSE 8501

# Command to run the app
CMD ["streamlit", "run", "app.py"]
