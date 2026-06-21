class CandidateApplication:
    def __init__(self, application_data):
        self.application_id = application_data.get('application_id')
        self.candidate_id = application_data.get('candidate_id')
        self.position_id = application_data.get('position_id')
        self.election_id = application_data.get('election_id')
        self.application_date = application_data.get('application_date')
        self.status = application_data.get('status', 'PEND')  # Default to 'PEND' if not provided
        self.status_change_date = application_data.get('status_change_date')

    def __repr__(self):
        return (f"CandidateApplication(application_id={self.application_id}, "
                f"candidate_id={self.candidate_id}, position_id={self.position_id}, "
                f"election_id={self.election_id}, application_date={self.application_date}, "
                f"status='{self.status}', status_change_date={self.status_change_date})")
