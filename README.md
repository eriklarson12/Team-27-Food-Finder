<div align="center">

# Atlanta Food Finder

Search restaurants by name, cuisine, distance, and rating, then see them plotted on a live Google map.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.1.1-092E20?logo=django&logoColor=white)
![Google Maps](https://img.shields.io/badge/Google%20Maps-Places%20API-4285F4?logo=googlemaps&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-local-003B57?logo=sqlite&logoColor=white)

**[Team portfolio, demo video, and process writeup](https://foodfinderteamportfolio.godaddysites.com/)**

</div>

---

Atlanta Food Finder is a Django web application that helps you discover restaurants near you. You enter a name, a cuisine, a maximum distance, and a minimum rating; the app queries the Google Places API, filters and sorts the results by real geodesic distance from your browser location, and renders them as a ranked list beside an interactive map.

Every restaurant has a detail page pulling live Google data: phone number, website, price level, rating, and the five most recent reviews. Create an account and you can favorite a restaurant from that page and pull the list back up from your profile.

<!-- Screenshot: add a dashboard capture to assets/ and reference it here with alt text. -->

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Team and Process](#team-and-process)
- [Limitations](#limitations)

## Features

- **Multi-filter search:** free-text name, cuisine type, minimum rating, and maximum distance in km, applied together.
- **Distance ranking:** browser geolocation feeds a geopy geodesic calculation, and results sort nearest first.
- **Interactive map:** each result gets a marker; clicking one opens the restaurant detail page.
- **Live restaurant detail:** phone, website, price level, Google rating, and the five most recent reviews, fetched per view and cached to the local database.
- **Accounts and favorites:** register, log in, favorite a restaurant, and review the saved list from your profile.

## Tech Stack

| Layer | Choice |
|---|---|
| Backend | Django 5.1.1 (Python 3.12) |
| Data | SQLite, created locally on first migrate |
| External API | Google Places text search and place details, Google Maps JavaScript API |
| Distance | geopy geodesic |
| Templates | Django templates, django-widget-tweaks, hand written CSS |
| Auth | Django `contrib.auth` plus a custom no-spaces password validator |

## Getting Started

### Prerequisites

- Python 3.12 or newer
- A Google Cloud API key with Places API and Maps JavaScript API enabled

### Installation

```bash
git clone https://github.com/eriklarson12/Team-27-Food-Finder.git
cd Team-27-Food-Finder/restaurant_finder
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env
```

Fill in `.env` before the first run. Generate a secret key with:

```bash
.venv/bin/python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Usage

```bash
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

Open http://127.0.0.1:8000 and allow location access when the browser asks. Without it, search falls back to a default coordinate pair. The database starts empty; restaurants are saved locally as you search.

## Configuration

All configuration comes from the environment, loaded from `restaurant_finder/.env` at startup. See `.env.example`. Missing required values raise `ImproperlyConfigured` at startup rather than failing silently.

| Variable | Required | Purpose |
|---|---|---|
| `DJANGO_SECRET_KEY` | yes | Django cryptographic signing |
| `GOOGLE_MAPS_API_KEY` | yes | Places API and Maps JavaScript API |
| `DJANGO_DEBUG` | no | defaults to `False`; set `True` only locally |
| `DJANGO_ALLOWED_HOSTS` | no | comma separated; required once `DEBUG` is off |

## Team and Process

Built by a team of five for Georgia Tech CS 2340. Full writeup, demo video, and individual profiles are on the [team portfolio site](https://foodfinderteamportfolio.godaddysites.com/).

| Name | Role |
|---|---|
| Marcos San Miguel | Full Stack Developer |
| Thithiesha Mahabaduge | Full Stack Developer |
| Erik Larson | Full Stack Developer |
| Cooper Brambley | Front End Developer |
| Sam Hauck | Full Stack Developer |

The team ran sprints against written planning documents, met twice weekly for scrum, tracked tasks on a Trello board, and paired on the harder integration work. Feature branches merged through GitHub.

## Limitations

- **Search hits the Google Places API on every request.** There is no caching layer or rate limiting, so a busy page burns quota fast.
- **Filters run in Python, not in the query.** Places returns up to 20 results per text search; rating and distance filters narrow that page rather than searching a wider set.
- **SQLite and `runserver` only.** The project was built and graded as a local development app, so there is no production database, WSGI server, or deployment configuration.
- **Test coverage is empty.** Both `tests.py` files are stubs. The team relied on manual testing and code review during sprints.
