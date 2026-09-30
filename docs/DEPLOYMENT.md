# Deployment Guide

## Local, no hardware

### PowerShell

```powershell
cd "C:\path\to\Cloud-Connected-Smart-Plant-Care"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

Open another PowerShell:

```powershell
cd "C:\path\to\Cloud-Connected-Smart-Plant-Care\frontend"
npm install
npm run dev
```

Open another PowerShell:

```powershell
cd "C:\path\to\Cloud-Connected-Smart-Plant-Care\sensor_simulator"
python simulator.py
```

Dashboard: `http://localhost:5173`  API docs: `http://localhost:8000/docs`.

## Docker / cloud-style local deployment

```powershell
docker compose up --build
```

Dashboard: `http://localhost:8080`  API: `http://localhost:8000`.

Stop:

```powershell
docker compose down
```

Delete database volume too:

```powershell
docker compose down -v
```

## Production notes

1. Replace the demo API key with a secret stored in the platform's secret manager.
2. Use PostgreSQL or a managed database, not SQLite.
3. Put HTTPS in front of the API.
4. Use real user authentication (Firebase Auth, Supabase Auth, Auth0, or the cloud provider's identity service).
5. Never expose the demo API key in a public repository.
6. Configure CORS to the exact production frontend origin.
7. Add rate limiting and device-specific credentials.
8. Use a managed IoT broker for large fleets.

The exact vendor UI and free-tier limits change over time, so verify current quotas/pricing before deployment.

## Option A — student-friendly managed deployment

A practical split is:

```text
React/Vite frontend -> static host (for example Vercel)
FastAPI backend      -> managed web service (for example Render)
PostgreSQL           -> managed Postgres (for example Supabase)
```

### 1. Push the repository to GitHub

```powershell
git init
git add .
git commit -m "Complete smart plant cloud project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/Cloud-Connected-Smart-Plant-Care.git
git push -u origin main
```

### 2. Create the Postgres database

Create a Supabase project, open **Connect**, and copy the PostgreSQL connection string for the backend. Supabase documents direct and pooled connection modes and provides a full PostgreSQL database. citeturn0search2turn0search3

Set the Render backend environment variables:

```text
DATABASE_URL=<your Supabase PostgreSQL connection string>
API_KEY=<strong random server/device credential>
CORS_ORIGINS=<your deployed frontend URL>
OFFLINE_AFTER_SECONDS=60
WATERING_DURATION_SECONDS=6
WATERING_COOLDOWN_SECONDS=60
MAX_WATERING_EVENTS_PER_HOUR=4
```

### 3. Deploy the FastAPI backend

Create a Render Web Service connected to the GitHub repository. Render's current FastAPI deployment documentation uses a Python build command and an Uvicorn start command, and Render supports automatic redeploys from linked Git branches. citeturn0search0turn0search12

For this repository use:

```text
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

After deployment, verify:

```text
https://YOUR-BACKEND.onrender.com/health
https://YOUR-BACKEND.onrender.com/docs
```

### 4. Deploy the React frontend

Create a Vercel project from the GitHub repository and set:

```text
Root Directory: frontend
Build Command: npm run build
Output Directory: dist
```

Set:

```text
VITE_API_URL=https://YOUR-BACKEND.onrender.com
VITE_API_KEY=<matching development/device credential>
```

Vercel documents Vite/React as a deployable static application pattern. citeturn0search5

### Important production security note

Do **not** treat `VITE_API_KEY` as a real secret in a production browser application. Vite variables prefixed with `VITE_` are bundled into client-side code. For a real deployment, replace this demo mechanism with user authentication plus server-side authorization and per-device credentials. The current key is intentionally suitable only for this educational prototype.

### 5. Simulator deployment

For a portfolio demo, run the simulator locally and point it to the public API:

```powershell
$env:API_URL='https://YOUR-BACKEND.onrender.com'
$env:API_KEY='<device credential>'
python sensor_simulator\simulator.py
```

This creates a useful architecture demonstration: **local virtual IoT node -> public cloud API -> managed PostgreSQL -> public dashboard**.

## Option B — enterprise architecture

Use AWS IoT Core -> API Gateway/IoT Rules -> Lambda/EventBridge -> DynamoDB/Timestream -> SNS -> S3/CloudFront, with CloudWatch for logs/metrics. See `docs/AWS_ARCHITECTURE.md`.
