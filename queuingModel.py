import numpy as np
import pandas as pd
from queue import Queue
import matplotlib.pyplot as plt
from matplotlib import style

class ChargingStation:

    def __init__(self,num_stalls : int):
        self.num_stalls = num_stalls

    def simulate_charging_station(self,arrival_list : list or np.array, charging_durations : list or np.array):
        # Initialize variables
        n_vehicles = len(arrival_list)
        current_time = 0
        queue = Queue()
        stalls = [0] * self.num_stalls  # Stores end times for each stall

        # Create result dictionary
        result = {
            'id': list(range(n_vehicles)),
            'arrival_time': arrival_list,
            'charging_duration': charging_durations,
            'start_time': [0] * n_vehicles,
            'end_time': [0] * n_vehicles,
            'stall_id': [-1] * n_vehicles
        }

        # Sort vehicles by arrival time
        sorted_indices = sorted(range(n_vehicles), key=lambda k: arrival_list[k])

        # Process each vehicle
        current_vehicle_idx = 0

        while current_vehicle_idx < n_vehicles or not queue.empty():
            # Add newly arrived vehicles to queue
            while (current_vehicle_idx < n_vehicles and
                   arrival_list[sorted_indices[current_vehicle_idx]] <= current_time):
                queue.put(sorted_indices[current_vehicle_idx])
                current_vehicle_idx += 1

            # Check for available stalls
            for stall_id in range(self.num_stalls):
                if stalls[stall_id] <= current_time and not queue.empty():
                    # Get next vehicle from queue
                    vehicle_id = queue.get()

                    # Set start time and stall
                    result['start_time'][vehicle_id] = current_time
                    result['end_time'][vehicle_id] = current_time + charging_durations[vehicle_id]
                    result['stall_id'][vehicle_id] = stall_id

                    # Update stall end time
                    stalls[stall_id] = result['end_time'][vehicle_id]

            # Move time to next event
            next_times = []
            if current_vehicle_idx < n_vehicles:
                next_times.append(arrival_list[sorted_indices[current_vehicle_idx]])
            for stall_time in stalls:
                if stall_time > current_time:
                    next_times.append(stall_time)

            if next_times:
                current_time = min(next_times)
            elif not queue.empty():
                current_time = min(t for t in stalls if t > current_time)

        # Create and return DataFrame
        return pd.DataFrame(result)


    def plot_result(self,res: pd.DataFrame):
        # convert the dataframe into stall_usage : list
        stall_usage = [[] for _ in range(self.num_stalls)]
        for i in range(self.num_stalls):
            usage = res[res['stall_id'] == i]
            for _, row in usage.iterrows():
                stall_usage[i].append((row['start_time'], row['end_time']))

        num_cars = len(res)

        style.use('seaborn-v0_8-deep')

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 1]})

        # Visualize the usage period
        colors = plt.cm.tab20c.colors
        for i, periods in enumerate(stall_usage):
            for j, (start, end) in enumerate(periods):
                ax1.broken_barh([(start, end - start)], (i - 0.4, 0.8), facecolors=colors[j % len(colors)])

        ax1.set_yticks(range(self.num_stalls))
        ax1.set_yticklabels([f'Stall{i + 1}' for i in range(self.num_stalls)])
        ax1.set_xlabel('Time(Minutes)')
        ax1.set_ylabel('Charging Stalls')
        ax1.set_title('Charging Stalls Occupancy Over Time')
        ax1.grid(True)

        # do this to set labels
        ax2.hlines(y=1, xmin=res.loc[0, 'arrival_time'], xmax=res.loc[0, 'start_time'], color='red', label='Queuing')
        ax2.hlines(y=1, xmin=res.loc[0, 'start_time'], xmax=res.loc[0, 'end_time'], color='green', label='Charging')

        for i in range(1, num_cars):
            ax2.hlines(y=i + 1, xmin=res.loc[i, 'arrival_time'], xmax=res.loc[i, 'start_time'],
                       color='red')  # Queuing Lines
            ax2.hlines(y=i + 1, xmin=res.loc[i, 'start_time'], xmax=res.loc[i, 'end_time'], color='green')  # Charging Lines

        # ax2.set_yticks(range(0,30))
        ax2.set_ylabel('Vehicle ID')
        ax2.set_xlabel('Time(Minutes)')
        ax2.set_title('Serving or Queuing Distribution for Vehicles')
        ax2.grid(True)
        ax2.legend(loc='lower right')

        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    NUM_CARS = 30
    SOC_RANGE = (20, 80)
    SIM_TIME = (0, 180)
    np.random.seed(13)
    arrival_list = sorted([np.random.randint(*SIM_TIME) for _ in range(NUM_CARS)])
    charging_duration = [np.random.randint(*SOC_RANGE) for _ in range(NUM_CARS)]

    CS1 = ChargingStation(num_stalls=5)
    res = CS1.simulate_charging_station(arrival_list,charging_duration)
    CS1.plot_result(res)

