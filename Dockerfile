FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the entire project
COPY . /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r api/requirements.txt

# Expose ports
EXPOSE 5000 8080

# Create a startup script
RUN echo '#!/bin/bash\n\
cd /app/api && python quantum_api.py &\n\
cd /app/web/public && python -m http.server 8080\n\
' > /app/start.sh && chmod +x /app/start.sh

CMD ["/app/start.sh"]
