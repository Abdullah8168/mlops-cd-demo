mlops-cd-demo

A Continuous Delivery pipeline for a small machine learning inference API.

Overview

The application is a Flask service that exposes a dummy prediction model. Its real purpose is to
act as the payload for a complete delivery pipeline: every release is packaged once as a Docker
image, published to the GitHub Container Registry, deployed automatically to staging, verified by
a health check, and promoted to production only after a human approves it.

How the pipeline works

Pull requests run continuous integration only. The CI workflow installs dependencies and runs the
test suite, and nothing is packaged or deployed.

Continuous delivery is triggered by pushing a semantic version tag such as v1.1.0. A tag is what
declares a release, not an ordinary commit on main. When a tag is pushed, the pipeline runs the
tests again, extracts the version number from the tag name, builds a Docker image, tags it with
both the version and latest, and pushes both to the registry.

The image is then deployed to the staging environment automatically. A smoke test calls the health
endpoint and confirms both that the service reports itself healthy and that it reports the exact
version that was just built. If either check fails the pipeline stops and production is never
reached.

Production deployment waits for manual approval from a required reviewer. Once approved, the same
image that was verified in staging is pulled and started. The artifact is never rebuilt between
environments, so what runs in production is byte for byte what passed the staging smoke test.

The artifact

Each release produces an image published as ghcr.io/abdullah8168/mlops-cd-demo followed by the
version number, along with a moving latest tag. The latest tag exists only as a convenience.
Deployments always reference an explicit version so that any running container can be reproduced
exactly.

Endpoints

A GET request to the root path returns a short service banner.

A GET request to /health returns the application version, the model version, the git commit the
image was built from, and a status field. This endpoint is what gates promotion to production.

A POST request to /predict accepts a JSON body containing a numeric value field and returns the
input, the prediction, and the model version. The model is deliberately trivial: it doubles the
input value.

Traceability

The git commit is baked into the image at build time as a Docker build argument and surfaced
through the health endpoint. This means any running container can be traced back to the exact
commit, pull request, and release tag it came from, which is what makes an incident in production
investigable.

Rollback

Because every image is versioned and immutable, rolling back is a matter of running an earlier
image again rather than rebuilding anything. Stop and remove the current container, then start a
new one from the previous version tag and confirm the health endpoint reports that older version.
Relying on the latest tag alone would make this impossible, which is why explicit version tags
matter.

Local development

Create a virtual environment, install the requirements, and run the test suite with pytest. The
service can be started directly with python or built and run as a Docker image. The health
endpoint is available on port 5000.

Versioning

The VERSION file holds the current application version and should be updated in the same pull
request as the change it describes. The release tag must match it. Application version, model
version, and dataset version are separate concerns and can move independently, which is what makes
delivery for machine learning systems harder than for ordinary software.
