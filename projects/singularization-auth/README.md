# SPS Auth Workflow

A lightweight authentication web application built with Python and Flask. This project demonstrates a complete user authentication workflow including registration, login, session management, and account administration.

## Overview

The SPS Auth Workflow application provides a straightforward authentication system where users can create accounts using their email and password, log in to access a personalized dashboard, and manage their account settings. The application is designed with scalability in mind, allowing developers to extend its functionality with additional pages and features.

This is Version 1.0, which implements the core authentication workflow without the singularization feature (placeholder toggle included for future development).

## System Architecture

The application follows a clean separation between backend logic and frontend presentation. Below is a high-level view of how the components interact:

```
┌─────────────────────────────────────────────────────────────────────┐
│                           USER BROWSER                              │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         FLASK APPLICATION                           │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────────┐  │
│  │   Routes    │───▶│   Models    │───▶│   SQLite Database       │  │
│  │  (auth.py)  │    │ (models.py) │    │   (sps_auth.db)         │  │
│  │(account.py) │    └─────────────┘    └─────────────────────────┘  │
│  └─────────────┘                                                    │
│         │                                                           │
│         ▼                                                           │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                    Jinja2 Templates                         │    │
│  │   (login.html, signup.html, dashboard.html, settings.html)  │    │
│  └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

## Directory Structure

The project is organized into two main directories. The backend contains all Python logic including the Flask application, database operations, and utility functions. The frontend holds the HTML templates and static assets.

```
singularization-auth/
│
├── backend/
│   ├── __init__.py
│   ├── app.py                 ◄── Flask application factory
│   ├── config.py              ◄── Environment-based configuration
│   ├── database.py            ◄── SQLite connection management
│   ├── models.py              ◄── User data operations
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py            ◄── Login, signup, logout
│   │   └── account.py         ◄── Dashboard, settings, delete
│   └── utils/
│       ├── __init__.py
│       ├── password.py        ◄── Hashing and validation
│       └── logger.py          ◄── Simple logging utilities
│
├── frontend/
│   ├── templates/
│   │   ├── base.html          ◄── Shared layout with header/footer
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── dashboard.html
│   │   └── settings.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── app.js         ◄── Password meter and toggle logic
│
├── run.py                     ◄── Application entry point
├── requirements.txt
├── .env.example
└── README.md
```

## Database Design

User data is stored in a SQLite database located within the backend directory. The database is created automatically when the application starts for the first time.

The users table contains the following structure:

```
┌──────────────────────────────────────────────────────────────────┐
│                           USERS TABLE                            │
├──────────────────┬───────────────┬───────────────────────────────┤
│ Column           │ Type          │ Description                   │
├──────────────────┼───────────────┼───────────────────────────────┤
│ id               │ INTEGER (PK)  │ Auto-incrementing identifier  │
│ uuid             │ TEXT          │ UUID4 for external reference  │
│ full_name        │ TEXT          │ User's display name           │
│ email            │ TEXT          │ Unique email address          │
│ username         │ TEXT          │ Unique username               │
│ password_hash    │ TEXT          │ MD5 hash of salted password   │
│ password_salt    │ TEXT          │ Unique salt per user          │
│ hashing_algorithm│ TEXT          │ Algorithm used (default: md5) │
│ created_at       │ TIMESTAMP     │ Account creation time         │
│ updated_at       │ TIMESTAMP     │ Last modification time        │
└──────────────────┴───────────────┴───────────────────────────────┘
```

The hashing_algorithm field allows for future migration to stronger hashing methods without breaking existing accounts.

## Authentication Flow

The application implements a standard authentication workflow. When a new user visits the site, they are directed to the login page where they can either sign in or navigate to the registration form.

```
                    ┌─────────────┐
                    │   Start     │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
              ┌─────│   /login    │─────┐
              │     └─────────────┘     │
              │                         │
        Has Account?              No Account?
              │                         │
              ▼                         ▼
       ┌────────────┐           ┌─────────────┐
       │ Enter      │           │  /signup    │
       │ Credentials│           │  Form       │
       └─────┬──────┘           └──────┬──────┘
             │                         │
             ▼                         ▼
       ┌────────────┐           ┌─────────────┐
       │ Validate   │           │ Validate &  │
       │ Password   │           │ Create User │
       └─────┬──────┘           └──────┬──────┘
             │                         │
             └────────────┬────────────┘
                          │
                          ▼
                   ┌─────────────┐
                   │ /dashboard  │
                   │ (Logged In) │
                   └──────┬──────┘
                          │
              ┌───────────┴───────────┐
              │                       │
              ▼                       ▼
       ┌─────────────┐         ┌─────────────┐
       │ /settings   │         │  /logout    │
       │             │         │             │
       └─────────────┘         └──────┬──────┘
                                      │
                                      ▼
                               ┌─────────────┐
                               │  /login     │
                               └─────────────┘
```

## Password Requirements

During registration, passwords must meet the following criteria to ensure adequate security. The password must be between 12 and 32 characters in length, contain at least one uppercase letter, include at least one digit, and have at least one special character.

The signup form includes a real-time password strength meter that provides visual feedback as the user types. The meter displays a red bar for passwords under 6 characters, transitions to yellow for passwords between 6 and 11 characters, and turns green once the password reaches 12 or more characters.

## Singularization Toggle

Both the login and signup pages include a toggle switch labeled "Use Singularization". In this initial version, the toggle serves as a placeholder for future functionality. When activated, the page displays a message indicating that the feature will be implemented in a future release, and the backend logs this action for tracking purposes.

## Installation and Setup

Begin by ensuring you have Python 3.10 or higher installed on your system. Navigate to the project directory and create a virtual environment to isolate the project dependencies.

```bash
cd singularization-auth
python -m venv venv
source venv/bin/activate
```

Install the required packages using pip.

```bash
pip install -r requirements.txt
```

Create your local environment configuration by copying the example file.

```bash
cp .env.example .env
```

Open the `.env` file and set a secure secret key for Flask sessions. You may generate one using Python:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Running the Application

With the environment configured, start the application using the run script.

```bash
python run.py
```

The server will start on `http://127.0.0.1:5000` by default. Open this address in your web browser to access the application. The database file will be created automatically in `backend/data/sps_auth.db` on first run.

For development with auto-reload enabled, ensure `FLASK_DEBUG=true` is set in your `.env` file.

## Configuration Options

The application reads its configuration from environment variables defined in the `.env` file.

```
FLASK_SECRET_KEY     A secure random string for session encryption
FLASK_DEBUG          Set to 'true' for development, 'false' for production
FLASK_HOST           The host address to bind (default: 127.0.0.1)
FLASK_PORT           The port number to use (default: 5000)
DATABASE_PATH        Path to the SQLite database file
```

## Extending the Application

The modular structure allows for straightforward extension. To add a new page, create a new route function in the appropriate blueprint file under `backend/routes/`, add a corresponding template in `frontend/templates/`, and register any new blueprints in `backend/routes/__init__.py` if necessary.

The base template in `frontend/templates/base.html` provides the common layout including the header with navigation and the footer with copyright information. New pages should extend this template to maintain visual consistency.

## Version Information

This is Version 1.0 of the SPS Auth Workflow, implementing core authentication functionality. The singularization feature referenced in the UI toggle will be developed in subsequent versions.

---

Website for Auth Workflow (SPS) v1.0
