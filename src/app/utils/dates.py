from datetime import datetime, timedelta

def get_base_monday():
    today = datetime.today()
    return today - timedelta(days=today.weekday())

def build_week_for_students(monday_date, rows):
    today = datetime.today().strftime("%Y-%m-%d")
    week = {}

    for i in range(7):
        day = monday_date + timedelta(days=i)
        date_str = day.strftime("%Y-%m-%d")
        week[date_str] = {
            "is_today": date_str == today,
            "lessons": []
        }
    for row in rows:
        schedule_id, lesson_date, lesson_time, subject, tutor_id, status, notes, duration = row
        week[lesson_date]["lessons"].append({
            "schedule_id": schedule_id,
            "time": lesson_time,
            "subject": subject,
            "tutor_id": tutor_id,
            "status": status,
            "notes": notes,
            "duration": duration
        })

    for day in week:
        if not week[day]["lessons"]:
            week[day]["lessons"] = "Нет занятий"

    return week

def getweekdates(monday):
    return [f"{(monday + timedelta(days=i)).day} {(monday + timedelta(days=i)).strftime('%B')}" for i in range(7)]


def build_week_for_tutors(monday_date, rows):
    today = datetime.today().strftime("%Y-%m-%d")
    week = {}

    for i in range(7):
        day = monday_date + timedelta(days=i)
        date_str = day.strftime("%Y-%m-%d")
        week[date_str] = {
            "is_today": date_str == today,
            "lessons": []
        }
    
    for row in rows:
        schedule_id, lesson_date, lesson_time, subject, student_id, status, notes, duration = row
        week[lesson_date]["lessons"].append({
            "schedule_id": schedule_id,
            "time": lesson_time,
            "subject": subject,
            "student_id": student_id,
            "status": status,
            "notes": notes,
            "duration": duration
        })

    for day in week:
        if not week[day]["lessons"]:
            week[day]["lessons"] = "Нет занятий"

    return week