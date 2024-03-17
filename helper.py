import csv
import datetime

# Define the path to the CSV file
csv_file_path = 'data/leaderboardstats.csv'

# Function to convert seconds to MM:SS format
def seconds_to_mm_ss(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{int(minutes):02d}:{int(seconds):02d}"

# Function to write data to CSV
def write_data_to_csv(data):
    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

# Function to get time input for each name in seconds, calculate ranks, and ignore 0 times for ranking
def get_times_and_rank(date):
    names = ['ahmad', 'ameer', 'ayham']
    times = {}
    
    for name in names:
        # Prompt user for time in seconds
        time = float(input(f"Time for {name} on {date.strftime('%m/%d/%Y')} in seconds: "))
        times[name] = time
    
    # Filter times greater than 0 and sort
    positive_times = {name: time for name, time in times.items() if time > 0}
    ranked_names = sorted(positive_times.items(), key=lambda x: x[1])
    
    # Prepare data for CSV with time in MM:SS format, append names with 0 time at the end
    csv_data = []
    rank = 1
    for name, time in ranked_names:
        time_mm_ss = seconds_to_mm_ss(time)
        csv_data.append([date.strftime('%m/%d/%Y'), name, rank, time_mm_ss])
        rank += 1
    
    # Append names with 0 time without rank
    for name, time in times.items():
        if time == 0:
            time_mm_ss = seconds_to_mm_ss(time)
            csv_data.append([date.strftime('%m/%d/%Y'), name, "-1", time_mm_ss])
    
    return csv_data

def main():
    # Initialize start and end dates
    start_date = datetime.date(2024, 1, 1)
    end_date = datetime.date(2024, 3, 17)
    
    # Check if CSV exists, if not, write header
    try:
        with open(csv_file_path, 'x') as file:
            writer = csv.writer(file)
            writer.writerow(['date', 'name', 'rank', 'time'])
    except FileExistsError:
        pass  # File already exists, do nothing

    current_date = start_date
    while current_date <= end_date:
        # Get times and ranks for the current day
        day_data = get_times_and_rank(current_date)
        
        # Write data to CSV
        write_data_to_csv(day_data)
        
        # Move to the next day
        current_date += datetime.timedelta(days=1)

if __name__ == "__main__":
    main()
