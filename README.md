# Booknauu API Test Framework

**AI-Powered Automated API Testing for the Booknauu Platform**

An automated testing framework for the Booknauu backend API. Designed with a minimalist approach and powered by **Local AI (Ollama)** to generate dynamic and realistic test data.

## ✨ Key Features

* **AI-Powered Data Generation**: Uses Ollama (LLaMA 3.2) to automatically generate values such as `email`, `businessName`, `resourceName`, and more.

* **Automatic Test Context Setup**: A global fixture automatically performs Register → Login → Create Resource Type → Create Resource → Create Reservation before the tests run.

* **Comprehensive Test Coverage**: Covers 70+ test scenarios across 11 modules, including Auth, Resource, Reservation, Google Integration, Team, Dashboard, and more.

* **Conflict Retry Mechanism**: If a `409 Conflict` occurs due to a duplicate email, the framework automatically retries with unique test data.

* **HTML Reports**: Supports visual HTML test reports for easier test result analysis.

## 🛠️ Tech Stack

* **Python 3.11+** & **Pytest** — Test Runner
* **Requests** — HTTP Client
* **Ollama** — Local AI Inference (LLaMA 3.2 3B)
* **python-dotenv** — Environment Management

## 📋 Prerequisites

Before running the framework, make sure that:

1. **Booknauu Backend** is running at `http://localhost:8080`.

2. **Ollama** is installed and running with the `llama3.2:3b` model.

   ```bash
   ollama pull llama3.2:3b
   ```
