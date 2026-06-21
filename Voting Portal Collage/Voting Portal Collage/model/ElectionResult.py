class ElectionResult:
    def __init__(self, result_data):
        self.result_id = result_data.get('result_id')
        self.candidate_id = result_data.get('candidate_id')
        self.position_id = result_data.get('position_id')
        self.election_id = result_data.get('election_id')
        self.status = result_data.get('status')
        self.status_change_date = result_data.get('status_change_date')

    def __repr__(self):
        return (f"ElectionResult(result_id={self.result_id}, "
                f"candidate_id={self.candidate_id}, position_id={self.position_id}, "
                f"election_id={self.election_id}, status='{self.status}', "
                f"status_change_date={self.status_change_date})")
