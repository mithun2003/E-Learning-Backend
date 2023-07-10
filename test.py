

from datetime import datetime
import pytz

# Assuming the timestamp in your case is 1688962581
timestamp = 1688964214

# Define the time zone
timezone = pytz.timezone('Asia/Kolkata')

# Convert the timestamp to a datetime object in UTC
utc_datetime = datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)

# Convert the datetime object to the desired time zone
local_datetime = utc_datetime.astimezone(timezone)

# Format the local datetime as a string
formatted_datetime = local_datetime.strftime('%Y-%m-%d %H:%M:%S %Z%z')

print(formatted_datetime)
