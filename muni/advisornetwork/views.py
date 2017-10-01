from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .forms import RegistrationForm, PositionPaperForm, PrintDocumentForm
from .models import School, Advisor, Delegate, PositionPaper, PrintDocument
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .alert import build_alert, do_alert, print_q_alert
from collections import defaultdict
from .conference_data import committee_list, position_paper_committees
from django.contrib import messages


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
    messages.add_message(request, messages.INFO, 'School fee marked as paid.')
    return HttpResponseRedirect('/')


@login_required()
def mark_delegate_paid(request):
    school = School.objects.get(user_account=request.user)
    school.marked_paid_delegate_fee = timezone.now()
    school.save()

    do_alert("marked delegate fee paid", school, request)
    messages.add_message(request, messages.INFO, 'Delegates fee marked as paid.')
    return HttpResponseRedirect('/')


@login_required()
def mark_transit_paid(request):
    school = School.objects.get(user_account=request.user)
    school.marked_paid_transit_fee = timezone.now()
    school.save()

    do_alert("marked transit fee paid", school, request)
    messages.add_message(request, messages.INFO, 'Transit fee marked as paid.')
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

    if len(name) < 1 or len(email) < 1 or len(work_phone_number) < 1 or len(mobile_phone_number) < 1:
        messages.add_message(request, messages.ERROR, "Please fill out all required fields to add an advisor.")
        return HttpResponseRedirect('/')
    else:
        a = Advisor(name=name, email=email, work_phone_number=work_phone_number,
                    mobile_phone_number=mobile_phone_number,
                    hotel_room_number=hotel_room_number, school=school)

        a.save()
        do_alert("added advisor", a, request)
        messages.add_message(request, messages.INFO, 'Advisor successfully added.')
        return HttpResponseRedirect('/')


@login_required()
def advisor_delete(request, advisor):
    a = Advisor.objects.get(pk=advisor)
    if a.school != School.objects.get(user_account=request.user):
        return HttpResponseRedirect('/')
    alert = build_alert("deleted advisor", a, request)
    a.delete()
    do_alert(alert)
    messages.add_message(request, messages.INFO, 'Advisor successfully deleted.')
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

    if len(name) < 1 or len(position) < 1 or len(committee) < 1:
        messages.add_message(request, messages.ERROR, "Please fill out all required fields to add a delegate.")
        return HttpResponseRedirect('/')
    else:
        d = Delegate(name=name, position=position, committee=committee, hotel_room_number=hotel_room_number,
                     school=school)
        d.save()

        do_alert("added delegate", d, request)
        messages.add_message(request, messages.INFO, 'Delegate successfully added.')
        return HttpResponseRedirect('/')


@login_required()
def delegate_delete(request, delegate):
    d = Delegate.objects.get(pk=delegate)
    if d.school != School.objects.get(user_account=request.user):
        return HttpResponseRedirect('/')

    alert = build_alert("deleted delegate", d, request)
    Delegate.objects.get(pk=delegate).delete()
    do_alert(alert)
    messages.add_message(request, messages.INFO, 'Delegate successfully deleted.')
    return HttpResponseRedirect('/')


@login_required()
def delegate_edit(request, delegate):
    d = Delegate.objects.get(pk=delegate)
    if d.school != School.objects.get(user_account=request.user):
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        name = request.POST['name']
        position = request.POST['position']
        committee = request.POST['committee']
        hotel_room_number = request.POST['hotel_room_number']
        if len(name) < 1 or len(position) < 1 or len(committee) < 1:
            messages.add_message(request, messages.ERROR, "Please fill out all required fields to edit a delegate.")
            return HttpResponseRedirect('/')
        d.name = name
        d.position = position
        d.committee = committee
        d.hotel_room_number = hotel_room_number
        d.save()
        messages.add_message(request, messages.INFO, 'Delegate successfully edited.')

        return HttpResponseRedirect('/')

    return render(request, 'editpage.html', {
        'obj': d,
        'edit_type': 'delegate',
        'committee_list': committee_list,
    })


@login_required()
def advisor_edit(request, advisor):
    a = Advisor.objects.get(pk=advisor)
    if a.school != School.objects.get(user_account=request.user):
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        work_phone_number = request.POST['work_phone_number']
        mobile_phone_number = request.POST['mobile_phone_number']
        hotel_room_number = request.POST['hotel_room_number']

        if len(name) < 1 or len(email) < 1 or len(work_phone_number) < 1 or len(mobile_phone_number) < 1:
            messages.add_message(request, messages.ERROR, "Please fill out all required fields to edit an advisor.")
            return HttpResponseRedirect('/')

        a.name = name
        a.email = email
        a.work_phone_number = work_phone_number
        a.mobile_phone_number = mobile_phone_number
        a.hotel_room_number = hotel_room_number
        a.save()

        messages.add_message(request, messages.INFO, 'Advisor successfully edited.')

        return HttpResponseRedirect('/')

    return render(request, 'editpage.html', {
        'obj': a,
        'edit_type': 'advisor'
    })


def print_q_submit(request):
    if request.method == 'POST':
        doc_form = PrintDocumentForm(request.POST, request.FILES)
        if doc_form.is_valid():
            doc = doc_form.save()
            alert = print_q_alert()
            alert.send()
            messages.add_message(request, messages.INFO, 'Document queued for printing.')

            return HttpResponseRedirect('/print')

    doc_form = PrintDocumentForm()
    return render(request, 'print.html', {
        'form': doc_form
    })


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

    if request.method == 'POST':
        pos_paper_form = PositionPaperForm(request.POST, request.FILES, school=school)
        if pos_paper_form.is_valid():
            paper = pos_paper_form.save()
            do_alert("uploaded position paper for %s" % (paper.delegate.name), school, request)
            messages.add_message(request, messages.INFO, 'Position paper added.')
            return HttpResponseRedirect('/')
        else:
            messages.add_message(request, messages.ERROR, 'Please select a delegate and upload a PDF or Word document.')
            return HttpResponseRedirect('/')

    pos_paper_form = PositionPaperForm(school=school)

    return render(request, 'main.html', {
        'school': school,
        'advisors': advisors,
        'delegates': delegates,
        'pos_paper_form': pos_paper_form,
        'committee_list': committee_list
    })


def position_papers(request):
    # use the latest for each delegate, so uploads can replace older ones
    temp = PositionPaper.objects.all()
    papers = []
    by_delegate = defaultdict(lambda: [])
    for paper in temp:
        by_delegate[paper.delegate].append(paper)

    for per_delegate in by_delegate.values():
        per_delegate = sorted(per_delegate, key=lambda p: p.updated_at, reverse=True)
        papers.append(per_delegate[0])

    by_cmt = defaultdict(lambda: [])
    for cmt in position_paper_committees:
        by_cmt[cmt] = []

    for paper in papers:
        by_cmt[paper.delegate.committee].append(paper)

    return render(request, 'positionpapers.html', {
        'papers': list(by_cmt.items()),
        'cmt': position_paper_committees
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
You have successfully registered for MUNI XXIII.

We look forward to making this conference the best one yet! Within a few days, you will
receive an invoice regarding all necessary fees. Below is your Advisor Network information.

Advisor Network Login: %s

Advisor Network Password: %s

The link to login is: http://advisornetwork.muni.illinoismun.org

I am very excited to begin working with you to make your pre-conference work as easy and
stress free as possible. If you have any questions, comments, or concerns, please don’t hesitate
to contact me at registration@illinoismun.org.

Best,

Daniel Benson
University of Illinois at Urbana-Champaign | Political Science '20
Undersecretary-General of Registration | MUNI XXIII
Chick Evans Caddie Scholar
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
