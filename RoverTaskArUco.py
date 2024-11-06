import cv2
import cv2.aruco as aruco
import time
import rospy
from std_msgs.msg import String
import os

rospy.init_node('aruco_detector_node', anonymous=True)
trajectory_pub = rospy.Publisher('/trajectory_info', String, queue_size=10)

fps = 15   # kameranın fps i ve publisher ın hz = fps
VideoCap = False
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, fps)
print("Current FPS:", cap.get(cv2.CAP_PROP_FPS))
print(cv2.__version__)
rate = rospy.Rate(fps)


if VideoCap is False: # kamera kullanılmicaksa fotoğraf klasörleri
    image_directory = "./aruco_tags/"
    save_directory = "./processed_images/"
    os.makedirs(save_directory, exist_ok=True) 


def findAruco(img, draw=True):   # detection func
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    arucoDict = aruco.getPredefinedDictionary(aruco.DICT_4X4_1000)
    arucoParam = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(arucoDict, arucoParam)
    corners, ids, _ = detector.detectMarkers(gray)

    direction_info = ""    # publischlenecek yazı

    if ids is not None:       # fotonun ve tag in orta noktaları 
        for corner in corners:
            x_min = min(corner[0][:, 0]) 
            x_max = max(corner[0][:, 0])  
            y_min = min(corner[0][:, 1])  
            y_max = max(corner[0][:, 1])  

            center_x = (x_min + x_max) / 2
            center_y = (y_min + y_max) / 2

            img_center_x = img.shape[1] / 2
            img_center_y = img.shape[0] / 2

            cv2.arrowedLine(img, (int(img_center_x), int(img_center_y)), (int(center_x), int(center_y)), (255, 0, 0), 2)

            if center_x < img_center_x:
                direction_info += "Move Left, "
            elif center_x > img_center_x:
                direction_info += "Move Right, "

        aruco.drawDetectedMarkers(img, corners, ids)
        
    if direction_info: # pub
        direction_info_cleaned = direction_info.strip(", ")
        trajectory_pub.publish(direction_info.strip(", "))
        print(f"Published message: {direction_info_cleaned}") 
    
    return corners, ids, img

processed_files = set() 

while not rospy.is_shutdown():
    if VideoCap:   # kamera kullanılıyorsa
        rate.sleep() 
        _, img = cap.read()
    else:  # klasördeki foto checkleme için
        for filename in os.listdir(image_directory):
            if filename.endswith((".jpg", ".jpeg", ".png", "webp")):
                img_path = os.path.join(image_directory, filename)
                img = cv2.imread(img_path)
            if filename in processed_files:
                break 

            corners, ids, processed_img = findAruco(img)
            if ids is not None: 
                save_path = os.path.join(save_directory, f"processed_{filename}")
                cv2.imwrite(save_path, processed_img)
                print(f"Saved: {save_path}")
                cv2.imshow("img", processed_img)
                processed_files.add(filename)

    bbox, ids, corners = findAruco(img)
    if  processed_files:
        break
    if cv2.waitKey(1) == 113:  # q to quit
        break
    cv2.imshow("img", img)

    continue

cap.release()
cv2.destroyAllWindows()
