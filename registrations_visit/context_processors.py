from datetime import date

def current_date(request):
    return {
        'today': date.today()
    }