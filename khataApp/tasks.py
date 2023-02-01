from .models import DailyWage, TestTable, Worker, MonthWageGiven
import datetime

from calendar import monthrange

def add_daily_wage():
    current_date = datetime.datetime.now().date()
    num_days = monthrange(current_date.year, current_date.month)[1]
    workers = Worker.objects.all()
    for worker in workers:
        if worker.working_status == "WORKING":
            if not DailyWage.objects.filter(worker_id=worker.id, date=current_date, type="LEAVE").first():
                DailyWage.objects.create(worker_id=worker.id, amount=round(worker.salary/num_days, 2), date=current_date, type='SPEND')


def test_func():
    TestTable.objects.create(name="Harsh")