# Booknauu API Test Framework

**AI-Powered Automated API Testing for the Booknauu Platform**

Framework testing otomatis untuk API backend Booknauu. Dirancang dengan pendekatan minimalis dan memanfaatkan **AI Lokal (Ollama)** untuk menghasilkan data uji yang dinamis dan realistis.

## ✨ Fitur Utama

- **AI-Powered Data Generation**: Menggunakan Ollama (LLaMA 3.2) untuk menghasilkan nilai `email`, `businessName`, `resourceName`, dll secara otomatis.
- **Automatic Setup Context**: Fixture global yang otomatis melakukan Register → Login → Buat Resource Type → Buat Resource → Buat Reservasi sebelum test berjalan.
- **Comprehensive Test Coverage**: Mencakup 70+ skenario uji dari 11 modul (Auth, Resource, Reservation, Google Integration, Team, Dashboard, dll).
- **Conflict Retry Mechanism**: Jika terjadi `409 Conflict` (duplikat email), framework akan otomatis mencoba ulang dengan data unik.
- **Laporan HTML**: Mendukung output laporan visual untuk memudahkan analisis.

## 🛠️ Tech Stack

- **Python 3.11+** & **Pytest** (Test Runner)
- **Requests** (HTTP Client)
- **Ollama** (Local AI Inference - LLaMA 3.2 3B)
- **python-dotenv** (Environment Management)

## 📋 Prasyarat

Sebelum menjalankan framework, pastikan:

1.  **Backend Booknauu** berjalan di `http://localhost:8080`.
2.  **Ollama** sudah terinstall dan berjalan dengan model `llama3.2:3b`.
    ```bash
    ollama pull llama3.2:3b
    ```