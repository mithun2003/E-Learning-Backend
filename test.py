

# from datetime import datetime
# import pytz

# # Assuming the timestamp in your case is 1688962581
# timestamp = 1688964214

# # Define the time zone
# timezone = pytz.timezone('Asia/Kolkata')

# # Convert the timestamp to a datetime object in UTC
# utc_datetime = datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)

# # Convert the datetime object to the desired time zone
# local_datetime = utc_datetime.astimezone(timezone)

# # Format the local datetime as a string
# formatted_datetime = local_datetime.strftime('%Y-%m-%d %H:%M:%S %Z%z')

# print(formatted_datetime)


# def buying_candy(amount_of_money):
#     if amount_of_money <= 0:
#         return 0
#     if amount_of_money < 2:
#         return 1
#     dp = {
#         0: 1,
#         1: 1
#     }
#     x = 2
#     while x <= amount_of_money:
#         dp[x] = dp[x - 1] + dp[x - 2]
#         x += 1
#     return dp[amount_of_money]
# print(buying_candy(4))

# import hashlib
# import random
# import string

# def generate_secret_key(user_id):
#     # Hash the user ID using SHA-256
#     hashed_user_id = hashlib.sha256(str(user_id).encode('utf-8')).hexdigest()

#     # Set the seed for the random number generator based on the hashed user ID
#     random.seed(hashed_user_id)

#     # Generate a random string of characters for the secret key
#     secret_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

#     return secret_key

# # Example usage
# user_id = 25

# secret_key = generate_secret_key(user_id)
# print("Generated secret key for user", user_id, ":", secret_key)

# # Generating the secret key again with the same user ID will produce the same result
# secret_key = generate_secret_key(user_id)
# print("Generated secret key for user", user_id, ":", secret_key)
# secret_key = generate_secret_key(user_id)
# print("Generated secret key for user", user_id, ":", secret_key)
# secret_key = generate_secret_key(user_id)
# print("Generated secret key for user", user_id, ":", secret_key)
# secret_key = generate_secret_key(user_id)
# print("Generated secret key for user", user_id, ":", secret_key)
# secret_key = generate_secret_key(user_id)
# print("Generated secret key for user", user_id, ":", secret_key)
# secret_key = generate_secret_key(user_id)
# print("Generated secret key for user", user_id, ":", secret_key)



import hashlib
import pyotp
import random
import string

def generate_secret_key(user_id):
    # Hash the user ID using SHA-256
    hashed_user_id = hashlib.sha256(str(user_id).encode('utf-8')).hexdigest()

    # Set the seed for the random number generator based on the hashed user ID
    random.seed(hashed_user_id)

    # Generate a random base32 string for the secret key
    secret_key = ''.join(random.choices(string.ascii_uppercase + '234567', k=16))

    return secret_key

# Example usage
user_id = 25

secret_key = generate_secret_key(user_id)
print("Generated secret key for user", user_id, ":", secret_key)

# Create a TOTP object with a 30-second interval
totp = pyotp.TOTP(secret_key, interval=30)

# Generate an OTP
otp = totp.now()
print("Generated OTP:", otp)
