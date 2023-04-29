#include <pybind11/pybind11.h>
#include "slam/System.h"

namespace py = pybind11;

PYBIND11_MODULE(slam, m) {
	m.doc() = "Python bindings for ORB-SLAM3";
	py::class_<ORB_SLAM3::System> system(m, "system");

	system.def(py::init<const std::string&, const std::string&, const ORB_SLAM3::System::eSensor,const bool>());
	system.def("trackMonocular", &ORB_SLAM3::System::TrackMonocular);
	system.def("shutdown", &ORB_SLAM3::System::Shutdown);
	system.def("getMap", &ORB_SLAM3::System::GetMap);

	py::enum_<ORB_SLAM3::System::eSensor>(system,"eSensor")
		.value("MONOCULAR", ORB_SLAM3::System::eSensor::MONOCULAR)
		.value("STEREO", ORB_SLAM3::System::eSensor::STEREO)
		.value("RGBD", ORB_SLAM3::System::eSensor::RGBD)
		.value("IMU_MONOCULAR", ORB_SLAM3::System::eSensor::IMU_MONOCULAR)
		.value("IMU_STEREO", ORB_SLAM3::System::eSensor::IMU_STEREO)
		.export_values();

	py::class_<ORB_SLAM3::Atlas> atlas(m, "atlas");
	atlas.def("getAllMapPoints", &ORB_SLAM3::Atlas::GetAllMapPoints);
	atlas.def("getAllKeyFrames", &ORB_SLAM3::Atlas::GetAllKeyFrames);

	py::class_<ORB_SLAM3::MapPoint> mapPoint(m, "mapPoint");
	mapPoint.def("getWorldPos", &ORB_SLAM3::MapPoint::GetWorldPos);

	py::class_<ORB_SLAM3::KeyFrame> keyFrame(m, "keyFrame");
	keyFrame.def("getPose", &ORB_SLAM3::KeyFrame::GetPose);
	keyFrame.def("getRotation", &ORB_SLAM3::KeyFrame::GetRotation);
	keyFrame.def("getTranslation", &ORB_SLAM3::KeyFrame::GetTranslation);
	keyFrame.def("getCameraCenter", &ORB_SLAM3::KeyFrame::GetCameraCenter);
	keyFrame.def("getMapPoints", &ORB_SLAM3::KeyFrame::GetMapPoints);
	keyFrame.def("getMapPoint", &ORB_SLAM3::KeyFrame::GetMapPoint);
}