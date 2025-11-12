from pymavlink import mavutil
import time
import sys

class Drone():
	def __init__(self,master, id):
		self.drone= mavutil.mavlink_connection(master)
		self.id = id
		
	def wait_heartbeat(self):
		self.drone.wait_heartbeat()
		
	def arm(self):
		self.drone.set_mode_apm('GUIDED')
		time.sleep(1)
		self.drone.arducopter_arm()



	def takeoff(self,alt):
		self.drone.mav.command_long_send(
		    self.drone.target_system,
		    self.drone.target_component,
		    mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
		    0,  # confirmation
		    0, 0, 0, 0,  # param1-4 (boş)
		    0, 0, alt  # lat, lon, alt (lat/lon = 0 => mevcut konum)
		)

	def land(self):
		self.drone.mav.command_long_send(
		    self.drone.target_system,
		    self.drone.target_component,
		    mavutil.mavlink.MAV_CMD_NAV_LAND,
		    0,
		    0, 0, 0, 0,  # param1-4
		    0, 0, 0      # lat, lon, alt (0 = bulunduğu yere in)
		)

	def move(self,x,y,z):
		self.drone.mav.set_position_target_local_ned_send(
		    0,
		    self.drone.target_system,
		    self.drone.target_component,
		    mavutil.mavlink.MAV_FRAME_LOCAL_OFFSET_NED,
		    0b110111111000,
		    x,y,-z,
		    0,0,0,
		    0, 0, 0, 
		    0, 0      
		)
		
drones = []
drone_number = int(sys.argv[1])
for i in range(0,drone_number):
	drones.append(Drone(f"udp:127.0.0.1:{14550 + i*10}",i))
	print(f"Drone {i} connected")


for drone in drones:	
	drone.wait_heartbeat()
	print(f"heartbeat from {drone.id} received")
	
while True:
	try:
		command = int(input(
			"""Enter command:
		ARM: 1
		TAKEOFF: 2
		SWARM MOVE: 3
		V FORMATION: 4
		SWARM LAND: 5
		INDIVIDUAL CONTROL: 0
		"""
		))
	except ValueError:
		print("Invalid input. Please enter a number corresponding to a command.")
		continue
	if command==1:
		for drone in drones:
			drone.arm()
			print(f"drone armed {drone.id}")

		
	if command==2:
		alt = int(input("enter alt: "))
		for drone in drones:
			drone.takeoff(alt)
			print(f"drone takeoff {drone.id}")

	if command==4:
		x, y, z = 5, 0, 0
		for drone in drones:
			drone.move(x,y,z)
			x+=5
			print(f"drone moved {drone.id}")
				
	if command == 3:
		d = input("displacement: x,y,z: ")  
		try:
			x, y, z = [float(i) for i in d.split(",")]
		except ValueError:
			print("wrong enter: x,y,z")
		else:
			for drone in drones:
				drone.move(x, y, z)
				print(f"Drone {drone.id} moved by {x}, {y}, {z}")

	if command==5:
		for drone in drones:
			drone.land()
			print(f"drone landed {drone.id}")

	if command==0:
		id = int(input(f"select drone: {[i for i in range(drone_number)]} "))
		while True:
			for drone in drones:
				if drone.id == id:
					command = int(input(
											"""Enter command:
					ARM:1
					TAKEOFF:2
					MOVE:3
					LAND:4
					CHANGE DRONE:5
					SWARM CONTROL:0
					"""
										))
					if command==1:
						drone.arm()
						print(f"drone armed {drone.id}")
					if command==2:
						alt = int(input("enter alt: "))
						drone.takeoff(7)
						print(f"drone takeoff {drone.id}")
					if command==3:
						d = input("displacement: x,y,z: ")  
						try:
							x, y, z = [float(i) for i in d.split(",")]
						except ValueError:
							print("wrong enter: x,y,z")
						else:
							drone.move(x, y, z)
							print(f"Drone {drone.id} moved by {x}, {y}, {z}")
					if command==4:
						drone.land()
						print(f"drone landed {drone.id}")		
					if command==5:
						id = int(input(f"select drone: {[i for i in range(drone_number)]} "))
					if command==0:
						break

