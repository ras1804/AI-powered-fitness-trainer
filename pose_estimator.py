import cv2
import mediapipe as mp
import math


class poseDetector():
    def __init__(self, mode=False, smooth=True, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(
            static_image_mode=self.mode,
            smooth_landmarks=self.smooth,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )

    def findPose(self, img, draw=True):
        # Validate input image
        if img is None or img.size == 0:
            print("Error: Empty image received in findPose")
            return img if img is not None else None

        try:
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.results = self.pose.process(imgRGB)

            if self.results.pose_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        img,
                        self.results.pose_landmarks,
                        self.mpPose.POSE_CONNECTIONS
                    )
        except Exception as e:
            print(f"Error in findPose: {e}")

        return img

    def getPosition(self, img, draw=True):
        self.lmList = []

        # Validate input image
        if img is None or img.size == 0:
            print("Error: Empty image received in getPosition")
            return self.lmList

        try:
            if self.results.pose_landmarks:
                for id, lm in enumerate(self.results.pose_landmarks.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    self.lmList.append([id, cx, cy])
                    if draw:
                        cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        except Exception as e:
            print(f"Error in getPosition: {e}")

        return self.lmList

    def findAngle(self, img, p1, p2, p3, draw=True):
        # Validate input image
        if img is None or img.size == 0:
            print("Error: Empty image received in findAngle")
            return 0

        try:
            # Get the landmarks
            if len(self.lmList) == 0:
                return 0

            x1, y1 = self.lmList[p1][1:]
            x2, y2 = self.lmList[p2][1:]
            x3, y3 = self.lmList[p3][1:]

            # Calculate the angle
            angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                                 math.atan2(y1 - y2, x1 - x2))

            if angle < 0:
                angle += 360

            # Draw
            if draw:
                cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
                cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
                cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
                cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
                cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
                cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

            return angle
        except Exception as e:
            print(f"Error in findAngle: {e}")
            return 0


def main():
    cap = cv2.VideoCapture('R.gif')

    # Check if video opened successfully
    if not cap.isOpened():
        print("Error: Could not open video file 'R.gif'")
        return

    detector = poseDetector()

    while True:
        success, img = cap.read()

        # Check if frame was read successfully
        if not success or img is None:
            print("End of video or could not read frame")
            break

        img = detector.findPose(img)
        lmList = detector.getPosition(img)

        if len(lmList) != 0:
            print(lmList[0])  # Print first landmark as example

        cv2.imshow('Image', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()