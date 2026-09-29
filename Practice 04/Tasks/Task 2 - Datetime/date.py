from datetime import datetime, timedelta

# 1
today = datetime.now()
print("5 days ago:", today - timedelta(days=5))

# 2
print("Yesterday:", today - timedelta(days=1))
print("Today:", today)
print("Tomorrow:", today + timedelta(days=1))

# 3
print("Without microseconds:", today.replace(microsecond=0))

# 4
date1 = datetime(2026, 9, 29, 12, 0, 0)
date2 = datetime(2026, 9, 29, 15, 30, 0)

difference = date2 - date1
print("Difference in seconds:", difference.total_seconds())