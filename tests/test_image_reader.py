from realsense_shm.reader import SharedMemoryReader
import numpy as np
import cv2

color_shape = (480, 640, 3)
depth_shape = (480, 640)
color_reader = SharedMemoryReader("cam_color",
                                    color_shape, np.uint8)

while True:
    image = color_reader.read()
    print(image.shape)
    cv2.imshow('Window Title', image)    
    # 3. Wait 1ms for key input AND check if it's the 'q' key
    # This small delay is mandatory to let OpenCV render the frame
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 4. Clean up resources
cv2.destroyAllWindows()

