import pyrealsense2 as rs
import numpy as np
import cv2
from config.loader import load_config
import logging
logger = logging.getLogger("vision")
from exceptions import exceptions
class RealSenseCamera:
    def __init__(self, config):
        self.camera_config = config
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.profile = None
        self.device = None
        self.align = None
        self.filters = {}
        self.intrinsics = {}
        self.camera_id = config["id"]
        self.serial = config["serial"]
    
    def get_intrinsics(self, stream_type):
        streams = self.profile.get_streams()
        for stream in streams:
            if stream.stream_type() == stream_type:
                video_stream = stream.as_video_stream_profile()
                #print(dir(video_stream))
                self.intrinsics[stream_type] = video_stream.get_intrinsics()
                return self.intrinsics[stream_type]
    
    def get_extrinsics(self, from_stream, to_stream):
        # depth stream = extrinsics (color profile)
        streams = self.profile.get_streams()
        for stream in streams:
            #print(stream.stream_type())
            if stream.stream_type() == from_stream:
                first_stream = stream.as_video_stream_profile()
            elif stream.stream_type() == to_stream:
                second_stream = stream.as_video_stream_profile()
                #print(help(depth_stream))
        extrinsics = first_stream.get_extrinsics_to(second_stream)
        return extrinsics

    def pixel_to_point(self, depth_frame, u, v):
        distance = depth_frame.get_distance(u,v)
        intrinsics = self.get_intrinsics(rs.stream.depth)
        point = rs.rs2_deproject_pixel_to_point(intrinsics, [u,v], distance)
        return point
    
    def start(self):
        try:
            self.profile = self.pipeline.start(self.config)
            self.profile = self.pipeline.start(self.config)
            self.device = self.profile.get_device()
            self.align = rs.align(rs.stream.color)
            self.filters["spatial"] = rs.spatial_filter()
            self.filters["temporal"] = rs.temporal_filter()
            self.filters["hole_filling"] = rs.hole_filling_filter()        
            print("---Camera Information---")
            print(f"Name: {self.device.get_info(rs.camera_info.name)}")
            print(f"Serial Number: {self.device.get_info(rs.camera_info.serial_number)}")
            print(f"Firmware Version: {self.device.get_info(rs.camera_info.firmware_version)}")
            print("\n---Sensor Information---")
            for sensor in self.device.sensors:
                print(f"Module: {sensor.get_info(rs.camera_info.name)}")
                #print(dir(sensor))
            logger.info("Camera Started")
        
        
        except RuntimeError as e:
            raise CameraStartError(f"Unable to start camera 
                                   {self.camera_id}") from e
        
        finally:
        
    
    def get_frame(self):
        # wait for frames and return frameset
        frames = self.pipeline.wait_for_frames()
        frames = self.align.process(frames)
        return frames
    
    def get_color_image(self, color_frame):
        color_buffer = color_frame.get_data()
        color_image = np.asanyarray(color_buffer)
        return color_image
    
    def get_depth_image(self, depth_frame):
        depth_buffer = depth_frame.get_data()
        depth_image = np.asanyarray(depth_buffer)
        return depth_image
    
    def process_depth(self, depth_frame):
        depth_frame = self.filters["spatial"].process(depth_frame)
        depth_frame = self.filters["temporal"].process(depth_frame)
        depth_frame = self.filters["hole_filling"].process(depth_frame)
        depth_frame = depth_frame.as_depth_frame()
        return depth_frame
    
    def stop(self):
        self.pipeline.stop()
        logger.info("Camera Stopped")
            
    def configure(self):
        color = self.camera_config["color"]

        self.config.enable_stream(
            rs.stream.color,
            color["width"],
            color["height"],
            FORMAT_MAP[color["format"]],
            color["fps"]
        )
        depth = self.camera_config["depth"]

        self.config.enable_stream(
            rs.stream.depth,
            depth["width"],
            depth["height"],
            FORMAT_MAP[depth["format"]],
            depth["fps"]
        )
        self.config.enable_device(self.camera_config["serial"])


FORMAT_MAP = {
            "bgr8": rs.format.bgr8,
            "z16": rs.format.z16,
        }

config = load_config("config/camera.yaml")
cameras = []

for cam_cfg in config["cameras"]:
    camera = RealSenseCamera(cam_cfg)
    camera.configure()
    camera.start()
    cameras.append(camera)

for camera in cameras:
    camera.stop()

# if __name__ == "__main__":
#     cameras = []
#     for cam_cfg in config["cameras"]:
#         camera = RealSenseCamera(cam_cfg)
#         camera.configure()
#         camera.start()
#         cameras.append(camera)

#     for camera in cameras:
#         frames = camera.get_frame()
#         color_frame = frames.get_color_frame()
#         depth_frame = frames.get_depth_frame()
#         depth_frame = camera.process_depth(depth_frame)

#         color_image = camera.get_color_image(color_frame)
#         depth_image = camera.get_depth_image(depth_frame)

#         point = camera.pixel_to_point(depth_frame, 100, 100)
#         filtered_depth = camera.process_depth(depth_frame)
#         timestamp = frames.get_timestamp()
#         frame_number = frames.get_frame_number()
#         depth_intrinsics = camera.get_intrinsics(rs.stream.depth)
#         color_intrinsics = camera.get_intrinsics(rs.stream.color)
#         e = camera.get_extrinsics(rs.stream.depth, rs.stream.color)
#         #camera.stop()