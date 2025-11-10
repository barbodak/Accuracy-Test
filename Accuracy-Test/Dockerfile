FROM node:18.19.0 AS node-build

WORKDIR /usr/src/app

COPY Accuracy-Test/package*.json ./

# --- ADD THIS SECTION FOR PUPPETEER ---
# Install system dependencies for Chromium
RUN apt-get update \
    && apt-get install -y \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libgbm1 \
    libasound2 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libatspi2.0-0 \
    libxshmfence1 \
    --no-install-recommends \
    # Clean up the cache
    && rm -rf /var/lib/apt/lists/*
# --- END SECTION ---

RUN npm install

COPY Accuracy-Test/ .

RUN npm run build

ENTRYPOINT [ "/bin/sh", "-c" , "node build" ]
