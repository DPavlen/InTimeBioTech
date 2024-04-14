import logging

from celery import shared_task
from django.core.mail import send_mail
from backend.settings import DEFAULT_FROM_EMAIL
from core.email_messages import create_confirmation_email

logger = logging.getLogger(__name__)


@shared_task
def send_email_message(email, email_message):
    """
    Асинхронная задача отправки электронного сообщения.
    Отправляет электронное сообщение на указанный адрес.
    Args:
        email (str): Адрес электронной почты получателя.
        email_message (str): Текст сообщения.
    Raises:
        Exception: Если произошла ошибка при отправке письма.
    """

    try:
        subject = "InTimeBioTech: OTP ."
        send_from = DEFAULT_FROM_EMAIL
        send_to = [email]

        send_mail(subject, str(email_message), send_from, send_to, fail_silently=False)
        logger.debug(f"Письмо отправлено пользователю: {send_to}")

    except Exception as error:
        logger.error(f"Непредвиденная ошибка отправки письма: {error}")
