from datetime import datetime, timedelta

import pytest

from app.logic import (
    create_id,
    verstka,
    verstkaprofile,
    gethwstatus,
    get_base_monday,
    build_week_for_students,
    build_week_for_tutors,
    getweekdates,
    check_answer,
    gettestanswersandtime,
)


# ---------- create_id ----------

def test_create_id_returns_int():
    value = create_id()
    assert isinstance(value, int)


def test_create_id_in_expected_range():
    value = create_id()
    assert 1_000_000 <= value <= 100_000_000_000_000


def test_create_id_randomness():
    ids = {create_id() for _ in range(100)}
    assert len(ids) > 90  # почти все должны быть уникальны


# ---------- verstka ----------

def test_verstka_replaces_name():
    template = "Hello, {{ name }}!"
    result = verstka(template, "Ivan")
    assert result == "Hello, Ivan!"


def test_verstka_no_placeholder():
    template = "Hello!"
    result = verstka(template, "Ivan")
    assert result == "Hello!"


# ---------- verstkaprofile ----------

def test_verstkaprofile_all_replacements():
    template = "{{ name }} {{ first_name }} {{ last_name }} {{ avatar }}"
    result = verstkaprofile(template, "user", "Ivan", "Petrov")

    assert "user" in result
    assert "Ivan" in result
    assert "Petrov" in result
    assert "IP" in result


# ---------- gethwstatus ----------

def test_gethwstatus_active_future_deadline():
    future = (datetime.now() + timedelta(days=1)).isoformat()
    assert gethwstatus(future) == "Активно"


def test_gethwstatus_finished_past_deadline():
    past = (datetime.now() - timedelta(days=1)).isoformat()
    assert gethwstatus(past) == "Завершено"


def test_gethwstatus_invalid_date():
    assert gethwstatus("not-a-date") == "Активно"


# ---------- get_base_monday ----------

def test_get_base_monday_is_monday():
    monday = get_base_monday()
    assert monday.weekday() == 0  # Monday = 0


# ---------- getweekdates ----------

def test_getweekdates_length():
    monday = datetime(2024, 1, 1)
    dates = getweekdates(monday)
    assert len(dates) == 7


def test_getweekdates_content():
    monday = datetime(2024, 1, 1)
    dates = getweekdates(monday)
    assert dates[0].startswith("1")


# ---------- build_week_for_students ----------

def test_build_week_for_students_empty_rows():
    monday = datetime(2024, 1, 1)
    week = build_week_for_students(monday, [])

    assert len(week) == 7
    for day in week.values():
        assert day["lessons"] == "Нет занятий"


def test_build_week_for_students_with_lessons():
    monday = datetime(2024, 1, 1)
    rows = [
        ("2024-01-01", "10:00", "Math", 1, "active", None, 60),
    ]

    week = build_week_for_students(monday, rows)
    assert len(week["2024-01-01"]["lessons"]) == 1


# ---------- build_week_for_tutors ----------

def test_build_week_for_tutors_structure():
    monday = datetime(2024, 1, 1)
    week = build_week_for_tutors(monday, [])

    assert len(week) == 7
    for day in week.values():
        assert "is_today" in day
        assert day["lessons"] == "Нет занятий"


# ---------- check_answer ----------

def test_check_answer_text_correct():
    options = '{"correct_answer": "Python"}'
    assert check_answer("text", "python", options) is True


def test_check_answer_single_choice():
    options = '{"options": ["a", "b", "c"], "correct": 1}'
    assert check_answer("single_choice", "b", options) is True


def test_check_answer_multi_choice():
    options = '{"options": ["a", "b", "c"], "correct": [0, 2]}'
    assert check_answer("multi_choice", ["a", "c"], options) is True


def test_check_answer_wrong_type():
    assert check_answer("unknown", "x", "{}") is False


# ---------- gettestanswersandtime ----------

class FakeForm:
    def __init__(self, data):
        self.data = data

    def get(self, key, default=None):
        return self.data.get(key, default)

    def getlist(self, key):
        return self.data.get(key, [])


def test_gettestanswersandtime_text_only():
    form = FakeForm({
        "test_id": "1",
        "time_spent": "120",
        "question_id[]": ["1"],
        "answer_text[]": ["answer"],
    })

    answers, time = gettestanswersandtime(form)

    assert time == 120
    assert len(answers) == 1
    assert answers[0]["type"] == "text"
