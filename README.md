# PulseLog

Built out of personal frustration — every health app is either paywalled, or just missing half the things you actually need. So I built my own.

PulseLog tracks calories, weight trends, and daily habits in one place. Nothing more, nothing less. Built for me and my friends while learning the entire stack from scratch FastAPI, PostgreSQL, JWT auth, and deployment ,all in under 3 months of coding.

🔗 **[Live App](https://resonant-kringle-307e9a.netlify.app)**  
🔗 **[API Docs](https://pulse-log.onrender.com/docs)**

---

## Features

- **Calorie Tracking** — search any food using the USDA FoodData Central database, log quantity, and automatically get calories, protein, carbs, and fats
- **Weight Tracking** — log your weight daily and visualize trends over time with a smooth line chart
- **BMI Calculator** — automatically calculated from your profile data, with category (Underweight / Normal / Overweight)
- **Habit Tracking** — create habits and track them daily
- **User Auth** — secure registration and login with JWT authentication and bcrypt password hashing
- **Persistent Data** — PostgreSQL database, data never resets

---

## Tech Stack

**Backend**
- Python + FastAPI
- PostgreSQL (via SQLAlchemy ORM + psycopg2)
- Alembic for database migrations
- JWT authentication (python-jose)
- bcrypt password hashing (passlib)
- USDA FoodData Central API for nutritional data

**Frontend**
- Vanilla HTML, CSS, JavaScript — no frameworks
- Canvas API for weight charts
- PWA-ready

**Deployment**
- Backend → Render
- Frontend → Netlify
- Database → Render PostgreSQL

---

## Architecture

```
Browser (Netlify CDN)
        ↓  fetch() with JWT Bearer token
Render Server — uvicorn + FastAPI
        ↓
SQLAlchemy ORM
        ↓
PostgreSQL (Render, Singapore)
        ↓  (for calorie lookups)
USDA FoodData Central API
```

---

## API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/registration` | Create new account | No |
| POST | `/login` | Login, returns JWT token | No |
| GET | `/me` | Get current user profile | Yes |
| GET | `/bmi` | Get BMI and category | Yes |
| POST | `/weight` | Log a weight entry | Yes |
| GET | `/weight` | Get all weight logs | Yes |
| POST | `/calorielog` | Log food (searches USDA API) | Yes |
| GET | `/calorielog` | Get all calorie logs | Yes |
| POST | `/habit` | Create a habit | Yes |
| GET | `/habit` | Get all habits | Yes |
| POST | `/habit/log` | Log a habit completion | Yes |
| GET | `/habit/log` | Get all habit logs | Yes |

---

## Local Development

**Prerequisites**
- Python 3.10+
- PostgreSQL (or use SQLite for local testing)

**Setup**

```bash
# Clone the repo
git clone https://github.com/gunavardhanra-dev/pulse_log
cd pulse_log

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create back/.env with:
# SECRET_KEY=your_secret_key
# USDA_API_KEY=your_usda_key
# DATABASE_URL=your_postgresql_url

# Run migrations
alembic -c back/alembic.ini upgrade head

# Start the server
uvicorn back.main:app --reload
```

**Frontend**

Open `front/login.html` with Live Server in VS Code.

---

## Project Structure

```
pulse_log/
├── back/
│   ├── main.py          # FastAPI app, all routes
│   ├── models.py        # SQLAlchemy database models
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── auth.py          # JWT authentication logic
│   ├── database.py      # Database connection setup
│   ├── migrations/      # Alembic migration files
│   └── .env             # Environment variables (not committed)
├── front/
│   ├── index.html       # Home dashboard
│   ├── login.html       # Login page
│   ├── register.html    # Registration page
│   ├── weight.html      # Weight history page
│   └── profile.html     # User profile page
└── requirements.txt
```

---

## Roadmap

- [ ] Food search autocomplete
- [ ] Meal type tagging (breakfast / lunch / dinner)
- [ ] Workout tracking
- [ ] AI-integrated health coach
- [ ] Social features — follow friends, compare weekly stats
- [ ] Mobile app (React Native)

---

## Author

[Gunavardhan](https://github.com/gunavardhanra-dev) — 3rd year engineering student, started coding 3 months ago, building toward backend development and a Masters in Germany. This is project 1.
