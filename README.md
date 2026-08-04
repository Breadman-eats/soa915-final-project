# SOA915 Final Project — User & Order Microservices

Group members: Beatriz De Paula Carvalho Alves, Dhruvkumar Vinodkumar Katariya, Matthaus Thomas Matthew

## Project structure

```
soa915-final-project/
  user-service/
    main.py
    requirements.txt
    test_user_service.py
    Dockerfile
  order-service/
    main.py
    requirements.txt
    test_order_service.py
    Dockerfile
  k8s/
    user-service-deployment.yaml
    user-service-service.yaml
    user-service-configmap.yaml
    user-service-secret.yaml
    user-service-hpa.yaml
    order-service-deployment.yaml
    order-service-service.yaml
    order-service-hpa.yaml
  .github/
    workflows/
      ci.yml
  docker-compose.yml
  prometheus.yml
```

Each service is built with **Python + FastAPI** and stores data in memory (no database yet) —
data resets whenever a service restarts.

## Prerequisites

- Python 3.9+
- Docker Desktop (with Kubernetes enabled, for the K8s section below)
- Git

## Getting the code

```bash
git clone https://github.com/Breadman-eats/soa915-final-project.git
cd soa915-final-project
```

## Running locally (without Docker)

### User Service (port 8000)

```bash
cd user-service
python3 -m venv venv
```

Activate the virtual environment:
- **Windows (PowerShell):** `venv\Scripts\Activate.ps1`
- **Mac/Linux:** `source venv/bin/activate`

```bash
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Open **http://localhost:8000/docs**.

### Order Service (port 8001)

Same steps in a separate terminal, inside `order-service`, but run:
```bash
python -m uvicorn main:app --reload --port 8001
```

Open **http://localhost:8001/docs**.

### Endpoints

**User Service**
| Method | Path | Description |
|---|---|---|
| GET | `/` | Health check |
| GET | `/users` | List all users |
| POST | `/users` | Create a user (`name`, `email`) |
| GET | `/users/{user_id}` | Get one user |
| DELETE | `/users/{user_id}` | Delete a user |
| GET | `/metrics` | Prometheus metrics |

**Order Service**
| Method | Path | Description |
|---|---|---|
| GET | `/` | Health check |
| GET | `/orders` | List all orders |
| POST | `/orders` | Create an order (`user_id`, `item`, `quantity`) |
| GET | `/orders/{order_id}` | Get one order |
| DELETE | `/orders/{order_id}` | Delete an order |
| GET | `/metrics` | Prometheus metrics |

## Running with Docker Compose (recommended)

This runs both services plus the full monitoring stack (Prometheus + Grafana) together:

```bash
docker compose up --build
```

This starts 4 containers:
- **user-service** — http://localhost:8000/docs
- **order-service** — http://localhost:8001/docs
- **prometheus** — http://localhost:9090 (check **Status > Targets** to confirm both services show `UP`)
- **grafana** — http://localhost:3000 (login: `admin` / `admin`, you'll be asked to set a new password on first login)

### Setting up the Grafana dashboard (if starting fresh)

1. Log into Grafana
2. Menu → **Connections** → **Data sources** → **Add data source** → **Prometheus**
3. Set URL to `http://prometheus:9090` → **Save & test**
4. Menu → **Dashboards** → **New** → **Add visualization** → select the Prometheus data source
5. Switch to **Code** mode in the query editor and enter:
   ```
   rate(http_requests_total[1m])
   ```
6. Save the panel, then save the dashboard

## Running tests

In each service folder (with its venv active):
```bash
python -m pytest
```
Each service has 8 tests covering all endpoints (happy path + 404 error handling).

## CI/CD

A GitHub Actions workflow (`.github/workflows/ci.yml`) runs automatically on every push to `main`:
1. Runs the User Service test suite
2. Runs the Order Service test suite
3. Builds both Docker images (only if both test suites pass)

Check the **Actions** tab on the GitHub repo to see run history.

## Running on Kubernetes

Requires Kubernetes enabled in Docker Desktop (Settings → Kubernetes → Enable Kubernetes).

```bash
docker compose build
kubectl apply -f k8s/
kubectl get pods
kubectl get deployments
kubectl get services
kubectl get hpa
```

This deploys:
- **Deployments** for both services, 2 replicas each (self-healing — a crashed pod is automatically restarted)
- **Services** giving each deployment a stable internal address
- A **ConfigMap** and **Secret** (example values, since neither service currently needs real config/secrets)
- **HorizontalPodAutoscalers** (min 2 / max 5 replicas, scaling on CPU utilization)

To access a service running in the cluster from your browser:
```bash
kubectl port-forward service/user-service 8000:8000
kubectl port-forward service/order-service 8001:8001
```

### Known limitations

- **HPA metrics show `<unknown>`:** Docker Desktop's local Kubernetes cluster doesn't include
  `metrics-server` by default, so the HPA can't read live CPU usage. The autoscaling configuration
  is correct and would work on a cluster with metrics-server installed (e.g. a cloud-managed cluster).
- **Monitoring runs via Docker Compose, not inside Kubernetes:** Docker Desktop's Kubernetes uses
  `kind` internally, which keeps its own isolated image store separate from the regular Docker
  build engine. This meant locally built images (including our metrics-instrumented code) weren't
  reliably visible inside the cluster without extra tooling (`kind load docker-image`) that isn't
  installed by default. Rather than lose time on that local tooling gap so close to the deadline,
  we run Prometheus + Grafana as their own layer via `docker-compose.yml`, scraping the same
  `/metrics` endpoints the services expose. This is also a common real-world pattern — a separate
  observability stack rather than something bundled into each service's own deployment.

## Notes for the team

- **Dhruvkumar (Docker/Kubernetes):** Dockerfiles and K8s manifests are in place per service /
  in `k8s/`. Feel free to extend the HPA/ConfigMap/Secret setup if we add real config later.
- **Beatriz (Testing/CI/CD/Monitoring):** test suites and the CI pipeline are in place; the
  monitoring stack (Prometheus + Grafana) is running via Docker Compose — see above for the
  dashboard setup steps if you want to add more panels.
- Both services currently use **in-memory storage** — a real database may get added later.
- `venv/` folders are excluded via `.gitignore` — always create your own, never commit it.
