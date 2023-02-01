from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
from django.db.models import Avg, Count, Min, Sum
from .serializers import DailyWageSerializer
from .decorators import unauthenticated_user
from .models import Worker, DailyWage, MonthWageGiven
from django.views.decorators.csrf import csrf_exempt
from calendar import monthrange

# Create your views here.


@unauthenticated_user
def index(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        print(password)
        user = authenticate(request=request, phone=phone, password=password)
        if user:
            login(request=request, user=user)
            return redirect('home')
        else:
            messages.error(request, 'Please provide correct credentials')
            return redirect('login')
    return render(request, 'index.html')


def year_month_format(date):
    return datetime.datetime.strptime(date, "%Y-%m")


@login_required(login_url='/')
def home(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        address = request.POST.get("address")
        salary = request.POST.get("salary")
        doj = request.POST.get('doj')
        worker_obj = Worker(name=name, email=email, phone=phone if phone else None,
                            address=address, salary=float(salary), doj=doj)
        try:
            worker_obj.save()
            messages.success(request, "Worker added successfully!")
        except Exception as e:
            print(e)
            messages.error(request, "Something went wrong")
        return redirect('home')
    workers = Worker.objects.all()
    daily_wage = DailyWage.objects.filter(date__month=datetime.datetime.now().date().month)
    spend_wage = daily_wage.filter(type="SPEND").aggregate(total_spend=Sum('amount')).get("total_spend", 0.0)
    given_wage = daily_wage.filter(type="GIVEN").aggregate(total_given=Sum('amount')).get("total_given", 0.0)
    context = {
        "workers": workers,
        "spend_wage": spend_wage if spend_wage else 0.0,
        "given_wage": given_wage if given_wage else 0.0,
    }
    return render(request, "home.html", context)


@login_required(login_url='/')
def logoutUser(request):
    logout(request=request)
    return redirect('login')


@login_required(login_url='/')
def workerPage(request, id):
    monYear = datetime.datetime.now().date()
    strMonYear = datetime.datetime.strftime(monYear, "%Y-%m")
    print(strMonYear)
    month_wage = MonthWageGiven.objects.filter(
        worker_id=id, month=strMonYear).first()
    daily_wage = DailyWage.objects.filter(
        worker_id=id, date__month=monYear.month, date__year=monYear.year).order_by('date')
    spend_money = daily_wage.filter(
        type="SPEND").aggregate(total_spend=Sum('amount'))
    given_money = daily_wage.filter(
        type="GIVEN").aggregate(total_given=Sum('amount'))
    spend_money = round(spend_money['total_spend'] if spend_money['total_spend'] else 0.0, 2)
    given_money = round(given_money['total_given'] if given_money['total_given'] else 0.0, 2)
    total = spend_money + given_money
    worker_obj = Worker.objects.filter(id=id).first()
    if worker_obj:
        return render(request, 'worker.html', context={
            "worker": worker_obj,
            "wages": daily_wage,
            "spend_money": spend_money,
            "given_money": given_money,
            "isPayDone": True if month_wage else False,
            "total": total,
        })
    else:
        return HttpResponse("Not found")


@login_required(login_url='/')
@csrf_exempt
def monthWages(request):
    if request.method == "POST":
        id = request.POST.get("id")
        date = request.POST.get("date")
        monYear = datetime.datetime.strptime(date, "%Y-%m")
        month_wage = MonthWageGiven.objects.filter(
            worker_id=id, month=date).first()
        daily_wage = DailyWage.objects.filter(
            worker_id=id, date__month=monYear.month, date__year=monYear.year).order_by('date')
        spend_money = daily_wage.filter(
            type="SPEND").aggregate(total_spend=Sum('amount'))
        given_money = daily_wage.filter(
            type="GIVEN").aggregate(total_given=Sum('amount'))
        spend_money = round(spend_money['total_spend'] if spend_money['total_spend'] else 0.0, 2)
        given_money = round(given_money['total_given'] if given_money['total_given'] else 0.0, 2)
        total = spend_money + given_money
        return JsonResponse({"data": {"daily_wage": DailyWageSerializer(daily_wage, many=True).data,
                                      "spend_money": str(spend_money),
                                      "given_money": str(given_money),
                                      "isPayDone": True if month_wage else False,
                                      "total": str(total),
                                      }})


@login_required(login_url='/')
def updateProfile(request):
    if request.method == "POST":
        id = request.POST.get("id")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        address = request.POST.get("address")
        salary = request.POST.get("salary")
        worker_obj = Worker.objects.filter(id=id).first()
        if worker_obj:
            worker_obj.name = name
            if phone:
                worker_obj.phone = int(phone)
            worker_obj.email = email
            worker_obj.address = address
            if worker_obj.salary != float(salary):
                current_date = datetime.datetime.now().date()
                num_days = monthrange(current_date.year, current_date.month)[1]
                DailyWage.objects.filter(date__month=current_date.month, type='SPEND').update(amount=round(float(salary)/num_days, 2))
                DailyWage.objects.filter(date__month=current_date.month, type='LEAVE').update(amount=round(float(salary)/30, 2))
                worker_obj.salary = float(salary)
            worker_obj.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('/worker/'+id+'/')
        else:
            messages.error(request, "Something went wrong!")
            return redirect('/worker/'+id+'/')


@login_required(login_url='/')
def updateGiven(request):
    if request.method == "POST":
        id = request.POST.get("id")
        date = request.POST.get("date")
        amount = request.POST.get("amount")
        reason = request.POST.get("reason")
        type = request.POST.get("type")
        worker_obj = Worker.objects.filter(id=id).first()
        if type == "GIVEN":
            dw_obj = DailyWage(worker_id=id, amount=amount,
                            date=date, reason=reason, type='GIVEN')
        elif type == "LEAVE":
            dw_obj = DailyWage.objects.filter(worker_id=id, date=date, type="SPEND").first()
            if dw_obj:
                dw_obj.type = "LEAVE"
                dw_obj.reason = "LEAVE"
                dw_obj.amount = round(worker_obj.salary/30, 2)
            else:
                dw_obj = DailyWage(worker_id=id, amount=round(worker_obj.salary/30, 2),
                                date=date, reason="LEAVE", type='LEAVE')
        dw_obj.save()
        messages.success(request, "Amount added successfully!")
        return redirect('/worker/'+id+'/')


@login_required(login_url='/')
@csrf_exempt
def updatePayment(request):
    if request.method == "POST":
        id = request.POST.get("id")
        date = request.POST.get("date")
        givenMoney = request.POST.get("givenMoney")
        spendMoney = request.POST.get("spendMoney")
        monYear = datetime.datetime.strptime(date, "%Y-%m")
        monYearString = datetime.datetime.strftime(monYear, "%B, %Y")
        mon_wage = MonthWageGiven(worker_id=id, amount=float(
            spendMoney), pre_amount=float(givenMoney), month=date)
        mon_wage.save()
        messages.success(request, "Payment done for "+monYearString)
        return JsonResponse({"data": "data"})
