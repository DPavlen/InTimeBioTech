COMPANY_MARK = f"""
               С любовью,
               Команда InTimeBioTech
               """

def create_collect_confirmation_email(
    first_name, last_name, description,
):
    email_message = f"""
                    Привет, {first_name} {last_name}!
                    Вход: {description}
                    {COMPANY_MARK}
                    """
    return email_message


def create_confirmation_email(first_name, last_name):
    email_message = f"""
                    Привет, {first_name} {last_name}!
                    {COMPANY_MARK}
                    """
    return email_message
