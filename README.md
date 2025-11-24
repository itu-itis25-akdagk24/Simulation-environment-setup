# Gazebo an Ardupilotplugin Setup
Gazebo and ArduPilot setup, including some model and world configurations.

Ubuntu 22.04\
Gazebo Sim Harmonic, version 8.10.0\
ArduPilot-4.6.0

NOTE: The ArduPilot plugin does not depend on ROS. Therefore, in this setup, we will skip ROS installation for now. In the future, it may be necessary.\
NOTE: At the end of this documentation, there is a Common Issues section. If you have any problems, please check that section first.\
NOTE: If you do not install "git" before, please ensure that you install it.
```bash
sudo apt-get update
sudo apt install git
```


All the documents using this setup are listed below:

https://gazebosim.org/docs/harmonic/install_ubuntu/ gazebo harmonic installation\
https://ardupilot.org/dev/docs/sitl-with-gazebo.html ardupilot+gazebo plugin\
https://discuss.ardupilot.org/uploads/default/original/2X/d/d7083377f747deab79798e7a9cef58d433ff5f66.pdf multiple drones
https://ardupilot.org/dev/docs/building-setup-linux.html ardupilot installation

## Gazebo Harmonic Installation
First install some necessary tools:
```bash
sudo apt-get update
sudo apt-get install curl lsb-release gnupg
```

Then install Gazebo Harmonic:
```bash
sudo curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] https://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
sudo apt-get update
sudo apt-get install gz-harmonic
```
## Installing Ardupilot SITL
Firstly, clone the ardupilot source code.
```bash
git clone https://github.com/ArduPilot/ardupilot.git
cd ardupilot
git submodule update --init --recursive
```
Install the SITL dependencies.
```bash
Tools/environment_install/install-prereqs-ubuntu.sh -y
```
Build SITL
```bash
cd ardupilot
./waf configure --board sitl
./waf copter
```
Do not forget sim_vehicle.py PATH Setup

İf you skip this step, probably you will have "sim_vehicle.py can not be found" error.
```bash
echo 'export PATH=$PATH:$HOME/ardupilot/Tools/autotest' >> ~/.bashrc
source ~/.bashrc
```

## Using Ardupilot SITL with Gazebo¶

Firstly, check your Gazebo. This command should open a world with various shapes.
```bash
gz sim -v4 -r shapes.sdf
```
While Gazebo is commonly used with ROS / ROS2, the ArduPilot Gazebo plugin does not depend on ROS.
### Install the ArduPilot Gazebo Plugin¶
1.) Install additional dependencies
```bash
sudo apt update
sudo apt install libgz-sim8-dev rapidjson-dev
sudo apt install libopencv-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev gstreamer1.0-plugins-bad gstreamer1.0-libav gstreamer1.0-gl
```
2.)Create a workspace folder and clone the repository
```bash
cd
mkdir -p gz_ws/src && cd gz_ws/src
git clone https://github.com/ArduPilot/ardupilot_gazebo
```
3.)Build the plugin
Set GZ_VERSION environment variable according to installed gazebo version 
```bash
export GZ_VERSION=harmonic
cd ardupilot_gazebo
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo
make -j4
```
### Configure the Gazebo environment¶
Do not forget to run these two commands:(If you skip this step, you can not start the gazebo)
```bash
echo 'export GZ_SIM_SYSTEM_PLUGIN_PATH=$HOME/gz_ws/src/ardupilot_gazebo/build:${GZ_SIM_SYSTEM_PLUGIN_PATH}' >> ~/.bashrc
echo 'export GZ_SIM_RESOURCE_PATH=$HOME/gz_ws/src/ardupilot_gazebo/models:$HOME/gz_ws/src/ardupilot_gazebo/worlds:${GZ_SIM_RESOURCE_PATH}' >> ~/.bashrc
source ~/.bashrc
```
However, if you have already done this and you still have problems, try exporting the variables manually in the terminal where you will launch Gazebo:
```bash
export GZ_SIM_SYSTEM_PLUGIN_PATH=$HOME/gz_ws/src/ardupilot_gazebo/build:${GZ_SIM_SYSTEM_PLUGIN_PATH}
export GZ_SIM_RESOURCE_PATH=$HOME/gz_ws/src/ardupilot_gazebo/models:$HOME/gz_ws/src/ardupilot_gazebo/worlds:${GZ_SIM_RESOURCE_PATH}
export LD_LIBRARY_PATH=$HOME/gz_ws/src/ardupilot_gazebo/build:$LD_LIBRARY_PATH
```
### Installing MAVProxy
These commands install MAVProxy and all required Python dependencies.
```bash
sudo apt-get install python3-dev python3-opencv python3-wxgtk4.0 python3-pip python3-matplotlib python3-lxml python3-pygame
python3 -m pip install PyYAML mavproxy --user
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.bashrc
source ~/.bashrc

```

### Using Gazebo with ArduPilot¶
In the first terminal, start a Gazebo example world:
```bash
gz sim -v4 -r iris_runway.sdf
```
In the second terminal, run SITL:
```bash
sim_vehicle.py -v ArduCopter -f gazebo-iris --model JSON --map --console
```
In the SITL terminal, you can test your connection (please try these commands one by one):
```bash
GUIDED
GUIDED
GUIDED
arm throttle
takeoff 10
```

If, at the end of the SITL terminal, you can see “heartbeat received” and do not see any “JSON message not received” errors, you can use the ArduPilot plugin and Gazebo properly. After this step, we can edit our worlds and models and start using them.

## Multiple Drone Simülation Environment
First, please clone this GitHub repository to your computer.\
(If you have any issues cloning, just download it as a ZIP file — no problem.)
```bash
cd
git clone https://github.com/itu-itis25-akdagk24/Simulation-environment-setup.git
# If you're asked for a password and don’t have one, please generate a personal access token from GitHub.
```
Make sure all the files are available:

```bash
cd Simulation-environment-setup/
ls
""" you should see something like that:
exp_drone_control.py       iris_runway_tripledrone.sdf   iris_with_gimbal_2
initialize.py              iris_runway_singledrone.sdf  iris_with_gimbal_3
iris_runway_dualdrone.sdf  iris_with_gimbal_1           README.md
"""
```
Now, you need to move the world and model files to the appropriate locations inside your gz_ws workspace that we’ve already worked on.\
You can do this manually, or use the following command.~/gz_ws/src/ardupilot_gazebo/models. If you want you can use following commands also:

World files must be placed in:\
~/gz_ws/src/ardupilot_gazebo/worlds

Model folders must be placed in:\
~/gz_ws/src/ardupilot_gazebo/models

If you prefer using the terminal, you can use:

```bash 
cd ~/Simulation-environment-setup

mv iris_runway_singledrone.sdf iris_runway_dualdrone.sdf iris_runway_tripledrone.sdf ~/gz_ws/src/ardupilot_gazebo/worlds

mv iris_with_gimbal_1 iris_with_gimbal_2 iris_with_gimbal_3 ~/gz_ws/src/ardupilot_gazebo/models
```
At the end, please make sure that:

The following files are in ~/gz_ws/src/ardupilot_gazebo/worlds
```bash
iris_runway_dualdrone.sdf    
iris_runway_tripledrone.sdf   
iris_runway_singledrone.sdf  
```
And the following folders are in ~/gz_ws/src/ardupilot_gazebo/models
```bash
iris_with_gimbal_1
iris_with_gimbal_2
iris_with_gimbal_3
```
These steps are very important — please don’t skip them.

After completing the world and model file setup, you can start your simulation environment.\
(Note: This simulation currently supports a maximum of 3 drones.)
```bash
cd Simulation-environment-setup
python initialize.py <drone_number>
```
After running this command, you should see:

The Gazebo GUI with multiple drones\
One ArduPilot SITL terminal, one MAVProxy console, and one MAVProxy map for each drone\
An example drone control terminal UI for testing your connections with some basic features (like arm, takeoff, swarm move)

If you complete this setup and can control your drones in Gazebo, you are ready to make the drones dance.

## Some common issues and their solutions:

Python:commond not found.
```bash
sudo apt install python-is-python3
```

sim_vehicle.py command not found.
```bash
export PATH=$PATH:$HOME/ardupilot/Tools/autotest
```
If you have still issue please, ensure that you have complete SITL steps correctly./

Please consider the error information. For example, if it says something like:/
xxxx module not found/
then try:/
sudo apt install xxxx/
Just install it.



















