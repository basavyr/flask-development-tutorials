# SPS Auth Workflow - Agent Instructions

---

## PRIORITY: Issue Tracking Workflow

**At the start of each session, the agent MUST:**

1. Read the `issues.md` file in the project root
2. Identify all issues with **Status: NOT COMPLETE**
3. Address each NOT COMPLETE issue in priority order (HIGH > MEDIUM > LOW)
4. After fixing an issue, update its status in `issues.md` to **COMPLETE** and add resolution notes
5. Only after all issues are resolved should the agent proceed with other user requests

**Issue Format in issues.md:**
```
### [ISSUE-XXX] Brief title
**Status:** NOT COMPLETE | COMPLETE
**Priority:** HIGH | MEDIUM | LOW
**Reported:** YYYY-MM-DD

Description of the issue...
```

**When resolving an issue, the agent must:**
- Update the Status to COMPLETE
- Add a **Resolved:** date
- Add a **Resolution:** section explaining what was changed and which files were modified

---

## Project Details

[INSTRUCTION DETAILS]
It is important to read the project description and implementation plan; BUT do not do it literally following the strict requirements if you know other more optimal rules. WE ARE NOT EXPERTS on creating system design. YOU ARE AN EXPERT ON SYSTEM DESIGN, ARCHITECTURE OF WEB APPLICATIONS, BACKENDS; all python focused.

As a result, even though we might require some things, if they are not STRICT, then your aim is to also intervene and adjust everything such that the entire system itself is much more fluent and easy to scale, maintain, understand.

## V1 - No singularization

This version of the app will be the straightforward auth workflow.

We require a simple web application, which should only focus on an authentication workflow for a user (based on email + password). Of course, first we need a "sign-up" procedure, where we enter:
- Full name (e.g., "Robert Poenaru")
- Email address (e.g., "robert.poenaru@orange.com")
- Username (e.g., it is typically recommended to be of the form `firstname.lastname' such as robert.poenaru, but of course the user can put any username)
- Password (it needs requirements, at least 12 and max 32 characters, at least 1 digit, at least one special symbol, and at least one capital letter)
We can use sqlite db to handle everything we need, and the password we keep it hashed  (e.g., using md5).

In terms of actual website, we can use a simple web app such as Flask (we should target python + sqlite). Backend and frontend all python. It should be mandatory to make the code as most concise as possible, with a single frontend/ + backend/ dirs for the implementation.

Once user has created the account, he can login to the server, and all he needs to see is a simple basic web page with "Hello, Name/username" and a button such as a "wheel" which will go into account settings, and a button to "Sign out".

The account settings page should only focus on changing the user full name and possible to delete the account. (We can consider a scenario in which the user is an admin to its own account, thus we do not require an admin account to control other accounts).

We can call this website "SPS Auth Workflow" and we can have a footer where we mention that "Website for Auth Workflow (SPS) v1.0" and of course it would be nice to have some sort of typical "Copyright + current year".

Moreover, when the user does a successful login, on his page it would be nice to see the local time.

[IMPORTANT]
Focus on making this website very easy to scale; have the scripts very nice, concise, but customizable, such that I can take attitude myself and start to extend with more pages to navigate.

### Auth behavior on account creation

It would be crucial for our website to have the following functionality: some sort of "password strength meter/calculator", where the user as he types, based on the number of characters, there should be a meter that will start from red, and moving to the right (kind of progress bar) and become yellow as user types password, when finally going green (for strong passwords). We do not have a fixed criteria yet for determining (this will be decided later on, however we find a solution here: https://www.passwordmonster.com/#scroll). Maybe now only focus on the number of characters (e.g., lengths 0-5 is red, 5-11 is yellow, and 12-32 is green). It is important that this progress bar/strength calculation will happen on-the-fly as the user types. After the "Create Account" button is pressed by the user, then we should process the request, create new entry in the database, save all that we require, and then just redirect already the user to his main page:
- some sort of greetings, very basic but friendly
- current time
- the setting menu button that will lead user to the account settings

[LOGIN DESIGN / ACCOUNT CREATION DESIGN]
On the login page /account creation page; the user should see a toggle button that will say "Use Singularization". In its initial state, the button must be toggled in the "OFF" state, which means that the current webpage should give the indication that the webpage does not "use singularization". In this first stage of the implementation, make the button work, however, in the situation that the user actually turns on singularization, then just show some html text (probably when the page is loading will be hidden) and mention something along the line that this feature will be implemented soon.

We should also see a log within our server console, that the current page of our webapp was "upgraded to singularization". But as I said, in this first version V1 - No singularization we only show and make this informatively.

[Database design]
Regarding the database, we should stick to a very concise implementation of using sqlite and just save the required info that has been introduced by the user on the account creation. Of course it would be also useful to have some sort of user ID (that will be for our internal handling) and logically we can start with "1" as the first user id and then go further. Other additional fields that would be useful for us:
- account creation timestamp
- UUID4
- although we mentioned that we will use md5 as the hashing algorithm, make a field "hashing_algorithm" or something similar, to reflect the hashing algorithm that was used to save the password locally on the db. This will be useful later on when/if we decide to change algorithms.
- if you require other fields in this db, feel free to add
 Most probably this db should exist on our "backend" (on the local server; my laptop for testing) and the website (frontend) will add data to it.

[BACKEND DESIGN]
Since we want python, everything that we implemented must be designed in such a way to be very easy to test/reproduce locally; with debugging if required. Thus, we might consider some sort of local config file that will use environment variables and other requirements.

[LOGGING]
It is crucial to have logging; so I can track the server and see what is happening on the web app. However, we prefer simple `print()` with added strings of "INFO - ..." or "DEBUG" or "ERROR" and so on

[STRUCTURE]

We already have the backend and frontend directories, so your task is to execute everything in the required locations. If needed, additional directories/files/configs can be created.

You are expert on system design and determine yourself to fully implement this plan.