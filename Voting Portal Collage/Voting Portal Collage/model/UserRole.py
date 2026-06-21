class UserRole:
    def __init__(self, user_role_data):
        self.user_role_id = user_role_data.get('user_role_id')
        self.user_id = user_role_data.get('user_id')
        self.role_id = user_role_data.get('role_id')
        self.status = user_role_data.get('status')
        self.status_change_date = user_role_data.get('status_change_date')

    def __repr__(self):
        return f"UserRole(user_role_id={self.user_role_id}, user_id={self.user_id}, role_id={self.role_id}, status='{self.status}', status_change_date='{self.status_change_date}')"
