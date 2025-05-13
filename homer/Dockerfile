# File: homer/Dockerfile

# -------- STAGE 1: Builder --------
    FROM python:3.10.17-slim-bookworm AS builder

    RUN apt-get update && apt-get install -y --no-install-recommends \
        wget \
        curl \
        ca-certificates \
        gnupg \
     && rm -rf /var/lib/apt/lists/*
    
    WORKDIR /build
    
   
    # Install Python deps
    COPY homer/requirements.txt .
    RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
    
    # -------- STAGE 2: Runtime --------
    FROM python:3.10.17-slim-bookworm
    
    RUN apt-get update && apt-get install -y --no-install-recommends \
        sudo \
        ca-certificates \
     && rm -rf /var/lib/apt/lists/*
    
    # Create non-root user
    RUN addgroup --system homer && \
        adduser --system --ingroup homer --home /homer homer && \
        adduser homer sudo && \
        echo "homer ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/homer
    
    # Setup working dir
    WORKDIR /homer
    
    # Python deps
    COPY --from=builder /install /usr/local
    
    # Copy full app package
    COPY homer/ /homer/
    
    # CLI executable
    RUN chmod +x /homer/homer && ln -sf /homer/homer /usr/local/bin/homer
    
    # Entrypoint script (Python-based)
    RUN chown homer:homer /homer/entrypoint.py
    
    # Final ownership
    RUN chown -R homer:homer /homer
    
    USER homer
    
    ENV PYTHONPATH=/
    ENV HOME=/homer
    
    VOLUME ["/tmp"]
    
    ENTRYPOINT ["python", "/homer/entrypoint.py"]
    