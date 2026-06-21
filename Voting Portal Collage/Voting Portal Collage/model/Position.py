class Position:
    def __init__(self, position_data):
        self.position_id = position_data.get('position_id')
        self.position_name = position_data.get('position_name')
        self.position_ranking = position_data.get('position_ranking')
        self.eligiblity = position_data.get('eligiblity')
        self.status = position_data.get('status')
        self.status_change_date = position_data.get('status_change_date')

    def __repr__(self):
        return (f"Position(position_id={self.position_id}, "
                f"position_name='{self.position_name}', position_ranking={self.position_ranking}, "
                f"status='{self.status}', status_change_date={self.status_change_date})")
