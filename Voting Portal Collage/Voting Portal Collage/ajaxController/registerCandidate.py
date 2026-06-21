from  flask import jsonify


def register_candidate(conn, candidate_data,userId):
    try:
        # Connect to your postgres DB
        cur = conn.cursor()

        # Insert data into candidate_applications table
        insert_candidate_application_query = """
        INSERT INTO vote.candidate_applications (candidate_id, position_id, election_id)
        VALUES (%s, %s, %s)
        RETURNING application_id;
        """
        cur.execute(insert_candidate_application_query, (
            userId,
            candidate_data.get('election_position'),
            candidate_data.get('election_year')
        ))
        application_id = cur.fetchone()[0]

        # Insert data into candidate_application_details table
        insert_candidate_application_details_query = """
        INSERT INTO vote.candidate_application_details (
            application_id, result_document, last_year_cgpa, current_backlog_number,
            current_backlog_subjects, current_acadmic_year, candidate_stream,
            current_sgpa, status
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cur.execute(insert_candidate_application_details_query, (
            application_id,
            candidate_data.get('document'),
            candidate_data.get('cgpa'),
            candidate_data.get('backlog_count'),
            candidate_data.get('backlog_subjects'),
            candidate_data.get('academic_year'),
            candidate_data.get('stream'),
            candidate_data.get('sgpa'),
            'PEND'
        ))

        # Commit the transaction
        conn.commit()

        return jsonify({
            "statusCode": 200,
            "message": "Candidate registered successfully"
        })

    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
        return jsonify({
            "statusCode": 500,
            "message": f"Registration unsuccessful..."
        })
    finally:
        cur.close()
        conn.close()