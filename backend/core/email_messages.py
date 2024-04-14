COMPANY_MARK = f"""
               С любовью,
               Команда InTimeBioTech
               """

def create_confirmation_email(first_name, last_name, otp_code):
    """."""
    email_message = f"""
                    Привет,  {first_name} {last_name} !
                    OTP-код: {otp_code} 
                    Введите этот код для аутенфикации. 
                    
                    
                    {COMPANY_MARK}
                    """
    return email_message

