import subprocess
import time
import sys

def initialize_gazebo_environment(drone_number):
    if drone_number == 1:
        subprocess.Popen(['gnome-terminal', '--', 'bash', '-c',
                        'gz sim -v4 -r iris_runway_singledrone.sdf; exec bash'])
        print(f"Gazebo environment launched with {drone_number} drones")
    if drone_number == 2:
        subprocess.Popen(['gnome-terminal', '--', 'bash', '-c',
                        'gz sim -v4 -r iris_runway_dualdrone.sdf; exec bash'])
        print(f"Gazebo environment launched with {drone_number} drones")
    if drone_number == 3:
        subprocess.Popen(['gnome-terminal', '--', 'bash', '-c',
                        'gz sim -v4 -r iris_runway_tripledrone.sdf; exec bash'])
        print(f"Gazebo environment launched with {drone_number} drones")

def ardupilot_vehicle(drone_number):
    for i in range(0, drone_number):
        subprocess.Popen(['gnome-terminal', '--', 'bash', '-c',
                          f'sim_vehicle.py -v ArduCopter -f gazebo-iris --model JSON --map --console -I{i}; exec bash'])
        print(f"Drone {i} launched")
        time.sleep(2)

def drone_control():
        subprocess.Popen(['gnome-terminal', '--', 'bash', '-c',
                          'python exp_drone_control.py; exec bash'])
        print(f"Drone control.")  


if __name__== "__main__":
    if len(sys.argv) < 2:
        print("Usage: python initialize.py <drone_number>")
        sys.exit(1)
    drone_number = int(sys.argv[1])
    if drone_number<=0 or drone_number>3:
        print("wrong enter: maksimum drone number is 3")
    initialize_gazebo_environment(drone_number)
    ardupilot_vehicle(drone_number)
    drone_control()



