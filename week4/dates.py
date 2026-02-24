#1
from datetime import date, timedelta

today = date.today()
new_date = today - timedelta(days=5)

print("Today's date:", today)
print("Date 5 days ago:", new_date)

#2
from datetime import date, timedelta

today=date.today()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("Yesterday is",yesterday)
print("Today is",today)
print("Tomorrow is",tomorrow)

#3
from datetime import datetime

now = datetime.now()
print("Original datetime:", now)

now_no_microseconds = now.replace(microsecond=0)
print("Datetime without microseconds:", now_no_microseconds)

#4
from datetime import datetime

date1_str = input("Enter the first date (YYYY-MM-DD HH:MM:SS): ")
date2_str = input("Enter the second date (YYYY-MM-DD HH:MM:SS): ")

date1 = datetime.strptime(date1_str, "%Y-%m-%d %H:%M:%S")
date2 = datetime.strptime(date2_str, "%Y-%m-%d %H:%M:%S")

difference = date2 - date1

seconds = difference.total_seconds()

print("Difference in seconds:", seconds)
