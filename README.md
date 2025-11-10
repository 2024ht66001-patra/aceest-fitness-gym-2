# ACEest Fitness Gym Service

This repository contains the ACEest Fitness Gym service. This README documents the repository layout and step-by-step instructions to set up, run, test, containerize, and deploy the application. It also summarizes the small task performed here (creating this README and running tests).

## Repository layout

Top-level files and directories:

- `Dockerfile` - Dockerfile to build the application image.
- `Jenkinsfile` - Pipeline definition used by Jenkins for CI/CD.
- `requirements.txt` - Python dependencies required by the service.
- `app/` - Python application source.
  - `__init__.py`
  - `ACEest_Fitness.py` - main application file (one of the entry points).
  - `ACEest_Fitness-V1.1.py` - alternate/older version of the app.
  - `__pycache__/` - bytecode cache (ignored in source control normally).
- `k8s/` - Kubernetes manifests for deployment and service.
  - `deployment-blue.yaml`
  - `deployment-canary.yaml`
  - `deployment-green.yaml`
  - `namespace.yaml`
  - `service.yaml`
- `tests/` - unit tests
  - `test_health.py` - basic health check test(s)

## Purpose of this README

You asked for a complete README with the layout and steps to perform the entire task done so far. The only explicit change made during this session was adding this `README.md` and running the repository tests to verify everything is healthy.

## Prerequisites

- OS: Windows (PowerShell) / Linux / macOS (commands shown for PowerShell where required)
- Python 3.8+ (use `python --version` to verify)
- pip (included with modern Python)
- Docker (for container builds)
- kubectl (for applying the manifests in `k8s/`)
- (Optional) Jenkins configured to use the included `Jenkinsfile`

## Setup (local)

1. Open PowerShell in the repository root (`c:\EC2\aceest-fitness-gym-2`).
2. (Optional but recommended) Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
# On cmd.exe: .venv\Scripts\activate.bat
```

3. Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Running the application locally

There are two main application files in `app/`. Use whichever is the intended entry point in your project.

From the repository root (PowerShell):

```powershell
# Example: run the main app
python .\app\ACEest_Fitness.py

# Or run the other version if desired
python .\app\ACEest_Fitness-V1.1.py
```

If the application requires environment variables or configuration, set them in your shell or in a `.env` file and load them accordingly. (This README does not assume additional env vars; check code for required configuration.)

## Running tests

This repo contains a small test suite under `tests/`. Use `pytest` to run tests.

Install pytest if not present:

```powershell
python -m pip install pytest
```

Run the tests:

```powershell
python -m pytest -q
```

Or to run only the health test:

```powershell
python -m pytest tests/test_health.py -q
```

Expected: tests should pass. If there are failures, check the test output for tracebacks and missing dependencies.

## Docker (build & run)

Build the Docker image (from the repo root):

```powershell
docker build -t aceest-fitness:local .
```

Run the container (map a port if the app listens on one, e.g., 5000):

```powershell
docker run --rm -p 5000:5000 aceest-fitness:local
```

Adjust `5000` to the port the application uses.

## Kubernetes deployment

The `k8s/` folder contains example manifests. To deploy to a cluster (after configuring `kubectl`):

```powershell
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/service.yaml
# choose one deployment strategy file to apply (blue, green, or canary)
kubectl apply -f k8s/deployment-blue.yaml
```

Note: These manifests are templates; review and adjust image names, container ports, resource requests/limits, and namespace settings before applying to a production cluster.

## CI/CD (Jenkins)

The repository includes a `Jenkinsfile`. Configure a Jenkins pipeline job that checks out this repo and executes the pipeline. The exact pipeline stages depend on your Jenkinsfile contents (build, test, docker build/push, deploy).

## What was done in this session

- Created `README.md` at the repository root describing layout, setup, run, test, Docker, and Kubernetes steps.
- Ran the repository tests to validate the project (see test results below or run the test commands shown earlier).

## Next steps / Recommendations

- Add or update documentation for any required environment variables that the application needs.
- Add a `README` inside `app/` describing entry points and how the app is structured if the app grows.
- Add CI steps to run tests automatically in `Jenkinsfile` if not already present.
- Add a `.dockerignore` file (if missing) to reduce image size.

## Contact / ownership

Repository: `aceest-fitness-gym-2`
Owner/maintainer: refer to repository / commit history.

---

End of README. This file was added automatically as part of your requested task.
