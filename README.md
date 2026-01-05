# **RepitHub** — LMS for Tutors and Students

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge\&logo=fastapi)](https://fastapi.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge\&logo=sqlite\&logoColor=white)](https://www.sqlite.org/)
[![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge\&logo=JSON%20web%20tokens\&logoColor=white)](https://jwt.io/)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge\&logo=python\&logoColor=white)](https://www.python.org/)

**RepitHub** — это LMS-платформа для репетиторов и учеников
(расписание, задания, оценки, профили, взаимодействие).

🌐 **Live:**  [RepitHub](https://repithub.online)

---
```

.
├── README.md
├── build.mjs
├── data
│   └── basa.db
├── docs
│   ├── lighthouse.png
│   ├── plan.md
│   └── ux.md
├── package-lock.json
├── package.json
├── requirements.txt
├── dockerfile
├── .dockerignore
├── docker-compose.yml
├── src
│   └── app
│       ├── QR.py
│       ├── auth.py
│       ├── database.py
│       ├── logic.py
│       ├── main.py
│       ├── static
│       │   └── favicon.ico
│       └── templates
│           ├── auth
│           │   ├── login
│           │   │   ├── login.css
│           │   │   └── login.html
│           │   ├── loginrepfailed
│           │   │   ├── loginrepfailed.css
│           │   │   └── loginrepfailed.html
│           │   └── loginstudfailed
│           │       ├── loginstudfailed.css
│           │       └── loginstudfailed.html
│           ├── cards
│           │   ├── gradestemplate.html
│           │   ├── gradestr.html
│           │   ├── hwcard.html
│           │   ├── hwtutcard.html
│           │   ├── lesson.html
│           │   ├── nohw.html
│           │   ├── nolessons.html
│           │   ├── studcard.html
│           │   └── tutcards.html
│           ├── errors
│           │   └── error
│           │       ├── error.css
│           │       └── error.html
│           ├── findtut
│           │   ├── findtut
│           │   │   ├── findtut.css
│           │   │   └── findtut.html
│           │   ├── findtutidfailed
│           │   │   ├── findtutidfailed.css
│           │   │   └── findtutidfailed.html
│           │   └── tutlist
│           │       ├── tutlist.css
│           │       └── tutlist.html
│           ├── grades
│           │   ├── studgrades
│           │   │   ├── studgrades.css
│           │   │   └── studgrades.html
│           │   └── tutgrades
│           │       ├── tutgrades.css
│           │       └── tutgrades.html
│           ├── homeworks
│           │   └── homeworkstut
│           │       ├── homeworkstut.css
│           │       └── homeworkstut.html
│           ├── mainpages
│           │   ├── hometut
│           │   │   ├── hometut.css
│           │   │   └── hometut.html
│           │   └── mainpage
│           │       ├── mainpage.css
│           │       ├── mainpage.html
│           │       └── mainpage.ts
│           ├── profiles
│           │   ├── editstudprofile
│           │   │   ├── editstudprofile.css
│           │   │   ├── editstudprofile.html
│           │   │   └── editstudprofile.ts
│           │   ├── edittutprofile
│           │   │   ├── edittutprofile.css
│           │   │   ├── edittutprofile.html
│           │   │   └── edittutprofile.ts
│           │   ├── profiletut
│           │   │   ├── profiletut.css
│           │   │   └── profiletut.html
│           │   └── studprofile
│           │       ├── studprofile.css
│           │       └── studprofile.html
│           ├── register
│           │   ├── regstud
│           │   │   ├── regstud.css
│           │   │   └── regstud.html
│           │   └── regtut
│           │       ├── regtut.css
│           │       └── regtut.html
│           └── timetable
│               └── studtime
│                   ├── studtime.css
│                   └── studtime.html
└── start.sh

```


---

## How to run the project


### 1️⃣ Run with Docker (recommended)

```bash
git clone https://github.com/Neckser/RepitSite.git
cd RepitSite

docker compose build
docker compose up
```

или одной командой:

```bash
docker compose up --build
```
> ⚠️ Requires:
>
> * docker
> * docker-compose
---

## 🛠️ Technologies

* **Backend:** FastAPI
* **Auth:** JWT
* **Database:** SQLite
* **Frontend:** HTML / CSS / TypeScript
* **Deploy:** Docker, Nginx
* **Python:** 3.12+

---

## 📌 Status

🟢 Active development
🟡 Docker support — stable
🔵 New tutor tools (workdesk, tests) — in progress


