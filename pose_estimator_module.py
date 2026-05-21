import math
import cv2
import mediapipe as mp


class poseDetector():
    def __init__(
        self,
        mode=False,
        upBody=False,
        smooth=True,
        detectionCon=0.5,
        trackCon=0.5
    ):

        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose

        # IMPORTANT:
        # model_complexity=1 prevents MediaPipe from trying
        # to download the lite model in Streamlit Cloud
        self.pose = self.mpPose.Pose(
            static_image_mode=self.mode,
            model_complexity=1,
            smooth_landmarks=self.smooth,
            enable_segmentation=False,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )

        self.results = None
        self.lmList = []

    def findPose(self, img, draw=True):

        if img is None:
            return img

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        if self.results.pose_landmarks and draw:
            self.mpDraw.draw_landmarks(
                img,
                self.results.pose_landmarks,
                self.mpPose.POSE_CONNECTIONS
            )

        return img

    def getPosition(self, img, draw=True):

        self.lmList = []

        if self.results and self.results.pose_landmarks:

            for id, lm in enumerate(self.results.pose_landmarks.landmark):

                h, w, c = img.shape

                cx = int(lm.x * w)
                cy = int(lm.y * h)

                self.lmList.append([id, cx, cy])

                if draw:
                    cv2.circle(
                        img,
                        (cx, cy),
                        5,
                        (255, 0, 0),
                        cv2.FILLED
                    )

        return self.lmList

    def findAngle(self, img, p1, p2, p3, draw=True):

        if len(self.lmList) == 0:
            return 0

        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        angle = math.degrees(
            math.atan2(y3 - y2, x3 - x2) -
            math.atan2(y1 - y2, x1 - x2)
        )

        if angle < 0:
            angle += 360

        if draw:

            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 4)
            cv2.line(img, (x2, y2), (x3, y3), (0, 255, 0), 4)

            cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (255, 0, 0), 2)

            cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 0), 2)

            cv2.circle(img, (x3, y3), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (255, 0, 0), 2)

            cv2.putText(
                img,
                str(int(angle)),
                (x2 - 20, y2 + 50),
                cv2.FONT_HERSHEY_COMPLEX,
                2,
                (255, 0, 0),
                2
            )

        return angle

# import math
# import cv2
# import mediapipe as mp

# class poseDetector():
#     def __init__(self, mode=False, upBody=False, smooth=True, detectionCon=0.5, trackCon=0.5):
#         self.mode = mode
#         self.upBody = upBody
#         self.smooth = smooth
#         self.detectionCon = detectionCon
#         self.trackCon = trackCon

#         self.mpDraw = mp.solutions.drawing_utils
#         self.mpPose = mp.solutions.pose
#         self.pose = self.mpPose.Pose(
#             static_image_mode=self.mode,
#             model_complexity=1 if not self.upBody else 0, 
#             smooth_landmarks=self.smooth,
#             enable_segmentation=False,
#             min_detection_confidence=self.detectionCon,
#             min_tracking_confidence=self.trackCon
#         )

#         self.results = None 

    
#     def findPose(self, img, draw=True):
#         imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         self.results = self.pose.process(imgRGB) 

#         if self.results.pose_landmarks:
#             if draw:
#                 self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        
#         return img
    
#     def getPosition(self, img, draw=True):
#         self.lmList = []

#         if self.results and self.results.pose_landmarks:  
#             for id, lm in enumerate(self.results.pose_landmarks.landmark):
#                 h, w, c = img.shape
#                 cx, cy = int(lm.x * w), int(lm.y * h)
#                 self.lmList.append([id, cx, cy])
#                 if draw:
#                     cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        
#         return self.lmList
    
#     def findAngle(self, img, p1, p2, p3, draw = True):
        
#         _, x1, y1 = self.lmList[p1]
#         _, x2, y2 = self.lmList[p2]
#         _, x3, y3 = self.lmList[p3]

#         # Calculating angle
#         angle = math.atan2(y3-y2, x3-x2) - math.atan2(y1-y2, x1-x2)
#         angle = math.degrees(angle)

#         if angle < 0:
#             angle *= -1


#         if draw:

#             cv2.line(img, (x1,y1), (x2,y2), (0,255,0), 4)
#             cv2.line(img, (x2,y2), (x3,x3), (0,255,0), 4)

#             cv2.circle(img,(x1,y1), 10, (255,0,0), cv2.FILLED)
#             cv2.circle(img,(x1,y1), 15, (255,0,0), 2)

#             cv2.circle(img,(x2,y2), 10, (255,0,0), cv2.FILLED)
#             cv2.circle(img,(x2,y2), 15, (255,0,0), 2)

#             cv2.circle(img,(x3,y3), 10, (255,0,0), cv2
#             .FILLED)
#             cv2.circle(img,(x3,y3), 15, (255,0,0), 2)

#             cv2.putText(img, str(int(angle)),(x2-20, y2+50), cv2.FONT_HERSHEY_COMPLEX, 2, (255,0,0),2)

#         return angle
    

# import time
# def main():
#     cap = cv2.VideoCapture('AiTrainer/pushup1.mp4')
#     pTime = 0
#     detector = poseDetector()

#     while True:
#         success, img = cap.read()
#         img = detector.findPose(img)
#         lmList = detector.getPosition(img, draw=False)
#         cTime = time.time
        
#         cv2.imshow("WebCam", img)
#         cv2.waitKey(1)


# if __name__ == "__main__":
#     main()
