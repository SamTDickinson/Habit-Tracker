import datetime
import uuid
from flask import Blueprint, current_app, render_template, request, redirect, url_for

pages = Blueprint("habits", __name__, template_folder="templates", static_folder="static")


def datetime_at_midnight():
    today = datetime.datetime.today()
    return datetime.datetime(today.year, today.month, today.day)


@pages.context_processor
def add_calc_date_range():
    def date_range(start: datetime.datetime):
        dates = [start + datetime.timedelta(days=diff) for diff in range(-3, 4)]
        return dates

    return {"date_range": date_range}


@pages.route("/")
def index():
    date_str = request.args.get("date")
    selected_date = datetime_at_midnight()
    if date_str:
        selected_date = datetime.datetime.fromisoformat(date_str)

    completions = [
        habit["habit"]
        for habit in current_app.db.completions.find({"date": selected_date})
    ]

    habits_on_current_date = current_app.db.habits.find({"added": {"$lte": selected_date}})
    return render_template(
        "index.html",
        habits=habits_on_current_date,
        selected_date=selected_date,
        completions=completions,
        title="Habit Tracker - Home",
    )


@pages.route("/add", methods=["GET", "POST"])
def add_habit():
    today = datetime_at_midnight()

    if request.method == "POST":
        current_app.db.habits.insert_one(
            {"_id": uuid.uuid4().hex, "added": today, "name": request.form.get("habit")}
        )

    return render_template(
        "add_habit.html",
        selected_date=today,
        title="Habit Tracker - Add Habit",
    )


@pages.post('/complete')
def complete():
    date_string = request.form.get("date")
    habit = request.form.get("habitName")
    date = datetime.datetime.fromisoformat(date_string)
    current_app.db.completions.insert_one({"date": date, "habit": habit})

    return redirect(url_for(".index", date=date_string))
