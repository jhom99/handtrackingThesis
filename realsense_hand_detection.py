import cv2
import socket
import numpy as np
import mediapipe as mp
import pyrealsense2 as rs

# @author Julian Hom,
# sources: concept of sending data to Unity via udp from 'cv-zone 3d-handtracking' - course https://www.computervision.zone/courses/3d-hand-tracking/
class UDPSocket:
    def __init__(self, address=("127.0.0.1", 2020)):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = address
        
    def sendData(self, data):
        self.socket.sendto(str.encode(str(data)), self.address)

class RealsenseSetup:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.pipeline = rs.pipeline()
        self.config = rs.config()

        self.config.enable_stream(rs.stream.depth, self.width, self.height, rs.format.z16, 30)
        self.config.enable_stream(rs.stream.color, self.width, self.height, rs.format.bgr8, 30)

        self.pipeline.start(self.config)
        align_to = rs.stream.color
        self.align = rs.align(align_to)
        # Get depth scale for converting depth values to meters
        self.depth_scale = self.pipeline.get_active_profile().get_device().first_depth_sensor().get_depth_scale()
        
    
    def stopStream(self):
        self.pipeline.stop()
        
    def get_frames(self):
        frames = self.pipeline.wait_for_frames()
        aligned_frames = self.align.process(frames)
        aligned_depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        
        if not aligned_depth_frame or not color_frame:
            return False, None, None
        

        spatial = rs.spatial_filter()
        spatial.set_option(rs.option.holes_fill, 3)
        filtered_depth = spatial.process(aligned_depth_frame)

        hole_filling = rs.hole_filling_filter()
        filled_depth = hole_filling.process(filtered_depth)
        
        return color_frame, filled_depth

class HandDetector:
    def __init__(self, max_num_hands = 1, min_detection_confidence = 0.7, min_tracking_confidence = 0.7):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands = max_num_hands,
            min_detection_confidence = min_detection_confidence,
            min_tracking_confidence = min_tracking_confidence
        )
        
    def detectHand(self, color_frame):
        results = self.hands.process(color_frame)
        if results.multi_hand_landmarks:
        
            hand_landmarks = results.multi_hand_landmarks[0]

            return hand_landmarks
        else:
            print('Handmarks could not be detected!')
            

if __name__ == "__main__":
    # Define UDP server address with localhost and any free port on system, might not be 2020 on on other System
    udp_socket_address = ("127.0.0.1", 2020)

    # Create instances of the Camera, HandDetector, and UDPConnection classes
    camera = RealsenseSetup(848,480)
    detector = HandDetector()
    udp_socket = UDPSocket(udp_socket_address)
    
    #create arrays that will hold image data
    color_image = np.empty((480, 848, 3), dtype=np.uint8)
    depth_image = np.empty((480, 848), dtype=np.uint16)

    while True:
        #get frames from camera
        color_frame, depth_frame = camera.get_frames()
        color_image = np.asanyarray(color_frame.get_data(), dtype=np.uint8)
        depth_image = np.asanyarray(depth_frame.get_data(), dtype=np.uint16)

        #define intrinsics of depth-stream, which are needed to get 3d position in camera coordinatesystem
        depth_intrinsics = depth_frame.profile.as_video_stream_profile().get_intrinsics()

        #Define list that will hold the landmarks and sent to Unity
        landmarks_xyz = []

        # Detect hand landmarks from the color frame
        hand_landmarks = detector.detectHand(color_image)
        if hand_landmarks:
             # Draw landmarks on the color image
            detector.mp_drawing.draw_landmarks(color_image, hand_landmarks, detector.mp_hands.HAND_CONNECTIONS)
            for landmark in hand_landmarks.landmark:
                # Get pixel coordinates of landmark
                x_pixel, y_pixel = int(landmark.x * color_image.shape[1]), int(landmark.y * color_image.shape[0])

                # this fixes position out of range error, which occurs on fast movements 
                # since the mediapipe model then sometimes estimates koordinates beyond the picture measurements
                if x_pixel >= color_image.shape[1]:
                    x_pixel = color_image.shape[1] - 1
                if y_pixel >= color_image.shape[0]:
                    y_pixel = color_image.shape[0] - 1
                    
                # Get depth value of landmark
                depth_value = depth_image[y_pixel, x_pixel]

                # Convert depth value to meters
                depth_meters = depth_value * camera.depth_scale


                # Get x, y, z coordinates of landmark in meters, y needs to be inverted since realsense's
                # coordinate system has 0-Point at the top
                landmark_xyz = rs.rs2_deproject_pixel_to_point(depth_intrinsics, [x_pixel, 480-y_pixel], depth_meters)
                
                # Append filtered x, y, and z coordinates to landmarks_xyz list
                landmarks_xyz.append(round(list(landmark_xyz)[0], 2))
                landmarks_xyz.append(round(list(landmark_xyz)[1], 2))
                landmarks_xyz.append(round(list(landmark_xyz)[2], 2))
                
            udp_socket.sendData(landmarks_xyz)
           

        # Display the color image
        cv2.imshow("Hand Detection", color_image)

        key = cv2.waitKey(1)
        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('q') or key == 27:
            break

    # Stop the camera pipeline and close all windows
    camera.stopStream()
    cv2.destroyAllWindows()