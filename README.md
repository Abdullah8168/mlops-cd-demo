# mlops-cd-demo

Continuous Delivery pipeline for a small ML inference API.

- `v*.*.*` tag -> test -> build -> GHCR -> staging -> smoke test -> manual approval -> production
- Image: `ghcr.io/abdullah8168/mlops-cd-demo:<version>`
- Health: `GET /health` returns `application_version`, `model_version`, `git_commit`, `status`
