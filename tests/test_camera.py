from realsense_camera.camera import RealSenseCamera

camera = RealSenseCamera()
camera.start()
camera.stop()
print(camera.pipeline)
print(camera.config)