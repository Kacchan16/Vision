from __future__ import annotations
import sys
import pyrealsense2 as rs


def main() -> int:
    context = rs.context()
    devices = context.query_devices()

    if len(devices) == 0:
        print("No RealSense camera is detected.")
        return 1

    print(f"Found {len(devices)} RealSense device(s):")

    for index, device in enumerate(devices):
        name = device.get_info(rs.camera_info.name)
        serial = device.get_info(rs.camera_info.serial_number)
        firmware = device.get_info(rs.camera_info.firmware_version)

        print(f"Camera {index}")
        print(f"  Name: {name}")
        print(f"  Serial: {serial}")
        print(f"  Firmware: {firmware}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
