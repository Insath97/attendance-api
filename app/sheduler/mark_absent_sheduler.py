from apscheduler.schedulers.background import BackgroundScheduler
from app.services.attendance_services import mark_absent_students

scheduler = BackgroundScheduler()

# Schedule task every day at 11:59 PM
scheduler.add_job(mark_absent_students, "cron", hour=23, minute=59)

scheduler.start()