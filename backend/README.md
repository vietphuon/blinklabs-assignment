 # Backend API Web Service

## Documentation
Swagger collection:

## Prerequisites

* Python 3.10.11

Development Tool:

* `mypy`: Type hinting support
* `black`: Python formatter
* `ruff`: Linter

## Development Setup

1. Install dependencies:
```
pip install requirements.txt
```

2. Setup `.env` file. Copy from `.env.example`
```
virtualenv -p `which python3` .venv # for python 2
python3 -m venv .venv # For python3.8 and higher

source .venv/bin/activate
pip install -r requirements.txt
```

3. Start project
```
python main.py
```
