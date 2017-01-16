from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .forms import RegistrationForm
from .models import School, Advisor, Delegate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .alert import build_alert, do_alert


def home(request):
    return render(request, 'home.html')


def thanks(request):
    return render(request, 'thanks.html')


@login_required()
def mark_school_paid(request):
    school = School.objects.get(user_account=request.user)
    school.marked_paid_at = timezone.now()
    school.save()

    do_alert("marked school fee paid", school, request)

    return HttpResponseRedirect('/')


@login_required()
def mark_delegate_paid(request):
    school = School.objects.get(user_account=request.user)
    school.marked_paid_delegate_fee = timezone.now()
    school.save()

    do_alert("marked delegate fee paid", school, request)

    return HttpResponseRedirect('/')


@login_required()
def mark_transit_paid(request):
    school = School.objects.get(user_account=request.user)
    school.marked_paid_transit_fee = timezone.now()
    school.save()

    do_alert("marked transit fee paid", school, request)

    return HttpResponseRedirect('/')


@login_required()
def add_advisor(request):
    if request.method != 'POST':
        return HttpResponseRedirect('/')

    name = request.POST['name']
    email = request.POST['email']
    work_phone_number = request.POST['work_phone_number']
    mobile_phone_number = request.POST['mobile_phone_number']
    hotel_room_number = request.POST['hotel_room_number']
    school = School.objects.get(user_account=request.user)

    if len(name) < 1 or len(email) < 1 or len(work_phone_number) < 1 or len(mobile_phone_number) < 1 or len(hotel_room_number) < 1:
        return HttpResponseRedirect('/')
    else:
        a = Advisor(name=name, email=email, work_phone_number=work_phone_number,
                    mobile_phone_number=mobile_phone_number,
                    hotel_room_number=hotel_room_number, school=school)

        a.save()
        do_alert("added advisor", a, request)
        return HttpResponseRedirect('/')


@login_required()
def advisor_delete(request, advisor):
    a = Advisor.objects.get(pk=advisor)
    alert = build_alert("deleted advisor", a, request)
    a.delete()
    do_alert(alert)

    return HttpResponseRedirect('/')


@login_required()
def add_delegate(request):
    if request.method != 'POST':
        return HttpResponseRedirect('/')

    name = request.POST['name']
    position = request.POST['position']
    committee = request.POST['committee']
    hotel_room_number = request.POST['hotel_room_number']
    school = School.objects.get(user_account=request.user)

    if len(name) < 1 or len(position) < 1 or len(committee) < 1 or len(hotel_room_number) < 1:
        return HttpResponseRedirect('/')
    else:
        d = Delegate(name=name, position=position, committee=committee, hotel_room_number=hotel_room_number,
                     school=school)
        d.save()

        do_alert("added delegate", d, request)
        return HttpResponseRedirect('/')


@login_required()
def delegate_delete(request, delegate):
    d = Delegate.objects.get(pk=delegate)
    alert = build_alert("deleted delegate", d, request)
    Delegate.objects.get(pk=delegate).delete()
    do_alert(alert)

    return HttpResponseRedirect('/')


@login_required()
def main(request):
    try:
        school = School.objects.get(user_account=request.user)
        advisors = school.advisors.all()
        delegates = school.delegates.all()
    except:
        school = None
        advisors = None
        delegates = None

    return render(request, 'main.html', {
        'school': school,
        'advisors': advisors,
        'delegates': delegates
    })


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_account = User.objects.create_user(
                username=form.cleaned_data["initial_advisor_email"],
                email=form.cleaned_data["initial_advisor_email"],
                password=form.cleaned_data["initial_password"]
            )

            school = School(
                name=form.cleaned_data["school_name"],
                address=form.cleaned_data["school_address"],
                phone_number=form.cleaned_data["school_phone"],
                delegate_count_estimate=form.cleaned_data["rough_number_of_delegates"],
                transportation_required=form.cleaned_data["transportation_required"],
                interested_crisis_committees=form.cleaned_data["crisis_interested"],
                interested_ipd_positions=form.cleaned_data["ipd_position_interested"],
                top_three_positions="%s\n%s\n%s" % (
                    form.cleaned_data["country_pref_1"],
                    form.cleaned_data["country_pref_2"],
                    form.cleaned_data["country_pref_3"]
                ),
                user_account=new_account,
                additional_registration_notes=form.cleaned_data["additional_notes"]
            )

            school.save()

            init_advisor = Advisor(
                name=form.cleaned_data["initial_advisor_name"],
                email=form.cleaned_data["initial_advisor_email"],
                mobile_phone_number=form.cleaned_data["initial_advisor_mobile_phone"],
                school=school
            )

            init_advisor.save()

            # Send initial email
            msg = """
Thank you for registering to attend MUNI XXII!

We look forward to making our conference a fantastic experience for both you and your delegates. Below you will find your login and password for our Advisor Network. Within two days, you will receive an invoice outlining all required fees you must pay to attend our conference.

Advisor Network Login: %s

Advisor Network Password: %s

The link to login is: http://advisornetwork.muni.illinoismun.org

I am excited to work with you further to make your pre-conference registration work as stress free and enjoyable as possible. Please feel free to contact me anytime with all of your MUNI related questions, comments, and concerns at registration@illinoismun.org.

Best,

John Hall
University of Illinois at Urbana-Champaign | Class of 2019
College of Liberal Arts & Sciences | Global Studies
Under Secretary General of Registration | MUNI XXII
            """ % (init_advisor.email, form.cleaned_data["initial_password"])

            email = EmailMessage(
                "MUNI XXII Registration Confirmation",
                msg,
                'tech@illinoismun.org',
                [init_advisor.email],
                ['registration@illinoismun.org', 'secgen@illinoismun.org'],
                reply_to=['registration@illinoismun.org']
            )

            email.send()

            return HttpResponseRedirect("/thanks")

    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})
