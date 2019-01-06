from django.http import HttpResponse
from ics import Calendar
import re
import requests


def strip_subject_id(event) -> str:
    event.name = re.sub(r' *[0-9A-Z]{3}\.[0-9A-Z]{3} [A-Z]* ', '', event.name)
    return event


def get_calendar(request):
    token = request.GET.get('token', '')
    url = 'https://tiss.tuwien.ac.at/events/rest/calendar/personal?token={token}'.format(token=token)
    response = requests.get(url)
    if response.status_code == 200:
        tiss_calendar = Calendar(response.text)
        tiss_calendar.events = map(strip_subject_id, tiss_calendar.events)
        return HttpResponse(tiss_calendar, content_type='text/calendar;charset=utf-8')
    else:
        return HttpResponse('Invalid Token')
