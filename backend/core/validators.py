from re import match

from django.core.exceptions import ValidationError


def validate_phone_number(value):
    """
    Валидирует номер телефона.

    Проверяет, соответствует ли указанное значение формату номера телефона,
    который должен начинаться с плюса, за которым следует от одной до трех
    цифр, а затем от четырех до пятнадцати дополнительных цифр.

    Параметры:
    value (str): Строка, представляющая номер телефона.

    Исключения:
    ValidationError: Вызывается, если значение не соответствует
    формату номера телефона.

    Примеры:
    - Правильные номера телефонов: +1234567890, +44, 799999999999999
    - Неправильные номера телефонов: 1234567890, +12abc345,
    +123, +12345678901234567890
    """
    if not match(r"^\+?\d{1,3}\d{4,15}$", value):
        raise ValidationError("Введите корректный номер телефона!")