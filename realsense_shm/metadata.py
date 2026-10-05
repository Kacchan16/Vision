#from generated.Vision import FrameMetadata
from generated.Vision import FrameMetadata
import flatbuffers

class MetadataSerializer:

    def serialize(self, frame_id, timestamp, width, height):
        builder = flatbuffers.Builder(1024)
        FrameMetadata.FrameMetadataStart(builder)
        FrameMetadata.FrameMetadataAddFrameId(builder, frame_id)
        FrameMetadata.FrameMetadataAddTimestamp(builder, timestamp)
        FrameMetadata.FrameMetadataAddWidth(builder, width)
        FrameMetadata.FrameMetadataAddHeight(builder, height)

        metadata_bytes = FrameMetadata.FrameMetadataEnd(builder)
        builder.Finish(metadata_bytes)
        return builder.Output()

    def deserialize(self, ser_buf):
        metadata = FrameMetadata.FrameMetadata.GetRootAsFrameMetadata(ser_buf, 0)
        return {
    "frame_id": metadata.FrameId(),
    "timestamp": metadata.Timestamp(),
    "width": metadata.Width(),
    "height": metadata.Height(),
}
        