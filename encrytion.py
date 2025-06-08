import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password
import ast

def verify_password(password, hashed_password):
    # Convert the stored hash back to bytes if needed
    if isinstance(hashed_password, str):
        try:
            hashed_password = ast.literal_eval(hashed_password)
        except (SyntaxError, ValueError):
            pass

    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

# Example usage
# hashed_pw = hash_password("Balaji@123")
# is_valid = verify_password("Balaji@123", hashed_pw)
# print("Password is valid:", is_valid)
stored_hash = "b'$2b$12$NuIeLXmMGnHK0VijZlhaMOce0bD9dosbb6UWriOLwEIfyjM3mfeji'"

# Simulate password check
is_valid = verify_password("Balaji@123", stored_hash)

print("Password is valid:", is_valid)

