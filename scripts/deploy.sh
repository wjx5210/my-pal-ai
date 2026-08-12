#!/usr/bin/env sh
set -eu

cd "$(dirname "$0")/.."

if [ ! -f .env.production ]; then
    echo "缺少 .env.production，请先复制 .env.production.example 并填写 API Key。"
    exit 1
fi

if [ ! -f data/vector_store.json ]; then
    echo "缺少 data/vector_store.json，请先在本地构建向量库并上传。"
    exit 1
fi

docker compose up -d --build
docker compose ps
