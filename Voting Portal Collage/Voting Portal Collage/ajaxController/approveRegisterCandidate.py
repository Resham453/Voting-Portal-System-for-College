from  flask import jsonify

def approve_register_candidate(db_connection, applicationId,unApproveApplicationId):
    response = {"status": "failure", "message": ""}
    try:
        with db_connection.cursor() as cursor:
            # Update status in vote.candidate_application
            update_application_query = """
                UPDATE vote.candidate_applications
                SET status = 'APRV'
                WHERE application_id = ANY(%s) AND status = 'PEND'
            """
            cursor.execute(update_application_query, (applicationId,))

            # Update status in vote.candidate_application_details
            update_application_details_query = """
                UPDATE vote.candidate_application_details
                SET status = 'APRV'
                WHERE application_id = ANY(%s) AND status = 'PEND'
            """
            cursor.execute(update_application_details_query, (applicationId,))

            update_application_query = """
                UPDATE vote.candidate_applications
                SET status = 'REJC'
                WHERE application_id = ANY(%s) AND status = 'PEND'
            """
            cursor.execute(update_application_query, (unApproveApplicationId,))

            # Update status in vote.candidate_application_details
            update_application_details_query = """
                UPDATE vote.candidate_application_details
                SET status = 'REJC'
                WHERE application_id = ANY(%s) AND status = 'PEND'
            """
            cursor.execute(update_application_details_query, (unApproveApplicationId,))

        db_connection.commit()

         # Fetch electionId, candidateId, and positionId for the approved applications
        with db_connection.cursor() as cursor:

            fetch_query = """
                SELECT DISTINCT election_id
                FROM vote.candidate_applications
                WHERE application_id = ANY(%s) and status = 'APRV'
            """
            cursor.execute(fetch_query, (applicationId,))
            result = cursor.fetchall()

            # Extract data into required variables
            election_ids = result[0][0]  # Distinct election IDs

            # Fetch electionId, candidateId, and positionId for the approved applications
            fetch_query = """
                SELECT DISTINCT  position_id,array_agg(candidate_id)
                FROM vote.candidate_applications
                WHERE application_id = ANY(%s) and status = 'APRV' and election_id = %s group by position_id
            """
            cursor.execute(fetch_query, (applicationId,election_ids,))
            result = cursor.fetchall()

            # Extract data into required variables
            # election_ids = list({row['election_id'] for row in result})  # Distinct election IDs
            position_candidate_pairs = [{"positionId":row[0],"candidateList": row[1]} for row in result]  # List of tuples
        return jsonify({
            "statusCode": 200,
            "message": "Candidate applications have been successfully reviewed and updated.",
            "electionId": election_ids,
            "positionCandidatePairs": position_candidate_pairs
        })

    except Exception as e:
        db_connection.rollback()
        return jsonify({
                "statusCode": 500,
                "error": "Failed to update candidate application statuses due to a system error."
            })
    
