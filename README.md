<div align="center">

# RepitHub

**LMS-платформа для репетиторов и учеников**

Расписание, домашние задания, оценки, тесты с автопроверкой, чаты и общая доска
для совместной работы - в одном веб-приложении.

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Nginx](https://img.shields.io/badge/Nginx-009639?logo=nginx&logoColor=white)](https://nginx.org/)
[![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?logo=prometheus&logoColor=white)](https://prometheus.io/)
[![Grafana](https://img.shields.io/badge/Grafana-F46800?logo=grafana&logoColor=white)](https://grafana.com/)

**Live:** [repithub.online](https://repithub.online)

</div>

---

## Содержание

- [Возможности](#возможности)
- [Архитектура](#архитектура)
- [Технологический стек](#технологический-стек)
- [Структура репозитория](#структура-репозитория)
- [Запуск](#запуск)
- [Конфигурация](#конфигурация)

---

## Возможности

**Для ученика**

- Личный кабинет с активными домашними заданиями и ближайшими занятиями
- Просмотр расписания
- Просмотр оценок по предметам
- Прохождение тестов (single/multi choice, текстовый ответ) с автоматической проверкой
- Чат с репетитором
- Поиск и подключение к репетитору
- Профиль с биографией и базовой информацией

**Для репетитора**

- Личный кабинет со списком учеников и расписанием на сегодня
- Создание и проверка домашних заданий (текстовые и графические задания)
- Выставление оценок
- Создание тестов с разными типами вопросов
- Управление расписанием занятий
- Чат с учениками
- Профиль с предметами и опытом

**Дополнительно**

- Общая доска для совместной работы
- Лендинг с FAQ, контактами и политиками (cookies, privacy policy, terms)

## Архитектура

```
                   ┌─────────────────────────────────┐
                   │            Nginx                │
                   │  TLS, rate limit, bad-bot block │
                   └──────────────┬──────────────────┘
                                  │                  
                                  │                  
                                  ▼ 
                      ┌────────────────────┐                 
                      │       FastAPI      │  
                      │   uvicorn :8000    │  
                      │                    │   
                      │  user-facing pages │  
                      │  JWT cookie auth   │                   
                      │  WebSocket (chat,  │                 
                      │   shared board)    │                    
                      └─────────┬──────────┘  
                                │                      
                                ▼
                       ┌──────────────────────┐
                       │   PostgreSQL 15      │
                       └──────────────────────┘

      ┌────────────────────┐         ┌───────────────────┐
      │   Prometheus       │ ◄────── │ /metrics из       │
      │   :9090            │         │ FastAPI           │
      └─────────┬──────────┘         └───────────────────┘
                │
                ▼
        ┌─────────────────┐
        │   Grafana       │
        │   :3000         │
        └─────────────────┘
```

## Технологический стек

### Backend

| Слой | Технологии |
|---|---|
| Основной  | **FastAPI** (Python 3.11+), Uvicorn, `python-multipart` |
| База данных | **PostgreSQL 15**, `psycopg2-binary` (с пулом соединений) |
| Аутентификация | **PyJWT** (HS256) в `httpOnly` cookies, **bcrypt** для паролей |

### Frontend

| Слой | Технологии |
|---|---|
| Шаблоны | HTML5, CSS3 |
| Скрипты | TypeScript , JavaScript |
| Сборка | **esbuild** (`build.mjs`) |
| Качество | ESLint, Prettier, Stylelint |

### Инфраструктура

| Компонент | Назначение |
|---|---|
| **Docker** + **docker-compose** | Все сервисы в контейнерах, один `docker compose up` |
| **Nginx** | TLS-терминация (Let's Encrypt), `limit_req_zone`, фильтр user-agent для сканеров, проксирование WebSocket |
| **Prometheus** | Сбор метрик с FastAPI (`prometheus-fastapi-instrumentator`) |
| **Grafana** | Дашборды поверх Prometheus |
| **GitHub Actions** | CI: TypeScript compile + lint + esbuild |

## Структура репозитория

```
RepitSite/
├── docker-compose.yml          # FastAPI + Postgres + Prometheus + Grafana
├── dockerfile                  # multi-stage: TS-сборка → Python-runtime
├── Dockerfile.tests            # отдельный образ для pytest
├── nginx.conf                  # production-конфиг с TLS, rate limit, WS
├── prometheus.yml              # scrape-конфиг
├── build.mjs                   # esbuild-сборка фронта
├── package.json                # фронтенд-зависимости и скрипты линтера
├── requirements.txt            # Python runtime
├── requirements-tests.txt      # Python для тестов
├── .github/workflows/ci.yml    # GitHub Actions
├── docs/
│   ├── plan.md                 # планирование и риски
│   └── ux.md                   # UX-сценарии
├── tests/
│   └── unit/                   # pytest (см. раздел «Тесты»)
└── src/app/
    ├── main.py                 # точка входа FastAPI, регистрация роутеров
    ├── auth.py                 # JWT issue / verify
    ├── config.py               # настройки приложения
    ├── database.py             # подключение к Postgres, DDL, пул
    ├── db_wrapper.py           # утилиты execute / query_one / query_all
    ├── routes/                 # ~20 роутеров (по доменам: tut*, stud*, auth, admin, ...)
    ├── services/               # бизнес-логика (auth, chats, tests, homeworks, ...)
    ├── utils/                  # hash, id, dates, validation, upload, QR, templates
    ├── templates/              # HTML/CSS/JS/TS для всех страниц
```

## Запуск

### Требования

- Docker и Docker Compose
- Свободные порты `127.0.0.1`: `8000` (FastAPI), `9090`
  (Prometheus), `3000` (Grafana), `5432` (Postgres — внутри сети compose)

### Шаги

```bash
git clone https://github.com/Neckser/RepitSite.git
cd RepitSite

cp .env.example .env
# открой .env и заполни секреты (см. ниже)

docker compose up --build
```

После старта:

- FastAPI: <http://localhost:8000>
- Prometheus: <http://localhost:9090>
- Grafana: <http://localhost:3000>

## Конфигурация


| Переменная | Назначение |
|---|---|
| `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` | Параметры контейнера Postgres |
| `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` | Подключение приложения к БД |
| `GRAFANA_PASSWORD` | Пароль admin-пользователя Grafana |
| `JWT_SECRET` | Секрет для пользовательских JWT в FastAPI |
