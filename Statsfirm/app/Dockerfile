# Multi-stage Dockerfile for Statsfirm Co. Web Platform & BFF
# Base image: Node.js 20 LTS Alpine (minimal footprint, hardened security)
FROM node:20-alpine AS base

WORKDIR /app

# Install dependencies in a separate layer for caching
FROM base AS dependencies
COPY package.json package-lock.json* ./
RUN npm ci --only=production

# Production runtime image
FROM base AS runner
ENV NODE_ENV=production
ENV PORT=3000

# Security: run as non-root user
USER node

# Copy dependencies and application source code
COPY --chown=node:node --from=dependencies /app/node_modules ./node_modules
COPY --chown=node:node . .

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/ || exit 1

CMD ["node", "server.js"]
