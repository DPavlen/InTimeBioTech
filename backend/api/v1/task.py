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
    :param email_message:
    :param email: Адрес электронной почты получателя.
    :param first_name: Имя пользователя.
    :param last_name: Фамилия пользователя.
    :param otp_code: OTP-код верификации.
    """
    try:
        subject = "InTimeBioTech: OTP ."
        send_from = DEFAULT_FROM_EMAIL
        send_to = [email]

        send_mail(subject, str(email_message), send_from, send_to, fail_silently=False)
        logger.debug(f"Письмо отправлено пользователю: {send_to}")

    except Exception as error:
        logger.error(f"Непредвиденная ошибка отправки письма: {error}")
