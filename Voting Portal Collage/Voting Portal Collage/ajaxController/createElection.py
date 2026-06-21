
def createElection(conn, electionName, startDate, positions):
    conn 
    positionObject = []
    cur = conn.cursor()
    cur.execute("INSERT INTO vote.elections (election_name, election_date,status,final_status) VALUES (%s, %s, %s,%s)", (electionName, startDate, 'ACTV','ACTV'))
    print("Election created")
    print(electionName)
    conn.commit()
    cur.execute("SELECT election_id FROM vote.elections WHERE election_name = %s and election_date=%s", (electionName,startDate,))
    electionId = cur.fetchone()[0]
    
    for position in positions:
        cur.execute("INSERT INTO vote.election_positions (election_id, position_id,status) VALUES (%s, %s,%s)", (electionId, position,'ACTV'))
        print("Position created %s",(position))
        positionObject.append({'positionId': position , 'candidateList': []})
    conn.commit()
    cur.close()
    conn.close()
    return electionId,positionObject