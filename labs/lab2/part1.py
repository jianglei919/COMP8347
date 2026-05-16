from datetime import datetime, timedelta, date


def main():
    # 1. Basic timedelta
    td = timedelta(days=180, hours=10, minutes=30)
    print(td)

    # 2. Today's date and current time
    now = datetime.now()
    print(f"Today is: {now}")

    # 3. Two years from now
    two_years = now.replace(year=now.year + 2)
    print(f"Two years from now it will be: {two_years}")

    # 4. timedelta with weeks and days
    delta = timedelta(weeks=3, days=4)
    future = now + delta
    print(f"In 3 weeks and 4 days it will be: {future}")

    # 5. Two weeks ago as a string
    two_weeks_ago = now - timedelta(weeks=2)
    print(f"Two weeks ago it was {two_weeks_ago.strftime('%a %b %-d, %Y')}.")

    # 6. Days till next Christmas
    today = date.today()
    christmas = date(today.year, 12, 25)
    if today > christmas:
        christmas = date(today.year + 1, 12, 25)
    days_left = (christmas - today).days
    print(f"{days_left} days left till next Christmas.")


if __name__ == "__main__":
    main()
