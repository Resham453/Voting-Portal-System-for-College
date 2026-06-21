from flask import Blueprint, render_template, request, current_app,session, redirect, url_for,jsonify
import authentication as auth
import db
from ajaxController import getUpdateUser
from flask_mail import Mail, Message
from config import Config as conf


# Define the blueprint for login
login_bp = Blueprint('login', __name__)



@login_bp.route('/login', methods=['GET'])
def login_page():
    requests = request.args.get('statusCode',default=200,type=int)
    statuCode = 200
    if requests is not None:
        statuCode = requests
    return render_template('login.html',statusCode=statuCode)

@login_bp.route('/register', methods=['GET'])
def register_page():
    requests = request.args.get('statusCode',default=200,type=int)
    statuCode = 200
    if requests is not None:
        statuCode = requests
    return render_template('register.html',statusCode=statuCode)

@login_bp.route('/register_user', methods=['POST'])
def register_user():
        # current_app.config['MAIL_SERVER'] = conf.SYSTEM_MAIL_SERVER  # Using Gmail's SMTP server
        # current_app.config['MAIL_PORT'] = conf.SYSTEM_MAIL_PORT  # The port for TLS
        # current_app.config['MAIL_USE_TLS'] = conf.SYSTEM_MAIL_USE_TLS  # Enable TLS
        # current_app.config['MAIL_USE_SSL'] = conf.SYSTEM_MAIL_USE_SSL  # Don't use SSL
        # current_app.config['MAIL_USERNAME'] = conf.SYSTEM_MAIL  # Your email address
        # current_app.config['MAIL_PASSWORD'] = conf.SYSTEM_MAIL_PASSWORD  # Your email password (consider using an current_app password)
        # current_app.config['MAIL_DEFAULT_SENDER'] = conf.SYSTEM_MAIL_DEFAULT_SENDER  # Default sender address

        mail = Mail(current_app)
        userData = request.get_json()['userData'][0]
        userId = request.get_json()['userId']
        userList=[]
        userTup = (userData['first_name'],userData['last_name'],userData['email'],userData['contact_no'],auth.encryptPassword(userData['password']),userData['status'],userData['prn_no'],userData['role'])
        userList.append(userTup)

        returnStatus = getUpdateUser.create_users(db.get_connection(),userList)
        if returnStatus.status_code == 200:
            emailRequestStatus = send_email(userData['email'],userData['password'],mail)
            return emailRequestStatus
        else:
            return jsonify({'statusCode': 400, 'message': 'Registration failed, please try again later.'})

@login_bp.route('/authentication', methods=['POST'])
def login():
    returnUrl = ''
    statusCode =400

    try:
        username = request.form['username']
        password = request.form['password']

        conn = db.get_connection()

        cur = conn.cursor()
        cur.execute("SELECT password,user_id FROM vote.users WHERE email = %s", (username,))
        userDetails = cur.fetchone()
        userPassword = userDetails[0]
        userId = userDetails[1]

        cur.execute("SELECT role_code FROM vote.roles r, vote.user_role ur WHERE ur.user_id=%s and ur.role_id = r.role_id", (userId,))
        # activeElection = cur.execute("SELECT election_id FROM vote.users WHERE email = %s", (username,))
        userRole = cur.fetchone()[0]

        if auth.verify_password(password, userPassword):
        # if password== userPassword:
            session['username'] = username
            if userRole=='ADMIN':
                # return redirect(url_for())
                returnUrl = 'admin.dashboard'
                statusCode = 200
            else:
                # return redirect(url_for('users.profile_page'))
                returnUrl = 'users.profile_page'
                statusCode = 200
        else:
            returnUrl = 'login.login_page'
            statusCode = 400

    except Exception as e:
        print("error while logining in...")
        # return redirect(url_for())
        returnUrl = 'login.login_page'
        
    if statusCode == 400:
        return redirect(url_for(returnUrl,statusCode=statusCode))
    
    return redirect(url_for(returnUrl))
     

@login_bp.route('/logout')
def logout():
    session.pop('username', None)  # Remove user from session
    return redirect(url_for('login.login_page'))

@login_bp.route('/getUserName')
def getUserName():
    try:
        userNameList = db.execute_query("select email,prn_no from vote.users where status='ACTV'")
        message="Got Username List"
        statusCode = 200
    except Exception as e:
        userNameList = []
        message = "Some internal error occurred"
        statusCode=400
    finally:
        print(message)
        return jsonify({'userNameList':userNameList,'statusCode':statusCode,'message':message})

def send_email(user_email,password,mail):
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
The College Election Committee
    """    
    )

    # Send the email
    try:
        mail.send(msg)
        return jsonify({'statusCode': 200, 'redirect_url': url_for('login.login_page'), 'message': 'Registration successful. Please check your email for login details.'})
    except Exception as e:
        return jsonify({'statusCode': 200, 'redirect_url': url_for('login.login_page'), 'message': 'Registration successful. However, we could not send the email. Please contact the administrator for login details.'})