import datetime
import csv
import random

def collect_daily_times(date, names):
    print(f"Date: {date.strftime('%Y-%m-%d')}")
    daily_times = []
    for name in names:
        while True:
            time_input = input(f"Enter time for {name} (HH:MM): ")
            try:
                if time_input == "00:00":
                    # Set a large timedelta for sorting to the end
                    valid_time = datetime.timedelta(days=365)  # Arbitrary large timedelta
                else:
                    # Convert time to a timedelta since midnight
                    valid_time = datetime.datetime.strptime(time_input, '%H:%M') - datetime.datetime.strptime("00:00", '%H:%M')
                break
            except ValueError:
                print("Invalid time format. Please use HH:MM.")
        # Include a random tiebreaker for all times
        daily_times.append((name, valid_time, random.random()))

    # Sort times, smallest timedelta first, with random for tie-breaking
    ranked_times = sorted(daily_times, key=lambda x: (x[1], x[2]))
    return [(date.strftime('%Y-%m-%d'), name, rank + 1, (datetime.datetime.min + time).time().strftime('%H:%M') if time < datetime.timedelta(days=1) else "00:00") for rank, (name, time, _) in enumerate(ranked_times)]

def append_to_csv(data, filename):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def main():
    start_date = datetime.datetime.strptime("2024-04-08", '%Y-%m-%d')
    days = 26  # Change this to collect data for more or fewer days
    names = ["ahmad", "ameer", "ayham", "dana"]
    filename = 'ranking_data.csv'

    # Prepare the CSV file with headers if it doesn't exist
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Name', 'Rank', 'Time'])

    # Collect and write data day by day
    for day in range(days):
        current_date = start_date + datetime.timedelta(days=day)
        daily_data = collect_daily_times(current_date, names)
        append_to_csv(daily_data, filename)

if __name__ == "__main__":
    main()
