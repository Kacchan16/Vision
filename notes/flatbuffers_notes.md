Why FlatBuffers?

We use FlatBuffers to serialize camera metadata into a compact binary format before placing it into shared memory.
Images (RGB and Depth) are not serialized because they are already stored efficiently in their own shared memory blocks.

Architecture:

RealSense Camera
      │
      ├── Color Image ──► cam_color (Shared Memory)
      ├── Depth Image ──► cam_depth (Shared Memory)
      └── Metadata
              │
              ▼
        FlatBuffers Serialize
              │
              ▼
     camera_metadata (Shared Memory)
     
FlatBuffer Schema
table FrameMetadata {
    frame_id:ulong;
    timestamp:double;
    width:uint;
    height:uint;
}

root_type FrameMetadata;

Generate Python classes:

flatc --python frame_metadata.fbs
Serializer

Purpose:

Convert Python values →FlatBuffer Binary
metadata_bytes = serializer.serialize(
    frame_id,
    timestamp,
    width,
    height
)

Output:

bytes
Metadata Writer

Purpose:

Store FlatBuffer bytes into shared memory.

Memory layout:

+----------------+----------------------+
| 4-byte length  | FlatBuffer payload   |
+----------------+----------------------+

Write:

metadata_writer.write_flatbuffer(metadata_bytes)
Metadata Reader

Purpose:

Read FlatBuffer bytes from shared memory.

metadata_bytes = metadata_reader.read_flatbuffer()

Output:

bytes
Deserializer

Purpose:

Convert

FlatBuffer bytes

↓

Python Dictionary
metadata = serializer.deserialize(metadata_bytes)

Result:

{
    "frame_id": ...,
    "timestamp": ...,
    "width": ...,
    "height": ...
}
Producer Flow
Camera

↓

Capture Frame

↓

Extract Metadata

↓

Serialize

↓

Write Metadata SHM

↓

Write Color SHM

↓

Write Depth SHM


Consumer Flow
Read Metadata SHM

↓

Deserialize

↓

Read Color SHM

↓

Read Depth SHM

↓

Use Images + Metadata


Shared Memory Lifecycle

Create once

Create
↓

Use forever

↓

close()

↓

unlink() (creator only)

Never unlink every frame.

FlatBuffers Advantages
Compact binary format
Very fast serialization
Low memory overhead
Cross-language support
Good for IPC (Inter-Process Communication)
