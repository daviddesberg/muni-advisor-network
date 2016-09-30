from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .forms import RegistrationForm
from .models import School, Advisor


def home(request):
    return render(request, 'home.html')


def thanks(request):
    return render(request, 'thanks.html')


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
Dear %s,
Thank you for registering for MUNI XXII. To manage your registration, including advisor information and delegate rosters, you may login to the MUNI XXII Advisor Network using your email address and the password you specified at registration.
The network is accessible at http://advisornetwork.muni.illinoismun.org

Thanks,
David Desberg
USG Tech - MUNI XXII
            """ % init_advisor.name

            send_mail(
                "MUNI XXII Registration and Advisor Network Info",
                msg,
                "tech@illinoismun.org",
                [init_advisor.email],
            )

            return HttpResponseRedirect("/thanks")

    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})
