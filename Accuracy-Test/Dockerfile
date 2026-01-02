# Use the official Bun image
FROM oven/bun:1 as builder

WORKDIR /usr/src/app

# Copy package files first to cache dependencies
COPY package.json bun.lock ./

# Install dependencies (frozen-lockfile ensures exact versions)
RUN bun install --frozen-lockfile

# Copy the rest of the source code
COPY . .

# Build the app
RUN bun run build

# Expose the port
EXPOSE 3000

# Start the server using Bun
# Note: adapter-node creates a "build/index.js" file by default
CMD ["bun", "build/index.js"]

