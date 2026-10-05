from realsense_camera.camera import RealSenseCamera
from realsense_shm.writer import SharedMemoryWriter
from multiprocessing.shared_memory import SharedMemory
from realsense_shm.metadata import MetadataSerializer
from realsense_shm.metadata_writer import MetadataWriter
from realsense_shm.metadata_reader import MetadataReader
import flatbuffers
import pyrealsense2 as rs
import numpy as np
from config.loader import load_config
import logging

logger = logging.getLogger("vision_processor")

if __name__ == "__main__":
    #shm = SharedMemoryWriter(name="my_shared_block", create=True, size=10)
    #camera configuration
    config = load_config("config/camera.yaml")
    camera_systems = []
    for cam in config["cameras"]:
        camera = RealSenseCamera(cam)
        camera.configure()
        camera.start()
        camera_id = cam["id"]

        color_cfg = cam["color"]
        depth_cfg = cam["depth"]

        color_shape = (
            color_cfg["height"],
            color_cfg["width"],
            3
        )
        depth_shape = (
            depth_cfg["height"],
            depth_cfg["width"])
        
        color_writer = SharedMemoryWriter(f"{camera_id}_color",
                                        color_shape,np.uint8)

        depth_writer = SharedMemoryWriter(f"{camera_id}_depth",
                                        depth_shape,np.uint16)

        metadata_writer = MetadataWriter(f"{camera_id}_metadata")
        #metadata_reader = MetadataReader(f"{camera_id}_metadata")
        serializer = MetadataSerializer()

        camera_systems.append({
            "camera": camera,
            "color_writer": color_writer,
            "depth_writer": depth_writer,
            "metadata_writer": metadata_writer,
            "serializer": serializer,
        })
    try:
        while True:
            for system in camera_systems:
                camera = system["camera"]
                color_writer = system["color_writer"]
                depth_writer = system["depth_writer"]
                metadata_writer = system["metadata_writer"]
                serializer = system["serializer"]
                        
                frames = camera.get_frame()
                
                color = frames.get_color_frame()
                depth = frames.get_depth_frame()

                        #depth processing
                depth_frame = camera.process_depth(depth)

                        #numpy conversion
                depth_image = camera.get_depth_image(depth_frame)
                color_image = camera.get_color_image(color)

                logger.debug(f"Color shape: {color_image.shape}")

                        #shared memory
                color_writer.write(color_image)
                depth_writer.write(depth_image)

                        #publish metadata
                        # 3. Serialize the fields into the buffer
                metadata = serializer.serialize(
                            frame_id=frames.get_frame_number(),
                            timestamp=frames.get_timestamp(),
                            width=color.get_width(),
                            height=color.get_height()
                        )

                metadata_writer.write(metadata)
    

    except KeyboardInterrupt:
        print("Stopping...")

    finally:
        for system in camera_systems:
            system["camera"].stop()
            system["color_writer"].close()
            system["depth_writer"].close()
            system["metadata_writer"].close()

            system["color_writer"].unlink()
            system["depth_writer"].unlink()
            system["metadata_writer"].unlink()
