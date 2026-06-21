import bcrypt

def encryptPassword(password: str) -> str:
    salt = bcrypt.gensalt()  # Generate a salt
    hashed_password = bcrypt.hashpw(password.encode(), salt)  # Hash the password
    return hashed_password.decode()  # Convert bytes to string


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


if __name__ == "__main__":
    password = "admin"
    hashed_pw = encryptPassword(password)
    print("Hashed Password:", hashed_pw)
