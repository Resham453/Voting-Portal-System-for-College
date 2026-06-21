from flask import Blueprint, render_template,request,redirect,url_for, jsonify,current_app
import db 
from model import CandidateApplication 
from ajaxController import createElection , adminPositionDetails ,getUpdateUser,approveRegisterCandidate
import authentication as auth
from redisConn import redisConnection
import json
import pandas as pd
from flask_mail import Mail, Message
from config import Config as conf



# Define the blueprint for admin
admin_bp = Blueprint('admin', __name__)

# Admin dashboard route
@admin_bp.route('/admin/dashboard')
def dashboard():


    return render_template('admin/index.html')  # Render admin dashboard
# Admin dashboard route
@admin_bp.route('/admin/candidate')
def candidateList():
    conn = db.get_connection()
    cursor = conn.cursor()

    query = """select u.first_name ,u.last_name , ca.application_id,ca.candidate_id,p.position_name,last_year_cgpa,current_backlog_number,
            current_backlog_subjects,current_acadmic_year,current_sgpa,current_acadmic_year,candidate_stream  ,ca.status,cad.result_document,'http://localhost:5000/'||replace(cad.result_document,'\','/') ,u.email
                    from vote.candidate_applications ca , vote.candidate_application_details cad ,vote.positions p ,vote.users u
                    where ca.application_id = cad.application_id 
                    and p.position_id = ca.position_id 
                    and ca.candidate_id = u.user_id and ca.status<>'REJC' and ca.final_status<>'DONE' """
    
    cursor.execute(query)
    candidateList = cursor.fetchall()

    query = """select u.first_name ,u.last_name , ca.application_id,ca.candidate_id,p.position_name,last_year_cgpa,current_backlog_number,
            current_backlog_subjects,current_acadmic_year,current_sgpa,current_acadmic_year,candidate_stream  ,ca.status,cad.result_document,'http://localhost:5000/'||replace(cad.result_document,'\','/') ,u.email
                    from vote.candidate_applications ca , vote.candidate_application_details cad ,vote.positions p ,vote.users u
                    where ca.application_id = cad.application_id 
                    and p.position_id = ca.position_id 
                    and ca.candidate_id = u.user_id and ca.status='REJC' and ca.final_status<>'DONE' """
    
    cursor.execute(query)
    rejccandidateList = cursor.fetchall()

    return render_template('admin/adminCandidate.html',actvCandidateList=candidateList,rejcCandidateList = rejccandidateList)  # Render admin dashboard
# Admin dashboard route
@admin_bp.route('/admin/positions')
def position():
    positionList = []
    # if electionId is None:
    #     return render_template('admin/adminPosition.html',positionList)  
    positionList = adminPositionDetails.getAdminPostionData(db.get_connection())
    return render_template('admin/adminPosition.html',positionList=positionList)  # Render admin dashboard

@admin_bp.route('/admin/addElection', methods=['POST'])
def createNewElection():
    data = request.get_json()
    electionName = data['electionName']
    electionDate = data['electionDate']
    positionList = data['positionList']
    print(electionName)
    print(electionDate)
    print(positionList)
 
    electionId = createElection.createElection(db.get_connection(), electionName, electionDate, positionList)
    if electionId is None:
        return jsonify({'statusCode': 400, 'message': 'Failed to create election.'}), 200
    else:

        return jsonify({'statusCode': 200, 'message': 'Election Created'}), 200  # Redirect to admin dashboard


@admin_bp.route('/admin/userManagement')
def userManagement():

    userList = getUpdateUser.get_active_users(db.get_connection())
    return render_template('admin/userManagement.html',userList = userList)


# @admin_bp.route('/admin/votingResult')
# def votingResult():
#     votes = []
#     # Retrieve all votes from Redis queue
#     # votes = redisConnection.lrange("vote_queue",0,-1)  # Remove and get the last vote
        
#     # Convert JSON strings to a list of dictionaries
#     votes = [json.loads(vote) for vote in votes]  
#     print(votes)

#     if not votes:
#         print("No votes found in Redis.")
#         return render_template('admin/votingResult.html')

#     # Convert to Pandas DataFrame
#     df = pd.DataFrame(votes)

#     # Calculate total votes per candidate per position
#     results = df.groupby(["position_id", "candidate_id"]).size().reset_index(name="total_votes")
#     results_json = results.to_json(orient="records")
#     print(results)

#     return render_template('admin/votingResult.html',results=results_json)

@admin_bp.route('/admin/addUser',methods=['POST'])
def addUser():
    userData = request.get_json()['userData'][0]
    userId = request.get_json()['userId']
    userList=[]
    userTup = (userData['first_name'],userData['last_name'],userData['email'],userData['contact_no'],auth.encryptPassword(userData['password']),userData['status'],userData['role'])
    userList.append(userTup)

    status = getUpdateUser.create_users(db.get_connection(),userList)
    if status.status_code == 200:
        body = f"""
                Dear User,

                    Thank you for registering with us! 
                    Your account has been created successfully. 

                    You can now log in to the voting portal using the credentials below:

                    Username: {userData['email']}
                    Password: {userData['password']}

                    Please ensure to keep your login details secure. 
                    If you have any questions or need assistance, feel free to contact us.

                Best regards,
                The College Election Committee
                """   
        mail = Mail(current_app)
        emailRequestStatus = send_email(userData['email'],userData['password'],mail,body)
        
        return emailRequestStatus
    else:
        return status


@admin_bp.route('/admin/inactiveUser',methods=['POST'])
def inactiveUser():
    userId = request.get_json()['userId']
    updateObject = {'status':'INAC'}
    status = getUpdateUser.update_user_fields(db.get_connection(),userId,updateObject)

    return status


@admin_bp.route('/admin/updateUser',methods =['POST'])
def updateUser():
    userData = request.get_json()['userData'][0]
    userId = request.get_json()['userId']


    # for data in userData:
    #     userTup = (data['first_name'],data['last_name'],data['email'],data['contact_no'],auth.encryptPassword(data['password']),data['status'])
    #     userList.append(userTup)

    userData['password'] = auth.encryptPassword(userData['password'])

    status = getUpdateUser.update_user_fields(db.get_connection(),userId,userData)


    return status


@admin_bp.route('/admin/approveCandidate',methods=['POST'])
def approveCandidate():
    approveCandidate = request.get_json()['applicationList']
    unapproveCandidate = request.get_json()['unapprovedCandidateList']
    userEmailApproved = request.get_json()['approvedCandidateEmail']
    userEmailUnApproved = request.get_json()['unapprovedCandidateEmail']
    mail = Mail(current_app)
    status = approveRegisterCandidate.approve_register_candidate(db.get_connection(),approveCandidate,unapproveCandidate)
    if status.status_code == 200:
        try:

            body = conf.APPROVED_CANDIDATE
            mail = Mail(current_app)
            if userEmailApproved is not None and len(userEmailApproved) > 0:
                emailRequestStatus = send_email(userEmailApproved,'',mail,body,"Candidate application approved","Candidate application approved; However mail couldn't be send to candidate")

            body =   conf.REJECTED_CANDIDATE
            mail = Mail(current_app)
            if userEmailUnApproved is not None and len(userEmailUnApproved) > 0:
                emailRequestStatus = send_email(userEmailUnApproved,'',mail,body,"Candidate application rejected","Candidate application rejected; However mail couldn't be send to candidate")
            return jsonify({'statusCode': 200, 'redirect_url': url_for('admin.dashboard'), 'message': 'Application status updated and email sent to the candidate.','positionCandidatePairs':status.json['positionCandidatePairs'],'electionId':status.json['electionId']})
        except Exception as e:
            return jsonify({'statusCode': 400, 'redirect_url': url_for('admin.dashboard'), 'message': 'Something went wrong. The status might have been updated, but the candidate won’t receive an email.'})


@admin_bp.route("/admin/get_voting_result",methods=['GET'])
def get_result():
    allElectionRecords = db.execute_normal_query(
        '''select e.election_id,e.election_name,e.election_date::varchar,array_agg(p.position_id) as position_id_list,array_agg( p.position_name) as position_name_list,
case when election_date::date > now()::date then 'DUE' when election_date::date = now()::date then 'ONGOING' else 'DONE' end as election_complete_status 
,to_char(e.election_date,'Mon-YYYY'), e.status ,e.final_status 
from vote.elections e , vote.election_positions ep ,vote.positions p 
where e.election_id = ep.election_id 
and ep.position_id = p.position_id 
group by e.election_id,e.election_name,e.election_date '''
    )
    print(allElectionRecords)
    return render_template('admin/votingResult.html', allElectionRecords = allElectionRecords)

def send_email(user_email,password,mail,body,successMsg,failMsg):
    # Get the user email from the form data or request

    # Create the email message
    print(user_email)
    msg = Message(
        'Alard Collage Voting Portal',
        recipients=user_email,  # Add the recipient email
body=body
    )

    # Send the email
    try:
        mail.send(msg)
        return jsonify({'statusCode': 200, 'redirect_url': url_for('admin.dashboard'), 'message': successMsg})
    except Exception as e:
        return jsonify({'statusCode': 200, 'redirect_url': url_for('admin.dashboard'), 'message': failMsg})
    
@admin_bp.route('/admin/updateElectionStatus',methods=['POST'])
def updateElectionStatus():
    print(request.get_data())
    electionId = request.get_json()['electionId']
    candidateList = request.get_json()['candidateList']
    mail = Mail(current_app)


    conn = db.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("update vote.elections set final_status = 'DONE' where election_id = %s and status='ACTV'",(electionId,))
        cursor.execute("update vote.election_positions set status = 'DONE' where election_id = %s and status='ACTV'",(electionId,))
        cursor.execute("update vote.candidate_applications set final_status = 'DONE' where election_id = %s ",(electionId,))
        conn.commit()

        body = '''
Dear Candidate,

We are pleased to inform you that you have been elected for the position you stood for in the recent election.

Thank you for your participation and effort throughout the process. We wish you all the best in your upcoming responsibilities.

Congratulations once again!

Best regards,  
The College Election Committee
'''

        for candidate_id in candidateList:
            print(f"Candidate ID: {candidate_id}")

            # Use parameterized query to prevent SQL injection
            query = f"SELECT email FROM vote.users WHERE user_id = {int(candidate_id)}"
            result = db.execute_normal_query(query)

            if result:
                candidate_email = result[0][0]
                print(f"Email: {candidate_email}")

                success = send_email(
                    [candidate_email],
                    None,
                    mail,
                    body,
                    "Mail sent successfully",
                    "Mail sent unsuccessfully"
                )
            else:
                print(f"No email found for user_id {candidate_id}")
    except Exception as e:
        conn.rollback()
        return jsonify({'statusCode': 400, 'redirect_url': url_for('admin.dashboard'), 'message': 'Failed to update election status.'}), 200
    finally:

        return jsonify({'statusCode': 200, 'redirect_url': url_for('admin.dashboard'), 'message': 'Election status updated successfully.'})

@admin_bp.route('/admin/getElectionPositionList',methods=['POST'])
def getElectionPositionList():
    electionId = request.get_json()['electionId']
    try:
        print(electionId)
        # print("select ep.position_id,p.position_name from vote.election_positions ep , vote.positions p where ep.position_id = p.position_id and ep.election_id= "+electionId)
        electionPositionList = db.execute_normal_query("select ep.position_id,p.position_name from vote.election_positions ep , vote.positions p where ep.position_id = p.position_id and ep.election_id= "+str(electionId))
        print(electionPositionList)
        return jsonify({'statusCode':200,'data':electionPositionList})
    except Exception as e:
        return jsonify({'statusCode':400,'data':[]})