# get-crypto-price-backend

# getting started

## virtual environment

```shell
python3 -m venv .venv
source .venv/bin/activate
```

## pip package

```
(.venv)$ pip install -r requirements.txt
```

# Run

## Create .env file

```dotenv
# .
# ├── Procfile
# ├── .... other files ....
# ├── .env   <---- this
# ├── README.md
```

### Content

```
# CHANGE THE FILE NAME TO .env

SECRET_KEY = ??
REDIS_URL = ??

# Gunicorn variables

HOST = ??
PORT = ??
```

### 生成 SECRET_KEY

```shell
python3 -c 'import secrets; print(secrets.token_hex())'
```

## Flask

### development

```shell
(.venv)$ python app.py
```

### production

```shell
(.venv)$ gunicorn wsgi:app
```