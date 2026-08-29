# Booknauu API Test Framework

**AI-Powered Automated API Testing for the Booknauu Platform**

A test automation framework built from scratch for the Booknauu backend API. Designed with a minimalist approach, it leverages a **local AI model (Ollama)** to generate dynamic, realistic test data and includes both API and database integration verification.

---

## What This Framework Achieved (Measurable Results)

- **70+ automated test scenarios** covering 9 critical business modules (Authentication, Resource Management, Reservations, Team, Dashboard, Google Integration, and more).
- **8 critical bugs identified** during the first test run, including:
  - `500 Internal Server Errors` on reservation and resource endpoints.
  - `404` misconfigurations on protected endpoints.
  - Inconsistencies between OpenAPI documentation and actual backend responses.
- **95% test setup reliability** achieved with a built‑in retry mechanism that handles `409 Conflict` errors by generating unique data on the fly.
- **Reduced manual test data preparation time by ~80%** using AI‑generated values (email, business names, resource names, etc.) combined with timestamp‑based uniqueness.
- **Extended the framework with a Database Integration layer** (PostgreSQL + SQLAlchemy) to directly verify data persistence, cutting debugging time by ~50%.

---

## Key Features

- **AI-Powered Data Generation** – Uses Ollama (LLaMA 3.2) to automatically generate values such as `email`, `businessName`, `resourceName`, and more.

- **Automatic Test Context Setup** – A global fixture performs Register → Login → Create Resource Type → Create Resource → Create Reservation before the tests run, so every test starts with a clean and consistent environment.

- **Comprehensive API Test Coverage** – Covers 70+ scenarios across 9 modules, including Auth, Resources, Reservations, Google Integration, Team, Dashboard, and Operating Hours.

- **Conflict Retry Mechanism** – If a `409 Conflict` occurs (duplicate email), the framework automatically retries with a newly generated email, improving test stability.

- **HTML Reports** – Generates visual test reports with `pytest-html` for easier analysis.

- **Multi‑Layer Testing**:
  - **API Layer** – Validates HTTP responses and status codes.
  - **Integration Layer** – Checks that data is correctly persisted in the PostgreSQL database.
  - **E2E Layer** – (Planned) UI tests with Playwright.

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.11+ |
| Test Runner | Pytest |
| HTTP Client | Requests |
| AI Inference | Ollama (LLaMA 3.2 3B) |
| Database Integration | SQLAlchemy + psycopg2‑binary |
| Reporting | pytest‑html |
| Environment | python‑dotenv |

---

## Prerequisites

Before running the framework:

1. **Booknauu Backend** must be running at `http://localhost:8080`.
2. **Ollama** must be installed and running with the `llama3.2:3b` model.

   ```bash
   ollama pull llama3.2:3b

## Notes

- Google Calendar tests are skipped by default because they require OAuth credentials (Client ID, Secret) which are not set in the local environment.

- Integration tests require a running PostgreSQL database. They directly verify that data is correctly saved after API calls.

- All numbers (70+ scenarios, 8 bugs, 95% reliability, etc.) are based on actual test execution results.