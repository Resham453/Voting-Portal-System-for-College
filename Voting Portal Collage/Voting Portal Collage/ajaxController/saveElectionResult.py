from flask import jsonify

def save_election_results(conn,data):
    cur = conn.cursor()
    try:
        election_id = data['election_id']
        for position in data['positionList']:
            position_id = position['positionId']
            candidates = position['candidateList']

            # Insert all candidate votes
            for c in candidates:
                cur.execute("""
                    INSERT INTO candidate_votes (candidate_id, position_id, election_id, vote_count)
                    VALUES (%s, %s, %s, %s)
                """, (c['candidateId'], position_id, election_id, c['voteCount']))

            # Get elected candidate with max voteCount
            elected = max(candidates, key=lambda x: x['voteCount'])
            cur.execute("""
                INSERT INTO elected_candidates (candidate_id, position_id, election_id, vote_count)
                VALUES (%s, %s, %s, %s)
            """, (elected['candidateId'], position_id, election_id, elected['voteCount']))

        conn.commit()
        cur.close()
        conn.close()
        return jsonify(
            {
            'statusCode': 200,
            'message': 'Election results exported to database'
            }
        )
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify(
            {
            'statusCode': 400,
            'message': 'Transaction Failed, Try Again After Sometimes.'
            }
        )