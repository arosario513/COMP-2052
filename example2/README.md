# Example 2

## Table of Contents

- [Intro](#intro)
- [File Structure](#file-structure)
- [Setup](#setup)

## Intro
This example is to show how a login with flask would work. It uses flask-SQLAlchemy for the database.

## File Structure
```
example2
├── instance
│   └── db.sqlite
├── main.py
├── models
│   ├── __init__.py
│   └── user.py
├── requirements.txt
└── templates
    ├── base.html
    ├── dashboard.html
    ├── footer.html
    ├── header.html
    ├── index.html
    ├── login.html
    └── register.html
```
## Setup
```bash
mkdir example
cd example
git init
git branch -m main
git remote add origin https://github.com/arosario513/COMP-2052.git
git sparse-checkout init
git sparse-checkout add example2
git pull origin main
```
Then go to `example2`:

```bash
cd example2
```
Create an .env file with the `SECRET_KEY`
I'll use this python one-liner to create the key and save it to `.env`. This is necessary otherwise `main.py` will complain about not setting `SECRET_KEY`:
```bash
python -c 'import secrets; SECRET_KEY=secrets.token_urlsafe(32);print(f"{SECRET_KEY=}")' > .env
```

Setup the python virtual environment:

### Linux/Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```powershell
python3 -m venv venv
venv\Scripts\activate.bat
```

Finally, install the required modules:

```bash
pip install -r requirements.txt
```

After that you should be good to go. Just run `python main.py` and the server should boot up

**Note:** the default server is http://127.0.0.1:5000
