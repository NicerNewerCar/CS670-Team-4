#include "global.h"
#include <iostream>
#include <algorithm>
#include <fstream>
#include <chrono>

#include <opencv2/core/core.hpp>

#include <System.h>
#include <Converter.h>

int webcam(int argc, char** argv) {

	if (argc != 4) {
		cerr << endl << "Usage: ./webcam path_to_vocabulary path_to_settings path_to_sequence_folder" << endl;
		return 1;
	}

	ORB_SLAM3::System SLAM(argv[1], argv[2], ORB_SLAM3::System::MONOCULAR, true); // true = use viewer (false = no viewer)

	// while webcam is active get frames and pass them to SLAM
	// SLAM.TrackMonocular(frame, timestamp); where frame is cv::Mat and timestamp is double

	// create a video capture object to acquire webcam feed
	cv::VideoCapture cap(0);

	// if not success, exit program
	if (cap.isOpened() == false) {
		cout << "Cannot open the web cam" << endl;
		cin.get(); //wait for any key press
		return -1;
	}
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
	std::vector<ORB_SLAM3::MapPoint*> allMapPoints = SLAM.GetMap()->GetAllMapPoints();
	std::cout << "# size=" << allMapPoints.size() << std::endl;
	std::cout << "# x,y,z" << std::endl;
	for (auto p : allMapPoints) {
		Eigen::Matrix<double, 3, 1> v = ORB_SLAM3::Converter::toVector3d(p->GetWorldPos());
		std::cout << v.x() << "," << v.y() << "," << v.z() << std::endl;
	}
	return 0;
}