from django.conf import settings
from django.core.mail import send_mail


def _base_send_mail(subject, message, recipient_email):
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [recipient_email]

    try:
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        print(f'Błąd wysyłania maila: {e}')


def welcome_mail(user):
    subject = 'Witamy w get_doctor'
    message = (
        f'Witaj {user.first_name}!\n\n'
        'Pomyślnie utworzyłeś konto w naszym serwisie. ' 
        'Zapraszamy do dokonania pierwszej rezerwacji'
    )
    _base_send_mail(subject, message, user.email)


def appointment_confirmation(user, appointment):
    doctor_full_name = appointment.slot.doctor.get_full_name()
    visit_date = appointment.slot.start_datetime.strftime('%d.%m.%Y')
    visit_time = appointment.slot.start_datetime.strftime('%H:%M')

    subject = "Wizyta umówiona!"
    message = (
        f'Witaj {user.first_name}! \n\n'
        f'Twoja wizyta u {doctor_full_name} została zarezerwowana. \n'
        f'Termin wizyty: {visit_date} (godzina: {visit_time}).\n\n'
        'Dziękujemy za skorzystanie z naszych usług!'
    )
    _base_send_mail(subject, message, user.email)


def appointment_cancellation(user):
    pass