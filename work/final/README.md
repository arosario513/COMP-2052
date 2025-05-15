# **MASS**: _Medical Appointment Scheduling System_

> A full-stack medical scheduling web application built with [Flask](https://flask.palletsprojects.com/en/stable/), containerized with [Docker](https://www.docker.com/), and served via [Gunicorn](https://gunicorn.org/) and [Nginx](https://nginx.org/en/).

## Table of Contents

- [About the Project](#about-the-project)
- [Manual Setup](#manual-setup)
- [Docker Setup](#docker-setup)
- [Project Structure](#project-structure)
- [Environment Variables](#environment-variables)

## About the Project

MASS is my final project for **COMP-2052** and the most ambitious app I've developed so far. It enables users to register, log in, and schedule appointments, with roles for Admins, Doctors, and Patients.

## Manual Setup

Before starting, clone the repository and run the setup script:

### macOS/Linux

```bash
curl https://raw.githubusercontent.com/arosario513/COMP-2052/refs/heads/main/work/final/setup.sh | sh
```

**OR**

```bash
wget https://raw.githubusercontent.com/arosario513/COMP-2052/refs/heads/main/work/final/setup.sh
chmod +x setup.sh
./setup.sh
```

Navigate into the `final/` directory and set up your Python environment:

```bash
cd final
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Project Structure

```
final/
├── app/
│   ├── admin/
│   ├── appointments/
│   ├── auth/
│   ├── models/
│   ├── static/
│   └── templates/
├── docker-compose.yml
├── Dockerfile
├── gen-certs.sh
├── main.py
├── nginx/default.conf
├── requirements.txt
└── setup.sh
```

## Environment Variables

Create a `.env` file in the project root with the following:

```env
SECRET_KEY='your_secret_key_here'

# Default Admin Credentials (change these!)
ADMIN_FIRSTNAME='Default'
ADMIN_LASTNAME='Admin'
ADMIN_EMAIL='admin@example.com'
ADMIN_PASSWORD='changeme123'
```

To generate a secure `SECRET_KEY`:

```bash
python -c 'import secrets; print(secrets.token_hex(16))'
```

## Running the App (Manually)

Once configured:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

You may change the port if needed.

## Docker Setup

> **Preferred method** – easier, isolated, and more secure.

Ensure you have Docker and OpenSSL installed.

1. Clone the repo and create your `.env` file.
2. Generate self-signed SSL certs:

```bash
./gen-certs.sh
```

Example output:

```
[+] Generating root CA...
[+] Issuing cert for mass-server...
Certificate request self-signature ok
subject=C=US, ST=PR, O=MASS, OU=MASS, CN=mass-server
```

3. Verify certificates were created in `nginx/certs/`.

4. Build and run the app:

```bash
docker-compose up -d --build
```

Then visit:

- [https://127.0.0.1](https://127.0.0.1)
- [https://mass.localhost](https://mass.localhost)

**Note**: Browsers will warn you about the self-signed certs. For production, replace them with real certificates and update `nginx/default.conf` accordingly.
