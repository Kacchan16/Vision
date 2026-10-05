import flatbuffers
from generated.Vision.FrameMetadata import FrameMetadata
builder=flatbuffers.Builder(1024)

# 2. Assign your data values
input_frame_id = 42
input_timestamp = 1718112000  # Example Unix timestamp
input_width = 1920
input_height = 1080

# 3. Serialize the fields into the buffer
FrameMetadata.FrameMetadataStart(builder)
FrameMetadata.FrameMetadataAddFrameId(builder, input_frame_id)
FrameMetadata.FrameMetadataAddTimestamp(builder, input_timestamp)
FrameMetadata.FrameMetadataAddWidth(builder, input_width)
FrameMetadata.FrameMetadataAddHeight(builder, input_height)

# 4. Finish building the object
metadata_offset = FrameMetadata.FrameMetadataEnd(builder)
builder.Finish(metadata_offset)

# 5. Extract the final serialized byte array
serialized_buffer = builder.Output()

# Pass the serialized bytes into a new or existing buffer parsing sequence
buf = serialized_buffer

# Extract the root object
metadata = FrameMetadata.GetRootAsFrameMetadata(buf, 0)

# Read the fields back out
frame_id = metadata.FrameId()
timestamp = metadata.Timestamp()
width = metadata.Width()
height = metadata.Height()

# Output verification
print(frame_id, timestamp, width, height)
# Expected Output: 42 1718112000 1920 1080
