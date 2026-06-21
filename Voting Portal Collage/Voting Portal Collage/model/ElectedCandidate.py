# import db 


class ElectedCandidate:
    def __init__(self, elected_candidate_data):
        self.elected_candidate_id = elected_candidate_data.get('elected_candidate_id')
        self.candidate_id = elected_candidate_data.get('candidate_id')
        self.position_id = elected_candidate_data.get('position_id')
        self.election_id = elected_candidate_data.get('election_id')
        self.status = elected_candidate_data.get('status', 'ACTV')
        self.status_change_date = elected_candidate_data.get('status_change_date')

    def __repr__(self):
        return (f"ElectedCandidate(elected_candidate_id={self.elected_candidate_id}, "
                f"candidate_id={self.candidate_id}, position_id={self.position_id}, "
                f"election_id={self.election_id}, status='{self.status}', "
                f"status_change_date={self.status_change_date})")
