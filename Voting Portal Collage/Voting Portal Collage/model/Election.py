class Election:
    def __init__(self, election_data):
        self.election_id = election_data.get('election_id')
        self.election_name = election_data.get('election_name')
        self.election_date = election_data.get('election_date')
        self.status = election_data.get('status')
        self.status_change_date = election_data.get('status_change_date')

    def __repr__(self):
        return (f"Election(election_id={self.election_id}, "
                f"election_name='{self.election_name}', election_date={self.election_date}, "
                f"status='{self.status}', status_change_date={self.status_change_date})")
