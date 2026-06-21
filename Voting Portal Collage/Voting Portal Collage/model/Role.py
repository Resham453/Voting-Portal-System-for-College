class Role:
    def __init__(self, role_data):
        self.role_id = role_data.get('role_id')
        self.role_code = role_data.get('role_code')
        self.role_description = role_data.get('role_description')
        self.status = role_data.get('status')
        self.status_change_date = role_data.get('status_change_date')

    def __repr__(self):
        return f"Role(role_id={self.role_id}, role_code='{self.role_code}', role_description='{self.role_description}', status='{self.status}', status_change_date='{self.status_change_date}')"
