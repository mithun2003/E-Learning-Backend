

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


def buying_candy(amount_of_money):
    if amount_of_money <= 0:
        return 0
    if amount_of_money < 2:
        return 1
    dp = {
        0: 1,
        1: 1
    }
    x = 2
    while x <= amount_of_money:
        dp[x] = dp[x - 1] + dp[x - 2]
        x += 1
    return dp[amount_of_money]
print(buying_candy(4))