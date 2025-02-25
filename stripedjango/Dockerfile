FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    git \
    libjpeg-dev \
    zlib1g-dev \
    libwebp-dev \
    libffi-dev \
    gdal-bin \
    libgdal-dev \
    python3-gdal \
    binutils \
    libproj-dev \
    proj-data \
    libgeos-dev \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*\
    postgis \
    postgresql-13-postgis-3 

RUN apt-get install -y libgdal-dev
RUN pip install GDAL==3.4.2

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

CMD ["python", "strupedjango.wsgi:application", "--bind", "0.0.0.0:8000"]