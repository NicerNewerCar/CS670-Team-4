#include "tello.hpp"
#include "global.h"
#include <iostream>
#include <algorithm>
#include <fstream>
#include <chrono>

#include <opencv2/core/core.hpp>

#include <System.h>
#include <Converter.h>


int drone(int argc, char** argv) {
	if (argc != 3) {
		std::cerr << endl << "Usage: ./drone path_to_vocabulary path_to_settings" << std::endl;
		return 1;
	}

	Tello tello;
	if (!tello.connect()) {
		std::cout << "Failed to connect to drone" << std::endl;
		return 1;
	}

	// access the tellos stream
	cv::VideoCapture cap{ "udp://0.0.0.0:11111", cv::CAP_FFMPEG };
	tello.enable_video_stream();

	/* 
	// Example flight code
	tello.takeoff();
    
    tello.move_right(20);
    tello.move_forward(20);
    tello.move_left(40);
    tello.move_back(40);
    tello.move_right(40);
    tello.move_forward(20);
    tello.move_left(20);
    
    tello.land();
	
	*/

	ORB_SLAM3::System SLAM(argv[1], argv[2], ORB_SLAM3::System::MONOCULAR, true); // init SLAN
	cv::Mat frame;
	double timestamp = 0.0;
	while (true) {
		cap >> frame;
		if (frame.empty())
			break; // end of video stream
		cv::imshow("Frame", frame);
		// get timestamp
		timestamp = (double)cv::getTickCount() / cv::getTickFrequency();
		SLAM.TrackMonocular(frame, timestamp);
		char c = (char)cv::waitKey(25);
		if (c == 27)
			break; // escape is pressed
	}

	SLAM.Shutdown();
	cap.release();
	/*
	// Example of how to get the map points
	std::vector<ORB_SLAM3::MapPoint*> allMapPoints = SLAM.GetMap()->GetAllMapPoints();
	std::cout << "# size=" << allMapPoints.size() << std::endl;
	std::cout << "# x,y,z" << std::endl;
	for (auto p : allMapPoints) {
		Eigen::Matrix<double, 3, 1> v = ORB_SLAM3::Converter::toVector3d(p->GetWorldPos());
		std::cout << v.x() << "," << v.y() << "," << v.z() << std::endl;
	}
	*/

	return 0;
}