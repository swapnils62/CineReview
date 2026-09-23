# 🎬 CineReview

## 📌 Project Overview

**CineReview** is a backend REST API for a movie review platform, built with **Django** and **Django REST Framework**.

Users can register, verify their account via email OTP, authenticate with JWT, browse movies, submit ratings and reviews, maintain a personal watchlist, and report inappropriate reviews. Administrators get a separate set of APIs to manage movies, genres, actors, cast, reviews, and reports.

This project was built for hands-on practice with real-world backend development: REST API design, authentication and authorization, database relationships, serializer validation, filtering, pagination, query optimization, and API security.

---

## ✨ Features

### 👤 User Authentication & Management
- Registration with username/email/password validation
- Email OTP verification (OTP hashed at rest, expires after 10 minutes, max 5 attempts)
- JWT authentication with token refresh
- Profile retrieval, update, and account deletion

### 🎬 Movies
- Public movie listing and detail views
- Poster upload, synopsis, runtime, release date, director, genres
- Average rating (via DB aggregation)
- Search by title, filter by genre, order by release date, pagination

### ⭐ Reviews
- Authenticated create, public read
- 1–5 star rating, title + content
- One review per user per movie (enforced at DB and serializer level)
- Users can view/update/delete their own reviews

### 🔖 Watchlist
- Add / view / remove movies from a personal watchlist
- Duplicate entries prevented

### 🚩 Review Reporting
- Report categories: `spam`, `offensive`, `spoiler`
- One report per user per review
- Admins can view, filter, and update report status
- Deleting a reported review auto-marks its reports as `action_taken`

### 👨‍💼 Admin Management
Full CRUD for movies, actors, genres, and cast (with search/filter/ordering/pagination), plus review and report moderation, and bulk cast creation per movie.

---

## 🏗️ Project Structure

```text
CineReview/
├── Adminapp/       # Movie catalog + admin management (Movie, Genre, Actor, Cast)
├── Reviewapp/       # Public movie APIs + reviews/reports (Review, Reportreview)
├── Userapp/         # Auth, profile, watchlist, OTP (OTP, Watchlist)
├── CineReview/       # Project settings, urls, wsgi/asgi
├── manage.py
├── requirements.txt
└── .gitignore
```

---

## 🔐 Authentication

Uses **djangorestframework-simplejwt**.

**Login** — `POST /login/`
```json
{ "username": "your_username", "password": "your_password" }
```
Returns `{ "refresh": "...", "access": "..." }`.

**Refresh** — `POST /refresh/`
```json
{ "refresh": "your_refresh_token" }
```

---

## 📧 Signup & OTP Verification

**Signup** — `POST /signup/`
```json
{
  "username": "swapnil",
  "email": "user@example.com",
  "first_name": "Swapnil",
  "last_name": "Sarpate",
  "password": "your_password",
  "confirm_password": "your_password"
}
```
Creates the user with `is_active=False`, generates a 6-digit OTP, hashes and stores it, and emails it to the user.

**Verify OTP** — `POST /otpverify/`
```json
{ "email": "user@example.com", "code": "123456" }
```
A valid OTP activates the account.

---

## 🎥 Movie APIs

| Action | Endpoint |
|---|---|
| List movies | `GET /Movie/` → id, Title, Poster, Released_date, average_rating |
| Movie detail | `GET /Movie/{id}/` → Title, Synopsis, Runtime, Poster, Released_date, Director, average_rating, Genre_name |
| Search by title | `GET /Movie/?search=batman` |
| Filter by genre | `GET /Movie/?Genre_name=1` |
| Order by release date | `GET /Movie/?ordering=Released_date` |

All public, no auth required.

---

## ⭐ Review APIs

**Get reviews for a movie** — `GET /Movie/{movie_id}/reviews/` (newest first)

**Create review** — `POST /Movie/{movie_id}/reviews/` (auth required)
```json
{ "Title": "Great Movie", "Review": "I really enjoyed this movie.", "Rating": 5 }
```
`user` and `Movie` are assigned automatically from the request/URL. One review per user per movie is enforced.

---

## 🎭 Cast API

`GET /Movie/{movie_id}/cast/` — returns cast entries (actor, movie, character) for that movie.

---

## 🔖 Watchlist APIs

| Action | Endpoint | Auth |
|---|---|---|
| Add to watchlist | `POST /Movie/{movie_id}/Watchlist/` | Required |
| My watchlist | `GET /me/watchlist/` | Required |
| Remove item | `DELETE /me/watchlist/{id}/` | Required |

Duplicate entries for the same user/movie are prevented.

---

## 👤 User APIs (`/me/`)

| Action | Endpoint |
|---|---|
| Get profile | `GET /me/profile/` |
| Update profile | `PATCH /me/profile/` |
| Delete account | `DELETE /me/profile/` |
| My reviews | `GET /me/review/`, and retrieve/update/partial-update/delete via `/me/review/{id}/` |
| My reports | `GET /me/reports/` |

---

## 🚩 Report a Review

`POST /reviews/{review_id}/report/` (auth required)
```json
{ "reason": "This review contains offensive language.", "reasoncategorie": "offensive" }
```
Categories: `spam`, `offensive`, `spoiler`. A user can't report the same review twice.

---

## 👨‍💼 Admin APIs (`/dashboard/`, requires `IsAdminUser`)

| Resource | Endpoint | Notes |
|---|---|---|
| Movies | `/dashboard/Movieview/` | Full CRUD; filter by `Genre_name`, `Director`; search by `Title`; order by `Released_date` |
| Bulk add cast | `POST /dashboard/Movieview/{movie_id}/bulkcastadd/` | Rejects duplicate actors in the request and actors already in the cast |
| Cast | `/dashboard/Castview/` | Full CRUD |
| Actors | `/dashboard/Actorview/` | Full CRUD; actor names validated case-insensitively |
| Genres | `/dashboard/Genreview/` | Full CRUD |
| Reviews | `/dashboard/Adminreview/` | List, retrieve, delete; filter by movie. Deleting marks related reports `action_taken` |
| Reports | `/dashboard/report/` | List, retrieve, update; filter by reported review/status; order by created date |

---

## 📄 Pagination

```python
class Mypagination(PageNumberPagination):
    page_size = 10
```

Explicitly applied (10 records/page) on: public movie list, movie reviews, admin movie list, admin review list, user's own reviews, and user's own watchlist. Any endpoint that doesn't set `pagination_class` explicitly falls back to the project default — `LimitOffsetPagination`, page size 20 (set in `REST_FRAMEWORK` in `settings.py`).

---

## ⚡ Query Optimization

Review listing uses `select_related()` to avoid extra queries:
```python
Review.objects.filter(
    Movie_id=self.kwargs['movie_pk']
).select_related('user', 'Movie').order_by('-Created_at')
```
Average ratings are computed in the DB with `Avg()` rather than in Python.

---

## 🗄️ Database

SQLite for development (`django.db.backends.sqlite3`, `db.sqlite3`), excluded via `.gitignore`.

---

## 🛠️ Tech Stack

| Technology | Usage |
|---|---|
| Python | Backend language |
| Django 6.1 | Web framework |
| Django REST Framework 3.18 | REST API |
| djangorestframework-simplejwt | JWT authentication |
| django-filter | Filtering |
| Pillow | Image handling |
| django-cors-headers | CORS |
| python-dotenv | Environment variables |
| django-environ | Environment configuration |
| SQLite | Development database |
| Django Debug Toolbar | Development debugging (⚠️ see Known Issues) |
| Git / GitHub | Version control |

---

## ⚙️ Installation

**1. Clone**
```bash
git clone https://github.com/swapnils62/CineReview.git
cd CineReview
```

**2. Virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
pip install django-debug-toolbar   # not yet in requirements.txt — see Known Issues
```

**4. Configure environment variables**

Create a `.env` file in the project root (never commit this):
```env
SECRET_KEY=your_secret_key

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_google_app_password
DEFAULT_FROM_EMAIL=your_email@gmail.com
```

**5. Migrate, create superuser, run**
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

API: `http://127.0.0.1:8000/` · Django Admin: `http://127.0.0.1:8000/admin/`

---

## 🔄 Application Flow

```text
Signup → Email OTP → OTP Verification → Account Activated → JWT Login
                                                                  │
                        ┌───────────────┬────────────────┬───────┴────────┐
                        ▼               ▼                ▼                ▼
                    Reviews        Watchlist       Report Review        Profile
```
Movie browsing is public and needs no authentication.

---

## 📚 API Overview

| Area | Endpoint | Auth |
|---|---|---|
| Login | `/login/` | Public |
| Refresh Token | `/refresh/` | Public |
| Signup | `/signup/` | Public |
| OTP Verification | `/otpverify/` | Public |
| Movies | `/Movie/`, `/Movie/{id}/` | Public |
| Movie Reviews | `/Movie/{id}/reviews/` | Read public / create authenticated |
| Movie Cast | `/Movie/{id}/cast/` | Public |
| Add Watchlist | `/Movie/{id}/Watchlist/` | Authenticated |
| Report Review | `/reviews/{id}/report/` | Authenticated |
| Profile | `/me/profile/` | Authenticated |
| My Reviews | `/me/review/` | Authenticated |
| My Watchlist | `/me/watchlist/` | Authenticated |
| My Reports | `/me/reports/` | Authenticated |
| Admin Movies/Actors/Cast/Genres/Reviews/Reports | `/dashboard/...` | Admin |

---

## 🔒 Security

Sensitive config is read from environment variables and must never be committed. `.gitignore` excludes `.env`, `db.sqlite3`, `media/`, `staticfiles/`, `__pycache__/`, `*.pyc`.

For production: set `DEBUG=False`, configure `ALLOWED_HOSTS`, use HTTPS, a proper secret key, a production database, and real email credentials.

---

## 🧭 Known Issues / TODO

- `Movie`, `Genre`, `Actor`, `Cast`, `OTP`, and `Watchlist` aren't registered in Django Admin (`Adminapp/admin.py` and `Userapp/admin.py` are empty boilerplate) — only `Review` is. Not required for the API to work, but worth registering if you want to manage data through `/admin/`.
- `TokenVerifyView` is imported in `CineReview/urls.py` but has no path wired up — either add a `/verify/` route or drop the unused import.
- `DEBUG` is hardcoded to `True` in `settings.py` rather than read from the environment.

---

## 🎯 Learning Objectives

Practical experience with: REST API development with DRF, JWT auth, permissions, email OTP verification, relational DB design, serializer validation, CRUD, filtering/search/ordering, pagination, `select_related()`, ORM aggregation, secure env config, and admin-level API operations.

---

## 👨‍💻 Author

**Swapnil Sarpate**
GitHub: [github.com/swapnils62](https://github.com/swapnils62)
Repo: [github.com/swapnils62/CineReview](https://github.com/swapnils62/CineReview)