# Defining the base image:
FROM python:3.9-alpine3.13

# Defining the label:
LABEL maintainer="Abdalla"

# Ensures that Python output is sent straight to the terminal
ENV PYTHONUNBUFFERED=1

# Set working directory before COPY/ENV
WORKDIR /app

# Copy the Python dependencies files into the container
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

# Copy the application code into the container
COPY ./app /app

# Expose port 8000 to allow external access to the app
EXPOSE 8000

# Allow Docker Compose to override this with build arg
ARG DEV=false

# Create a virtual environment in /py
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then \
        /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# Add the virtual environment’s bin directory to the PATH
ENV PATH="/py/bin:$PATH"

# Use non-root user for better security
USER django-user

# Default command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
