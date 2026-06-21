class User:
    def __init__(self, user_data):
        self.user_id = user_data.get('user_id')
        self.first_name = user_data.get('first_name')
        self.last_name = user_data.get('last_name')
        self.email = user_data.get('email')
        self.contact_no = user_data.get('contact_no')
        self.status = user_data.get('status')
        self.status_change_date = user_data.get('status_change_date')
        self.password = user_data.get('password')

    def __repr__(self):
        return f"User(user_id={self.user_id}, first_name='{self.first_name}', last_name='{self.last_name}', email='{self.email}', contact_no={self.contact_no}, status='{self.status}', status_change_date='{self.status_change_date}', password='{self.password}')"
