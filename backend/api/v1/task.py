import logging

from celery import shared_task
from django.core.mail import send_mail
from backend.settings import DEFAULT_FROM_EMAIL

logger = logging.getLogger(__name__)


@shared_task
def send_email_message(email, msg):
    """
    Асинхронная задача отправки электронного сообщения.
    Отправляет электронное сообщение на указанный адрес.
    :param email: Адрес электронной почты получателя.
    :param msg: Текст сообщения.
    """
    try:
        subject = "InTimeBioTech: OTP ."
        message = msg
        send_from = DEFAULT_FROM_EMAIL
        send_to = [email]

        send_mail(subject, message, send_from, send_to, fail_silently=False)
        logger.debug(f"Письмо отправлено пользователю: {send_to}")

    except Exception as error:
        logger.error(f"Непредвиденная ошибка отправки письма: {error}")
