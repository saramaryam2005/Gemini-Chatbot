# Use an official lightweight Python image
FROM python:3.10-slim

# Set up a new user named "user" with UID 1000
RUN useradd -m -u 1000 user

# Set the working directory inside the container
WORKDIR /home/user/app

# Copy requirements file first to leverage Docker caching
COPY --chown=user requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of your application files into the container
COPY --chown=user . .

# Switch to the non-root user
USER user

# Expose the default port Hugging Face Spaces expects
EXPOSE 7860

# Run the Flask app on host 0.0.0.0 and port 7860
CMD ["python", "app.py"]