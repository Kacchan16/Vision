Create Context
      ↓
Find Devices
      ↓
Create Pipeline
      ↓
Configure Streams
      ↓
Start Camera
      ↓
Get Frames
      ↓
Process Frames
      ↓
Stop Camera

learn one class at a time like rs.context, what methods it have, what each method return.

pyrealsense2, will connect to realsense camera, configure, capture frames, read depth information, access rgb images, align depth and color, use imu data, control camera settings-exposure, gain, etc, perform post-processing filters.
python code -- pyrealsense2 --librealsense sdk -- realsense camera

classes -- pipeline, config, pipeline_profile, device, sensor, frameset, frame, depth_frame, video_frame, align, pointcloud, colorizer, spatial_filter, temporal_filter.

main are pipeline, config, start(), wait_for_frames(), frameset, color_frame, depth_frame, stop()

pipeline, it manages camera streaming, methods are .start(), stop, wait_for_frames, poll_for_frames, get_active_profile.

dir() -- tells the methods inside the class. open toolbox
help() -- shows the doc of the method.
type(depth), dir(depth)

ARCHITECTURE:-

Camera
   │
   ▼
pipeline
   │
   ▼
config
   │
   ▼
start()
   │
   ▼
Frames continuously arrive
   │
   ▼
wait_for_frames()
   │
   ▼
frameset
   ├── depth_frame
   └── color_frame

Class: pipeline, manager of camera session. 

Purpose:
Starts and manages camera streaming. open cam, start & stop stream, sync frame, deliver.

without pipeline, need to configure each sensor manually and keep their time sync.

Methods:
- start() - finds cam, validate req streams, configure streams, and start stream.
- stop()
- wait_for_frames() - cam is running, next sync set of frames, frameset. block until the next sync frameset is ready
- poll_for_frames() - check if new frameset is available and retrieve latest undelivered set without blocking.
- get_active_profile() - returns info about current stream config

Returns:
frameset, container has same moment data. then extra both data again.

Class: Config
Purpose: cam produce diff kinds of data, rgb, depth, infra, imu data. which streams u want, with details like resol, and frame rate.

what is pipeline, why it exist, wt problem it solve?

class: Config

purpose: simply set of instructions, how you want the camera to stream.

enable_stream - req a stream
disable_stream  - remove prev req stream
disable_all_streams - clear all req stream
enable_device - req spec cam by serial
resolve
enable_record_to_file - rec sesson to bag file
enable_device_from_file - replay data from prev rec bag file instead of live cam.

Create config
      │
      ▼
Add stream requests
      │
      ▼
Pass to pipeline.start()
      │
      ▼
Pipeline reads the configuration

lesson 4

workflow is 

Create Pipeline
        ↓
Create Config
        ↓
Configure Streams
        ↓
Start Pipeline
        ↓
Receive Frames
        ↓
Stop Pipeline

after start

Find Camera
      ↓
Validate Configuration
      ↓
Open Sensors
      ↓
Allocate Buffers
      ↓
Start Streaming

every step returns another object

pipeline()
      │
      ▼
pipeline object

config()
      │
      ▼
config object

start()
      │
      ▼
pipeline_profile

wait_for_frames()
      │
      ▼
frameset

get_depth_frame()
      │
      ▼
depth_frame

get_color_frame()
      │
      ▼
video_frame

wait-for-frames, returns rep of realsense raw data not numpy arrays. frame contains more than pixel data, like timestamp, frame number, sensor info, depth scale, metadata.

Pipeline_profile

purpose: it is receipt, of what req, al config

Pipeline Profile
│
├── Connected Device
├── Active Streams
├── Stream Formats
├── Resolution
├── FPS
└── Sensors

get_device() - returns a device object
get_streams() - returns info about active streams.

rs
│
├── pipeline()
│       │
│       ├── start(config)
│       │
│       ▼
│   pipeline_profile
│       │
│       ├── get_device()
│       └── get_streams()
│
└── config()

device, phys realsense camera
cam name, serial, firware, usb type, id, available sensors. prop of hardware.

query_sensors - cam have multiple sensors. get sensors inside device.
first_depth_sensor - get depth sensor directly
get_info - read hardware info 
hardware_reset - restart cam

rs
│
├── pipeline
│      │
│      ▼
│ pipeline_profile
│      │
│      ▼
│   device
│      │
│      ▼
│   sensors
│
└── config

sensor, hardware comp produces type of data.

Device
│
├── RGB Sensor
│      ├── Exposure
│      ├── Gain
│      └── White Balance
│
├── Depth Sensor
│      ├── Laser Power
│      ├── Exposure
│      └── Gain
│
└── Motion Sensor

get_info - info about sensor
supports - check whether sensor supports feature
get_option - read value of setting
set_option - change setting
open - prepare sensor for streaming
close - close sensor

pipeline
      │
      ▼
pipeline_profile
      │
      ▼
device
      │
      ▼
sensor
      │
      ▼
options

frameset
container that groups together sync frames from all enabled streams.

Camera
   │
   ▼
RGB Sensor ─────────────┐
                        │
Depth Sensor ───────────┤
                        │
IR Sensor ──────────────┤
                        ▼
                 Synchronization
                        ▼
                  Frameset
                        ▼
                 Your Python Code
                 
get_color_frame - get rgb frame
get_depth_frame - get depth frame
first - get first frame of spec stream type
size - num of frames in frameset

frame - foundation object
A frame is the basic unit of data coming from a RealSense camera. one capt piece of data at one moment in time.

depth.get_distance(x,y)
frame.get_timestamp - capture time
get_data - access raw image data
get_frame_number - frame seq num
get_profile - info about stream
supports_frame_metadat - check metadata avail
get_frame_metadata - read metadata
keep - 

Camera Sensors
      │
      ▼
pipeline
      │
      ▼
frameset
      │
      ├─────────────┐
      ▼             ▼
depth_frame     video_frame
      │             │
      ▼             ▼
depth data      RGB data
      │             │
      ▼             ▼
 NumPy         NumPy
      │             │
      ▼             ▼
 OpenCV / AI processing
 
 depth_frame 
 pixel to distance. a 2d image where every pixel containes distance infor.
 
 get_distance(x,y) - gives distance at pixel
 get_depth_scale - returns depth
 
 video_frame, frame having pixels arranged in 2D image.
 
 stream, continuous flow of data from sensor.
 
 rs.stream.depth

rs.stream.color

rs.stream.infrared

rs.stream.gyro

rs.stream.accel

config.enable_stream(
    stream_type,
    width,
    height,
    format,
    fps
)

config.enable_stream(
    rs.stream.color,
    640,
    480,
    rs.format.bgr8,
    30
)

rs.format.bgr8
rs.format.z16

get_streams - 

camera options(rs.option)

sensor.set_option(rs.option_gain, 200)

gain - how much elec sig is amplified
exposure - how long sensor collects light
sensor.supports(option)
if lighting is fixed, use manual exposure, every frame has consistent brightness.

cam intrinsics - how cam sees the world (focal length, principal point, distortion)
extrinsics - relation bn rgb and depth cameras
coordinate transf - conv 2D pixel + depth into 3D point (x,y,z)
alignment - making rgb & depth correspond pixel-to-pixel
filters - improve depth quality
pcd - gen a 3D rep of scene.

 pixel, a location on the image.
Width, Height - image resol

ppx, ppy - principal point (optional center of cam), now always exactly center xel

fx, fy - focal length in pixel units.
fx, high - more zoom and narrow fov, low . wider fov

Distortion Model - straight lines may appear curved, cam stores distortion params so software can comp for this effect.

without intrinsics, we cant compute real world position. it determines fov, distortion, zoom.

Distortion Coefficients

img pixel + depth + intrinsics -> real 3d coord.

Extrinsics - how cam real to each other
from one coord to other
several cams inside one device
RealSense D455

+--------------------------------------+
|                                      |
|  [IR Left] [IR Right]   [RGB Camera] |
|                                      |
+--------------------------------------+

pixel to 3d coordinates
deprojection, reversing cam projection.

rs.rs2_deproject_pixel_to_point(
    intrinsics,
    pixel,
    depth
)

Alignment -rs.align
both rdb, depth sees same obj at diff pixel.
align = rs.align(rs.stream.color)

needs info, calib, intr, extr, target stream
not only same timestamp, it will show same pixel correspond to same point in scene.

aligned_frames = align.process(frames)
It processes the entire synchronized frameset and returns another frameset where the requested stream has been transformed.

Camera
   │
   ▼
Pipeline
   │
   ▼
Frameset
   │
   ▼
Alignment
   │
   ▼
Aligned Frameset
   │
   ├─────────────┐
   ▼             ▼
Color Frame   Depth Frame
   │             │
   └──────┬──────┘
          ▼
Same pixel = Same real-world point

filters (imp depth quality)
some pixels are noisy, missing, outliers.
filters are also classes.

spatial filter - smooth neighboring pixels. This reduces random pixel-to-pixel noise while trying to preserve edges.
temporal filter - use time, variation is sensor noise, compare consecutive frames and smooths those fluctuations. across time.
hole filling filter - when depth cannot be measured, value is 0, it estimates a reasonable value using nearby valid pixels.
chaining filters - filters are often used together
decimation filter - reduce resolution

A Spatial Filter looks at neighboring pixels within the same frame. The noise is changing between frames, not between neighboring pixels.The wall is stationary, so the same pixel should report nearly the same depth over time. temp - across time - mult frames, spatial - across neigh pixels - same frame.

PCD 

rs.pointcloud
pc.calculate(depth_frame)
pc.map_to(color_frame)

Recodring & Play bag
bag file is like video recording, much richer

IMU ( Gyroscope & Accelerometer ) - motion sensors
accelerometer - measures linear acceleration
gyro - measures ang acceleration

