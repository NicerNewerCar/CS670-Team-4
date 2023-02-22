# Compiling the Docker Image

Make sure you have docker desktop installed, if not either download from dockers website or open a Windows Terminal and run `winget install Docker.DockerDesktop`.
The docker image can be built with the following command:
* `cd path/to/repo/CS670-Team-4/docker`
* `docker build -t "drone:latest" -f .\DOCKERFILE .`. 
    * This is a rather large image so it make take some time to build.
* NOTE: If we want to switch between ORB-SLAM and CCM-SLAM pipelines we need to uncomment lines `108-109` and comment lines `80-81` in the docker file.

# Launching the Docker Image with GUI pass through

See this [guide](https://dev.to/darksmile92/run-gui-app-in-linux-docker-container-on-windows-host-4kde) for more information (I would suggest running the firefox example here just to make sure everything is working).

* Install [VcXsrv](https://sourceforge.net/projects/vcxsrv/), either from the download link provided or with chocolaty. `choco install vcxsrv`.
* Find your IP with `ipconfig`
* Use `docker run -it --net=host -e DISPLAY=<your ip>:0.0 --name droneContainer drone:latest`
* Use docker desktop to attach a console to begin running code