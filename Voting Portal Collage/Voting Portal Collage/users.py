from flask import Blueprint, render_template,session,request,jsonify,current_app,json
import db
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from ajaxController.registerCandidate import register_candidate
from redisConn import redisConnection



# Define the blueprint for users
users_bp = Blueprint('users', __name__)




# User profile page route
@users_bp.route('/user/profile')
def profile_page():
    db_connection = db.get_connection()

    cursor =db_connection.cursor()

    cursor.execute("select * from vote.users where email=%s",(session['username'],))
    userRecord = cursor.fetchone()

    cursor.execute("select application_id from vote.candidate_applications where election_id = (select election_id from vote.elections where status='ACTV' and final_status='ACTV') and candidate_id = (select user_id from vote.users where email=%s)",(session['username'],))
    filledApplication = cursor.fetchone()

    cursor.execute("""select  election_name, 
                            (election_date::date)::varchar as election_date,
                            array_agg ( position_name) as positions,array_agg ( p.position_id::varchar) as position_id,
                            e.election_id,string_agg(position_name,', ') as ps,
                            case when election_date::date =  now()::date then 'vote' else 'novote' end as castVote,
                   		case when election_date::date - interval '7 day' >=  now()::date then 'enroll' else 'noEnroll' end as enrollCandidate
                    from 
                    	vote.elections e , 
                    	vote.election_positions ep , 
                    	vote.positions p 
                    where 	e.election_id = ep.election_id 
                    	and p.position_id = ep.position_id 
                    	and e.status ='ACTV' and e.final_status<>'DONE'
                    	group by election_name,election_date,e.election_id 
                   """)
    
    electionDetails = cursor.fetchone()

    
    cursor.execute("""select candidate_id,p.position_id ,p.position_name , first_name || ' ' || last_name || ' { '|| candidate_stream ||', '|| current_acadmic_year || ' Year }' as candidate_name
                    	from vote.candidate_applications ca, 
                    		vote.positions p ,
                    		vote.users u ,
                    		vote.candidate_application_details cad 
                    	where 	ca.status ='APRV'
                    		and u.user_id =ca.candidate_id 
                    		and p.position_id = ca.position_id 
                    		and cad.application_id = ca.application_id 
                            and u.email <> %s and ca.final_status<>'DONE' 
                   """,(session['username'],))
    
    candidatePosition = cursor.fetchall()


    return render_template('users/profile.html',userRecord=userRecord,userElectionDetails=electionDetails,candidatePosition=candidatePosition,filledApplication=filledApplication)  # Render user profile page

@users_bp.route('/user/registerCandidate',methods=['POST'])
def registerCandidate():
    try:
        # Get data from the request
        data = request.get_json()
        
        # Extract data from the JSON payload
        candidate_data = data.get('candidateData')[0]
        userId = data.get('userId')
        
        # marksheet = candidate_data.get('marksheet')  # File path or name

        # Handle file upload (marksheet) if provided
        # marksheet_filename = None
        # if marksheet:
        #     # Save the uploaded file securely
        #     marksheet_filename = secure_filename(marksheet)
            # marksheet.save(os.path.join(current_app.config['UPLOAD_FOLDER'], marksheet_filename))
        
        # candidate_data['marksheet'] = marksheet_filename

        status = register_candidate(db.get_connection(),candidate_data=candidate_data,userId=userId)
        return status
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"statusCode": 500, "message": "Internal server error. Please try again."}), 500


@users_bp.route('/user/castVote',methods=['POST'])
def cast_vote():
    data = request.get_json()
    user_id = data.get('user_id')
    candidate_id = data.get('candidate_id')
    position_id = data.get('position_id')  # Position (e.g., President, Secretary)
    election_id = data.get('election_id')

    if not all([user_id, candidate_id, position_id, election_id]):
        return jsonify({"message": "Missing required fields","statusCode":400}), 200

    # Prevent double voting (each user can vote once per position)
    user_vote_key = f"user_vote:{user_id}:{election_id}:{position_id}"
    # redisConnection.delete(user_vote_key)
    # vote_data = redisConnection.rpop("vote_queue")
    if redisConnection.exists(user_vote_key):
        return jsonify({"message": "You have already voted for this position","statusCode":403}),200

    # Store vote in Redis list
    vote_data = json.dumps({
        "user_id": user_id,
        "candidate_id": candidate_id,
        "position_id": position_id,
        "election_id": election_id
    })
    redisConnection.lpush("vote_queue", vote_data)  # Add to Redis list
    # redisConnection.lpush("vote_queue", vote_data)  # Add to Redis list
    redisConnection.persist("vote_queue")

    # print(redisConnection.lpop("vote_queue"))


    # Mark user as voted for this position
    redisConnection.set(user_vote_key, candidate_id)

    return jsonify({"message": "Vote recorded successfully","statusCode":200}), 200

@users_bp.route('/user/UploadDocuments',methods=['POST'])
def UploadDocuments():
    try:
        user_id = request.form.get("userId")
        document_name = request.form.get("documentName")
        document_type = request.form.get("documentType")
        description = request.form.get("description")
        status = request.form.get("status")
        file = request.files.get("file")

        if not file or file.filename == "":
            return jsonify({"statusCode": 400, "message": "No file uploaded"})

        # Save file
        file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)

        return jsonify({
            "statusCode": 200,
            "message": "File uploaded successfully",
            "filePath": file_path,
            "user_id": user_id,
            "document_name": document_name,
            "document_type": document_type,
            "description": description,
            "status": status
        })

    except Exception as e:
        return jsonify({"statusCode": 500, "message": str(e)}), 500
    

@users_bp.route("/users/get_voting_result",methods=['GET'])
def get_result():
    allElectionRecords = db.execute_normal_query(
        '''select e.election_id,e.election_name,e.election_date::varchar,array_agg(p.position_id) as position_id_list,array_agg( p.position_name) as position_name_list,
case when election_date::date> now()::date then 'DUE' when election_date::date = now()::date then 'ONGOING' else 'DONE' end as election_complete_status 
,to_char(e.election_date,'Mon-YYYY'), e.status ,e.final_status 
from vote.elections e , vote.election_positions ep ,vote.positions p 
where e.election_id = ep.election_id 
and ep.position_id = p.position_id 
group by e.election_id,e.election_name,e.election_date '''
    )
    print(allElectionRecords)
    db_connection = db.get_connection()

    cursor =db_connection.cursor()

    cursor.execute("select * from vote.users where email=%s",(session['username'],))
    userRecord = cursor.fetchone()
    print(userRecord)
    print(session['username'])
     
    return render_template('users/votingResult.html',userRecord=userRecord,allElectionRecords=allElectionRecords)