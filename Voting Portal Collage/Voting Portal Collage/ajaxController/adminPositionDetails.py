def getAdminPostionData(conn):
    cursor = conn.cursor()
    cursor.execute("select election_id from vote.elections where status='ACTV' and final_status='ACTV'")
    electionId = cursor.fetchone()
    
    # Fix indentation here for the if statement
    if electionId is None:
        return []

    cursor.execute('''
        select
            p.position_id as position_id,
            position_name,
            ca.status as status,
            coalesce(case when ca.status ='APRV' then count(distinct application_id) end,0) as approved_count,
            count(distinct application_id) as all_request
        from
            vote.positions p left join
            vote.candidate_applications ca
        on
            ca.position_id = p.position_id and ca.final_status='ACTV'
        where p.position_id in (
            select
                position_id
            from
                vote.election_positions
            where election_id = %s  
        ) 
        group by
            p.position_id,
            position_name,
            ca.status
    ''', (electionId[0],))
    
    positions = cursor.fetchall()

    return positions
