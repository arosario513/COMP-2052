# MASS: Medical Appointment Scheduling System

## Intro

This app was made in python using [flask](https://flask.palletsprojects.com/en/stable/) and deployed using [Docker](https://www.docker.com/), [gunicorn](https://gunicorn.org/) and [nginx](https://nginx.org/en/). This is my last work of COMP-2052, probably my biggest project so far.

## Manual Setup

Before deploying the app, we must clone it first, and then set up some variables.

### macOS/Linux

```bash
curl https://raw.githubusercontent.com/arosario513/COMP-2052/refs/heads/main/work/final/setup.sh | sh
```

or

```bash
wget https://raw.githubusercontent.com/arosario513/COMP-2052/refs/heads/main/work/final/setup.sh
chmod +x setup.sh
./setup.sh
```

This will have the `final` app in wherever you ran the setup script

### Structure

```
final
├── app
│   ├── admin
│   │   ├── forms.py
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── appointments
│   │   ├── forms.py
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── auth
│   │   ├── forms.py
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── __init__.py
│   ├── models
│   │   ├── appointment.py
│   │   ├── __init__.py
│   │   ├── role.py
│   │   └── user.py
│   ├── routes.py
│   ├── security.py
│   ├── static
│   │   ├── bootstrap-icons-1.12.1
│   │   │   ├── bootstrap-icons.min.css
│   │   │   └── fonts
│   │   │       ├── bootstrap-icons.woff
│   │   │       └── bootstrap-icons.woff2
│   │   ├── css
│   │   │   ├── bootstrap.min.css
│   │   │   └── style.css
│   │   ├── favicon.ico
│   │   └── js
│   │       └── bootstrap.bundle.min.js
│   └── templates
│       ├── accounts.html
│       ├── appointments.html
│       ├── base.html
│       ├── edit.html
│       ├── error.html
│       ├── footer.html
│       ├── header.html
│       ├── index.html
│       ├── login.html
│       ├── modal_appt.html
│       ├── modal.html
│       ├── new_account.html
│       ├── new_appointment.html
│       └── register.html
├── docker-compose.yml
├── Dockerfile
├── gen-certs.sh
├── main.py
├── nginx
│   └── default.conf
├── requirements.txt
└── setup.sh
```

Then proceed to cd into `final`.

Now we have to setup the python environment, which can be done with:

```bash
python -m venv venv
```

Enter the virtual environment:

```
source venv/bin/activate
```

You should have `(venv)` somewhere on the terminal letting you know you're in the virtual environment

Make sure pip is up-to-date:

```bash
pip install --upgrade pip
```

Now install the requirements:

```bash
pip install -r requirements.txt
```

### Environment Variables

This is needed otherwise flask will yell at you.

Create a file named `.env` and fill the credentials:

```bash
SECRET_KEY='yoursecretkey'

# Default Values (don't use these)
ADMIN_FIRSTNAME='Default'
ADMIN_LASTNAME='Admin'
ADMIN_EMAIL='admin@example.com'
ADMIN_PASSWORD='changeme123'
```

To set a proper secret key you can use this one-liner:

```bash
python -c 'import secrets;k=secrets.token_hex(16);print(k)'
```

Example Output:

```bash
b1d1e66e4266f3e9e2c63939fdd75292
```

And then set it for `SECRET_KEY`

```bash
SECRET_KEY='b1d1e66e4266f3e9e2c63939fdd75292'
```
Now you can run the app with:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

You can change the port to whatever you want, just make sure it doesn't conflict with anything else.

## Setup with Docker
**Note:** Make sure you got Docker and OpenSSL installed.

I prefer this method, because it's more secure and because I'm lazy.

First clone the repo, and set the variables in `.env` like in the manual setup.

Then, run the `gen-certs.sh` script:
```bash
./gen-certs.sh
```
### Output:
```
[+] Generating root CA...
[+] Issuing cert for mass-server...
Certificate request self-signature ok
subject=C=US, ST=PR, O=MASS, OU=MASS, CN=mass-server
```
This will create the SSL certificates needed for HTTPS

Make sure it created them correctly inside `nginx/certs`:
```
mass-server.key  mass-server.pem  rootCA.key  rootCA.pem  rootCA.srl
```
Now, you can run:
```bash
docker-compose up -d --build
```
It will download and build everything needed the first time you run it, but then it will start everything up.
You can check `https://127.0.0.1` or `https://mass.localhost` to see if it works.

You can also change the SSL certs (which is very recommended for production) for other ones from a domain you own, since these ones are self-signed you'll most likely get a warning about them not being secure, just make sure to change `nginx/default.conf` to match the domains and remove the old certs for the new ones.

To-do: Add previews of the page
