from django.core.mail import EmailMessage
from .models import School, Advisor, Delegate
from django.utils.timezone import now, localtime


def build_alert(action, obj, request):
    footer = """
-------------
Action info
-------------
Timestamp: %s
User agent: %s
IP address: %s""" % (
        localtime(now()).isoformat(),
        request.META['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in request.META else '',
        request.META['REMOTE_ADDR'] if 'REMOTE_ADDR' in request.META else ''
    )

    if isinstance(obj, School):
        subject = "MUNI Advisor Network Alert: \"%s\" %s" % (obj.name, action)
        msg = """
%s %s via the MUNI Advisor Network.
""" % (obj.name, action)
    elif isinstance(obj, Delegate) or isinstance(obj, Advisor):
        subject = "MUNI Advisor Network Alert: \"%s\" %s" % (obj.school.name, action)
        msg = """
\"%s\" %s \"%s\"
""" % (obj.school.name, action, obj.name)
    else:
        raise RuntimeError("Invalid object type passed to build_alert")

    email = EmailMessage(
        "MUNI XXII Alert: %s" % subject,
        msg + footer,
        'tech@illinoismun.org',
        ['registration@illinoismun.org'],
        ['tech@illinoismun.org']
    )

    return email


def print_q_alert():
    email = EmailMessage(
        "MUNI Alert: Document Added for Printing",
        "(see subject)",
        'tech@illinoismun.org',
        ['tech@illinoismun.org'],
    )

    return email


def do_alert(*args):
    if len(args) == 3:
        alert = build_alert(args[0], args[1], args[2])
    elif len(args) == 1:
        alert = args[0]
    else:
        raise RuntimeError("Invalid use of do_alert, expected 1 or 3 arguments but got %d" % len(args))

    alert.send()
