# CS 670 - Team #4      Cancel changes


This repo contains the code for our final project.

## Cloning the Repository

`git clone --recursive https://github.com/NicerNewerCar/CS670-Team-4.git`

## SLAM

### Build instructions

Note: This MUST be built on **windows** and in the **Release** configuration, the Debug config WILL NOT WORK.
If you are using Linux checkout the ORB_SLAM3 repo on [GitHub](https://github.com/UZ-SLAMLab/ORB_SLAM3).

* Open the `slam.sln` file in Visual Studio.
* Right click on the `slam`, in the solution explorer, and click build.
    * This build may take 15-20 minutes.

### Usage

In order to run the SLAM on a video you need the cameras intrinsic parameters and distortion coefficients. Fill in these values in a copy of the `example.yaml` file.

* Run the `slam` executable with the path to the video and the path to the yaml file as arguments.
```bash
cd SLAM
.\x64\Release\slam.exe video ./Vocabulary/ORBvoc.txt example.yaml /path/to/video.mp4 /path/to/output/dir
```

## SIDE
### Build instructions
Note: 
* Code was ran on **windows** using Python 3.6
* All of the process should be followed the above link.
* To customize the h5 files from the NYU dataset as input of the SIDE, please modify the create_point_clouds.py.
* Our training process is done with the Intel Core i7-8700, 32 GHz, 32 GB RAM, and NVIDIA GTX 1080 GPU.


## 3D reconstruction and map creation 

### Build instructions 
Note: code was ran on **windows** using **python 3.10.9**

* create an anacoda enviroment from the provided yaml file 

### Usage
Note: directories for io are defined at compile time. Each of the scripts are ran one after another, with 
the exception of outlier_removal.py and make_csv.py. outlier_removal.py is only needed sometimes and make_csv.py is
only required becuase the A* algorithm we use takes maps as csv's

* create_point_clouds.py
* outlier_removal.py
* merge_point_clouds1.py
* point_cloud_to_layer2.py
* 2d_map_from_layer_2.py
* make_csv.py

## Navigation

An implementation of A* returning the shortest path between two points on a 2D array.

### Usage
Specify a map, start position and goal position in the map.py. The map should be a .csv file. After that, run main.py at the terminal. The output, a git file, will be created in the same directory.

An example of path planning output.
![PathPlanning](https://user-images.githubusercontent.com/103143536/236883382-bc11d810-d812-434b-a5a2-b4b165f644c7.gif)






