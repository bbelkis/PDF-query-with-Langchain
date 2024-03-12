# Use an existing Docker image as a base
FROM python:3.10
# Set the working directory
WORKDIR /src
# Copy files into the image, if necessary
COPY . .
# Install dependencies
RUN pip install -r requirements.txt
# Expose port for FastAPI
EXPOSE 8000
# Command to run the FastAPI application with hot reloading
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]