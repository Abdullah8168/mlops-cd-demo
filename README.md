# mlops-cd-demo

Continuous Delivery pipeline for a small ML inference API.

## Pipeline

```
v*.*.* tag -> test -> build -> GHCR -> staging -> smoke test -> MANUAL APPROVAL -> production
```

PRs run CI only (`.github/workflows/ci.yml`). CD (`.github/workflows/cd.yml`) fires only on a
semantic version tag, so a tag is what declares a release.

## Artifact

Built once per tag and promoted unchanged through both environments:

```
ghcr.io/abdullah8168/mlops-cd-demo:<version>
ghcr.io/abdullah8168/mlops-cd-demo:latest
```

`latest` is a movable convenience tag. Deployments always reference the explicit version.

## Endpoints

| Route | Method | Purpose |
|---|---|---|
| `/` | GET | service banner |
| `/health` | GET | version + liveness, used as the staging gate |
| `/predict` | POST | dummy model, returns `value * 2` |

```json
{
  "application_version": "1.0.0",
  "model_version": "model-7",
  "git_commit": "ddb115e",
  "status": "healthy"
}
```

`git_commit` is baked in at build time via a Docker build arg, so any running container can be
traced back to an exact commit.

## Rollback

Earlier images are versioned and immutable, so rollback is a re-run, never a rebuild:

```bash
docker rm -f mlops-api
docker run -d --name mlops-api --restart unless-stopped -p 5000:5000 \
  ghcr.io/abdullah8168/mlops-cd-demo:1.0.0
curl http://localhost:5000/health
```

## Local development

```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
pytest
docker build -t mlops-cd-demo:local .
```
