from flask import Flask , request, render_template, redirect, url_for, session
from flask_assets import Environment, Bundle
import authentication as auth
import secrets
import db 
from login import login_bp
from admin import admin_bp
from users import users_bp
import os
from redisConn import redisConnection
from config import Config as conf
from web3 import Web3
import json
from voting import voting_bp
from ajaxController import adminPositionDetails

app = Flask(__name__)

app.config['MAIL_SERVER'] = conf.SYSTEM_MAIL_SERVER  # Using Gmail's SMTP server
app.config['MAIL_PORT'] = conf.SYSTEM_MAIL_PORT  # The port for TLS
app.config['MAIL_USE_TLS'] = conf.SYSTEM_MAIL_USE_TLS  # Enable TLS
app.config['MAIL_USE_SSL'] = conf.SYSTEM_MAIL_USE_SSL  # Don't use SSL
app.config['MAIL_USERNAME'] = conf.SYSTEM_MAIL  # Your email address
app.config['MAIL_PASSWORD'] = conf.SYSTEM_MAIL_PASSWORD  # Your email password (consider using an app password)
app.config['MAIL_DEFAULT_SENDER'] = conf.SYSTEM_MAIL_DEFAULT_SENDER  # Default sender address



UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.secret_key = secrets.token_hex(24)

assets = Environment(app)

# Define a SCSS to CSS bundle
scss_bundle = Bundle('scss/base.scss', filters='scss', output='css/admin/base.css')
assets.register('scss_all', scss_bundle)

app.register_blueprint(login_bp, url_prefix='/')
app.register_blueprint(admin_bp, url_prefix='/')
app.register_blueprint(users_bp, url_prefix='/')
# Register blueprint
app.register_blueprint(voting_bp, url_prefix='/voting')

@app.context_processor
def inject_globals():
    
    # Add common data here
    electionList = db.execute_query("select election_id,election_name, TO_CHAR(election_date, 'Mon-YYYY') election_period from vote.elections ")
    electionDetails = db.execute_query("select *,case when election_date::date > now()::date then 'DUE' when election_date::date = now()::date then 'ONGOING' else 'DONE' end  from vote.elections where status='ACTV' and final_status='ACTV'")
    
    applicationList = db.execute_query("select * from vote.candidate_applications where final_status<>'DONE'")
    approvedApplicationList = db.execute_query("select * from vote.candidate_applications where status='APRV' and final_status='ACTV'")
    positionList = db.execute_query("select * from  vote.positions p where p.status ='ACTV'")
    currentPositionList = db.execute_normal_query("select * from  vote.positions p where p.status ='ACTV' and position_id in (select position_id from vote.election_positions where status='ACTV')")
    usersList = db.execute_query("select * from vote.users where email <> 'admin@gmail.com'")
    checkUsersList = db.execute_normal_query("select user_id,first_name || ' ' || last_name  from vote.users where email <> 'admin@gmail.com'")
    user_name = session['username'] if 'username' in session else None
    allUserName = db.execute_query("select email,prn_no from vote.users where status='APRV'")
    adminPositionList = adminPositionDetails.getAdminPostionData(db.get_connection())

    return {
        'user_name': user_name,
        'applicationList' : applicationList,
        'allPositionList' : positionList,
        'userList' : usersList,
        'approvedApplicationList':approvedApplicationList,
        'currentPositionList' : currentPositionList,
        'mappingUserList':checkUsersList,
        'electionDetails': electionDetails,
        'allUserName':allUserName,
        'electionList':electionList,
        'adminPositionList':adminPositionList
        }

@app.before_request
def require_login():

    if request.endpoint and request.endpoint.startswith('static'):
        return None  # Allow access to static files
    # Skip the login route (allow unauthenticated users to access the login page)
    if request.endpoint in ['login.login_page','login.register_page','login.register_user','login.login','login.getUserName']:
        return None  # Allow access to the login page
    
    # Check if user is not logged in for all other routes
    if 'username' not in session:
        return redirect(url_for('login.login_page'))  # Redirect to login page if not authenticated

@app.route('/')
def index():
    return redirect(url_for('login.login_page'))



if __name__ == "__main__":
    app.run(debug=True)
