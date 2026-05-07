from datetime import datetime, date, time, timedelta

# A basic timedelta
delta = timedelta(days=365, hours=5, minutes=1)
print(delta)  # e.g., 365 days, 5:01:00

# Now (date+time together)
now = datetime.now()
print("Today is:", now)

# Two years from now
two_years = now.replace(year=now.year + 2)
print("Two years from now it will be:", two_years)

# In 2 weeks and 3 days from now
future = now + timedelta(weeks=2, days=3)
print("In 2 weeks and 3 days it will be:", future)

# Three weeks ago as a friendly string
three_weeks_ago = now - timedelta(weeks=3)
print("Three weeks ago it was", three_weeks_ago.strftime("%A %B %d, %Y"))

# Days until next Christmas (Dec 25)
today = date.today()
this_year_xmas = date(today.year, 12, 25)
if today > this_year_xmas:
    this_year_xmas = date(today.year + 1, 12, 25)

days_left = (this_year_xmas - today).days
print(f"{days_left} days left till next Christmas")
