# Booknauu API Test Framework

**AI-Powered Automated API Testing for the Booknauu Platform**

An automated testing framework for the Booknauu backend API. Designed with a minimalist approach and powered by **Local AI (Ollama)** to generate dynamic and realistic test data.

---

## Key Features

- **AI-Powered Data Generation** – Uses Ollama (LLaMA 3.2) to automatically generate values such as `email`, `businessName`, `resourceName`, and more.

- **Automatic Test Context Setup** – A global fixture automatically performs Register → Login → Create Resource Type → Create Resource → Create Reservation before the tests run.

- **Comprehensive Test Coverage** – Covers 70+ test scenarios across 11 modules, including Auth, Resource, Reservation, Google Integration, Team, Dashboard, and more.

- **Conflict Retry Mechanism** – If a `409 Conflict` occurs due to a duplicate email, the framework automatically retries with unique test data.

- **HTML Reports** – Supports visual HTML test reports for easier test result analysis.

- **Multi‑Layer Testing** (optional)  
  - **API Layer** – validates HTTP responses.  
  - **Integration Layer** – verifies that API operations correctly persist data in the database (PostgreSQL).  
  - **E2E Layer** – (planned) UI tests with Playwright.

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.11+ |
| Test Runner | Pytest |
| HTTP Client | Requests |
| AI Inference | Ollama (LLaMA 3.2 3B) |
| Database (Integration) | SQLAlchemy + psycopg2‑binary |
| Reporting | pytest‑html |
| Environment | python‑dotenv |

---

## 📋 Prerequisites

Before running the framework, make sure that:

1. **Booknauu Backend** is running at `http://localhost:8080`.
2. **Ollama** is installed and running with the `llama3.2:3b` model.

   ```bash
   ollama pull llama3.2:3b
3. **Install requirements:** 
   
   ```bash
   cd api-test-framework
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```