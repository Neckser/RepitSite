FROM node:18-alpine AS frontend-builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY src/app/templates/ ./src/app/templates/
COPY build.mjs ./build.mjs

RUN npx tsc /app/src/app/templates/mainpages/mainpage/mainpage.ts --target es2015 --outDir /app/src/app/templates/mainpages/mainpage

RUN npx tsc /app/src/app/templates/profiles/editstudprofile/editstudprofile.ts --target es2015 --outDir /app/src/app/templates/profiles/editstudprofile

RUN npx tsc /app/src/app/templates/profiles/edittutprofile/edittutprofile.ts --target es2015 --outDir /app/src/app/templates/profiles/edittutprofile

RUN npm run esbuild

FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    sqlite3 \
    locales \
    && echo "ru_RU.UTF-8 UTF-8" >> /etc/locale.gen \
    && locale-gen ru_RU.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

ENV LANG=ru_RU.UTF-8 \
    LANGUAGE=ru_RU:ru \
    LC_ALL=ru_RU.UTF-8

RUN mkdir -p /app/data

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --from=frontend-builder /app/build/ ./build/

COPY src/app/ ./src/app/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DATABASE_PATH=/app/data/basa.db

EXPOSE 80

WORKDIR /app/src/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]