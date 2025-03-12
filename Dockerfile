FROM continuumio/miniconda3:latest

WORKDIR /app

# Copy environment file first
COPY environment.yml /app/

# Create Conda environment
RUN conda env create -f environment.yml

# Set up shell to use the Conda environment by default
SHELL ["conda", "run", "-n", "kokoro-tts", "/bin/bash", "-c"]

# Copy application code
COPY . /app/

# Expose the API port
EXPOSE 8000

# Run using the Conda environment
CMD ["conda", "run", "--no-capture-output", "-n", "kokoro-tts", "python", "app.py"]