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


## 3D reconstruction and map creation 

## Build instructions 


## Navigation






