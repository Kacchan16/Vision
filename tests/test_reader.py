from realsense_shm.metadata import MetadataSerializer
from realsense_shm.metadata_writer import MetadataWriter
from realsense_shm.metadata_reader import MetadataReader

metadata_reader = MetadataReader("camera_metadata")
serializer = MetadataSerializer()
while True:
    metadata_bytes = metadata_reader.read()
    metadata = serializer.deserialize(metadata_bytes)
    #metadata_reader.shm.close()
    print(metadata)