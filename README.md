# SOA915 Final Project — User & Order Microservices

Group members: Beatriz De Paula Carvalho Alves, Dhruvkumar Vinodkumar Katariya, Matthaus Thomas Matthew

## Project structure

```
soa915-final-project/
  user-service/
    main.py
    requirements.txt
  order-service/
    main.py
    requirements.txt
```

Each folder is an independent microservice, built with **Python + FastAPI**. They currently
store data in memory (no database yet) — data resets whenever a service restarts.

## Prerequisites

- Python 3.9+ installed (`python3 --version` or `python --version` to check)
- Git

## Getting the code

```bash
git clone https://github.com/Breadman-eats/soa915-final-project.git
cd soa915-final-project
```

## Running User Service (port 8000)

```bash
cd user-service
python3 -m venv venv
```

Activate the virtual environment:
- **Windows (PowerShell):** `venv\Scripts\Activate.ps1`
- **Mac/Linux:** `source venv/bin/activate`

Install dependencies and run:
```bash
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Open **http://localhost:8000/docs** to see and test the API.

### Endpoints
| Method | Path | Description |
|---|---|---|
| GET | `/` | Health check |
| GET | `/users` | List all users |
| POST | `/users` | Create a user (`name`, `email`) |
| GET | `/users/{user_id}` | Get one user |
| DELETE | `/users/{user_id}` | Delete a user |

## Running Order Service (port 8001)

Open a **separate terminal window** (User Service needs to keep running in its own window):

```bash
cd order-service
python3 -m venv venv
```

Activate the virtual environment (same commands as above), then:
```bash
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8001
```

Open **http://localhost:8001/docs** to see and test the API.

### Endpoints
| Method | Path | Description |
|---|---|---|
| GET | `/` | Health check |
| GET | `/orders` | List all orders |
| POST | `/orders` | Create an order (`user_id`, `item`, `quantity`) |
| GET | `/orders/{order_id}` | Get one order |
| DELETE | `/orders/{order_id}` | Delete an order |

## Notes for the team

- **Dhruvkumar (Docker/Kubernetes):** each service folder is meant to become its own container.
  A Dockerfile per service (`user-service/Dockerfile`, `order-service/Dockerfile`) plus a
  root-level `docker-compose.yml` running both together is the natural next step.
- **Beatriz (Testing/CI/CD/Monitoring):** endpoints are listed above — good candidates for
  unit tests (business logic), integration tests (hitting the running API), and eventually a
  GitHub Actions workflow that runs tests on push.
- Both services currently use **in-memory storage**. A real database (e.g. SQLite/Postgres)
  may get added later — flag if your part depends on persistent data.
- `venv/` folders are excluded via `.gitignore` — always create your own with the steps above,
  never commit it.
