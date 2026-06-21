from flask import jsonify, url_for
def send_email(user_email,password,mail,Message):
    # Get the user email from the form data or request

    # Create the email message
    msg = Message(
        'Alard Collage Voting Portal',
        recipients=[user_email],  # Add the recipient email
body = f"""
Dear User,

    Thank you for registering with us! 
    Your account has been created successfully. 

    You can now log in to the voting portal using the credentials below:

    Username: {user_email}
    Password: {password}

    Please ensure to keep your login details secure. 
    If you have any questions or need assistance, feel free to contact us.

Best regards,
The Voting Portal Team
    """    
    )

    # Send the email
    try:
        mail.send(msg)
        return jsonify({'statusCode': 200, 'redirect_url': url_for('login.login_page'), 'message': 'Registration successful. Please check your email for login details.'})
    except Exception as e:
        return jsonify({'statusCode': 200, 'redirect_url': url_for('login.login_page'), 'message': 'Registration successful. However, we could not send the email. Please contact the administrator for login details.'})