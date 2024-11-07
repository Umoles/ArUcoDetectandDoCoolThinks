# ArUcoDetectandDoCoolThings
Our first goal in this repository is to detect ArUco tags. After ArUco Tag detection, a vector is drawn from the midpoint of the image to the midpoint of the detected tag. Our aim is to publish to other nodes via ROS the direction in which the vehicle, which is assumed to move towards the tag, should move and to ensure that the vehicle arrives at the right place with a high accuracy rate.

Bu repositoryde amacımız ilk olarak ArUco tag tespitidir. ArUco Tag tespiti sonrasında görüntünün orta noktasından, tespit edilmiş tagin orta noktasına bir vektör çizilir. Amacımız bu şekilde tag'e doğru hareket edileceği varsayılan aracın hangi yönde ilerlemesi gerektiği ros aracılığıyla diğer node'lara publischlemek ve yüksek doğruluk oranıyla aracın doğru yere varışının sağlamaktır.

## 1. Prerequisites
- [Python](https://www.python.org/downloads/)
- [ROS](http://wiki.ros.org/ROS/Installation)

```
    # if your cv2 version is lover then 4.7 syntax must be changed but it should still work 
    python3 -m pip install opencv-contrib-python
    pip3 install -U opencv-contrib-python

```
## 2. Usage
    Clone Rep on your work space.
    run roscore 
    cd ArUcoDetectandDoCoolThings

    python3 RoverTaskArUco.py
#if VideoCap = True it ll run your camera. If it is False it ll detect all photos in your directory(image_directory)

![](./processed_ArUco4.jpeg)
