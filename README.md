# Notifier API

Notifier API is used to send notifications using email services and messenger applications. 

## Installation

```bash
git clone https://github.com/lianakalpakchyan/NOTIFIER.git
cd NOTIFIER
docker build --tag notifier .
docker run -p 127.0.0.1:80:8080/tcp notifier
```

## Usage
Accepts JSON forat data via POST method.

```json
{
    "event_type": "your type here",
    "body": "your text here",
    "to": "your email address here (optional)"
}

```

## Running Tests
The following tests can be run From NOTIFIER folder.

```bash
python -m unittest tests/unit/test_repositories.py
python -m unittest tests/unit/test_use_cases.py
python -m unittest tests/unit/test_controllers.py
```

## Status
Always can be improved :)
