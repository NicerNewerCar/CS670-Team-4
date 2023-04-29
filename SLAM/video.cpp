#include "global.h"
#include <iostream>
#include <algorithm>
#include <fstream>
#include <chrono>

#include <opencv2/core/core.hpp>

#include <System.h>
#include <Converter.h>

#include <string>
#include <experimental/filesystem>
#include <vector>

namespace fs = std::experimental::filesystem;


int video(int argc, char** argv) {

	if (argc != 5) {
		cerr << endl << "Usage: ./video path_to_vocabulary path_to_settings path_to_video output_directory" << endl;
		return 1;
	}

	ORB_SLAM3::System SLAM(argv[1], argv[2], ORB_SLAM3::System::MONOCULAR, true); // true = use viewer (false = no viewer)

	// Open the video file with opencv
	cv::VideoCapture cap(argv[3]);
	std::cout << "Video file: " << argv[3] << std::endl;
	if (!cap.isOpened()) {
		cerr << endl << "Could not open video file" << endl;
		return 1;
	}

	// Get the frame rate
	double fps = cap.get(cv::CAP_PROP_FPS);

	// Get the total number of frames in the video
	int totalFrameNumber = cap.get(cv::CAP_PROP_FRAME_COUNT);

	// Get the width and height of the frames in the video stream
	int frameWidth = cap.get(cv::CAP_PROP_FRAME_WIDTH);
	int frameHeight = cap.get(cv::CAP_PROP_FRAME_HEIGHT);

	std::string point_cloud_output = argv[4] + std::string("/point_clouds/");
	std::string key_frame_output = argv[4] + std::string("/key_frames/");

	// Create these directories if they don't exist 
	fs::create_directories(point_cloud_output);
	fs::create_directories(key_frame_output);

	cv::Mat img;
	double timestamp = 0.0;
	int frameNumber = 0;
	while (true) {
		cap >> img;
		if (img.empty())
			break; // end of video stream
		cv::imshow("Frame", img);
		// calculate the timestamp from the frame number and the frame rate
		timestamp = frameNumber / fps;
		SLAM.TrackMonocular(img, timestamp);
		char c = (char)cv::waitKey(25);
		if (c == 27)
			break; // escape is pressed
		


		// Save the keyframe
		// We only want to save the points that are in the keyframe

		// Get the keyframe
		ORB_SLAM3::KeyFrame* keyframe = SLAM.GetTracker()->mCurrentFrame.mpReferenceKF;
		if (keyframe != NULL) {
			std::cout << "Keyframe found!" << std::endl;

			// Get the map points
			std::vector<ORB_SLAM3::MapPoint*> map_points = keyframe->GetMapPointMatches();

			// Save the keyframe
			std::string key_frame_name = key_frame_output + std::to_string(frameNumber) + std::string(".png");
			cv::imwrite(key_frame_name, img);

			// Export the map points
			std::string point_cloud_name = point_cloud_output + std::to_string(frameNumber) + std::string(".txt");
			std::ofstream point_cloud_file(point_cloud_name);
			for (ORB_SLAM3::MapPoint* map_point : map_points) {
				if (map_point != NULL) {
					cv::Mat point = map_point->GetWorldPos();
					point_cloud_file << point.at<float>(0) << " " << point.at<float>(1) << " " << point.at<float>(2) << std::endl;
				}
			}
			point_cloud_file.close();
		}
		frameNumber++;
	}

	// Stop all threads
	SLAM.Shutdown();
	cap.release();

	return 0;

}