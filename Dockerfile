FROM python:3.9

WORKDIR /code

# Install system dependencies for Whisper (ffmpeg)
RUN apt-get update && apt-get install -y ffmpeg

# Install Python requirements
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy application files
COPY . .

# Expose the port Hugging Face requires
EXPOSE 7860

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
