
import cv2
import mediapipe as mp
import numpy as np
import streamlit as st
import tempfile
import time

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils


# ================= ANGLE FUNCTION =================

def calculate_angle(a, b, c):

    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(
        c[1] - b[1],
        c[0] - b[0]
    ) - np.arctan2(
        a[1] - b[1],
        a[0] - b[0]
    )

    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180:
        angle = 360 - angle

    return angle


# ================= MAIN VIDEO PROCESSOR =================

def process_video(video_path, exercise):

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        st.error("Could not open video.")
        return

    frame_placeholder = st.empty()
    counter_placeholder = st.empty()

    counter = 0
    stage = None

    with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as pose:

        while cap.isOpened():

            ret, frame = cap.read()

            if not ret:
                break

            # Resize for smoother streaming
            frame = cv2.resize(frame, (640, 480))

            # Convert color
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Pose detection
            results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:

                landmarks = results.pose_landmarks.landmark

                # ================= BICEP CURL =================

               # ================= BICEP CURL =================

if exercise == "curl":

    # RIGHT ARM
    right_shoulder = [
        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y
    ]

    right_elbow = [
        landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
        landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y
    ]

    right_wrist = [
        landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
        landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y
    ]

    right_angle = calculate_angle(
        right_shoulder,
        right_elbow,
        right_wrist
    )

    # LEFT ARM
    left_shoulder = [
        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y
    ]

    left_elbow = [
        landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
        landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y
    ]

    left_wrist = [
        landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
        landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y
    ]

    left_angle = calculate_angle(
        left_shoulder,
        left_elbow,
        left_wrist
    )

    # Use the arm with smaller angle
    angle = min(right_angle, left_angle)

    # Display angle
    cv2.putText(
        image,
        str(int(angle)),
        (50, 150),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2,
        cv2.LINE_AA
    )

    # MUCH BETTER CURL THRESHOLDS
    if angle > 140:
        stage = "down"

    if angle < 75 and stage == "down":
        stage = "up"
        counter += 1

            # ================= UI DISPLAY =================

            # Counter Box
            cv2.rectangle(
                image,
                (0, 0),
                (250, 80),
                (245, 117, 16),
                -1
            )

            cv2.putText(
                image,
                'REPS',
                (15, 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 0),
                2,
                cv2.LINE_AA
            )

            cv2.putText(
                image,
                str(counter),
                (15, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.8,
                (255, 255, 255),
                3,
                cv2.LINE_AA
            )

            # Stage
            cv2.putText(
                image,
                'STAGE',
                (120, 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 0),
                2,
                cv2.LINE_AA
            )

            cv2.putText(
                image,
                str(stage),
                (120, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (255, 255, 255),
                3,
                cv2.LINE_AA
            )

            # Draw landmarks
            if results.pose_landmarks:

                mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(
                        color=(245, 117, 66),
                        thickness=2,
                        circle_radius=2
                    ),
                    mp_drawing.DrawingSpec(
                        color=(245, 66, 230),
                        thickness=2,
                        circle_radius=2
                    )
                )

            # Convert for Streamlit
            display_image = cv2.cvtColor(
                image,
                cv2.COLOR_BGR2RGB
            )

            # REAL-TIME FRAME UPDATE
            frame_placeholder.image(
                display_image,
                channels="RGB",
                use_container_width=True
            )

            # Live counter update
            counter_placeholder.markdown(
                f"## Reps Count: {counter}"
            )

            # IMPORTANT:
            # Small delay for actual video movement
            time.sleep(0.03)

    cap.release()

    st.success(f"Finished! Total Reps: {counter}")


# ================= EXERCISE FUNCTIONS =================

def bicepCurls(video_path):
    process_video(video_path, "curl")


def squats(video_path):
    process_video(video_path, "squat")


def pushUps(video_path):
    process_video(video_path, "pushup")

# import cv2
# import numpy as np
# import time
# import pose_estimator_module as pm


# def pushUps(para1):
#     # Handle webcam vs file
#     if para1 is None:
#         cap = cv2.VideoCapture(0)  # webcam
#     else:
#         cap = cv2.VideoCapture(para1)

#     # Check if camera/video opened successfully
#     if not cap.isOpened():
#         print("Error: Could not open video source")
#         return

#     detector = pm.poseDetector()
#     count = 0
#     dir1 = 0
#     dir2 = 0

#     # Get FPS of video if using a file
#     fps = int(cap.get(cv2.CAP_PROP_FPS))
#     delay = int(1000 / fps) if fps > 0 else 1

#     frame_skip = 2
#     frame_count = 0

#     while True:
#         success, img = cap.read()

#         # Check if frame was read successfully
#         if not success or img is None:
#             print("Error: Could not read frame or end of video")
#             break

#         frame_count += 1
#         if frame_count % frame_skip != 0:
#             continue

#         img = detector.findPose(img, False)
#         lmList = detector.getPosition(img, draw=False)

#         if len(lmList) != 0:
#             angle1 = detector.findAngle(img, 12, 14, 16)
#             angle2 = detector.findAngle(img, 11, 13, 15)

#             per1 = np.interp(angle1, (60, 180), (0, 100))
#             per2 = np.interp(angle2, (60, 180), (0, 100))

#             # check for the push-up
#             if per1 >= 95 or per2 >= 95:
#                 if dir1 == 0 or dir2 == 0:
#                     count += 0.5
#                     dir1, dir2 = 1, 1

#             if per1 <= 5 or per2 <= 5:
#                 if dir1 == 1 or dir2 == 1:
#                     count += 0.5
#                     dir1, dir2 = 0, 0

#             # Display counter
#             cv2.rectangle(img, (0, 250), (150, 580), (0, 255, 0), cv2.FILLED)
#             cv2.putText(
#                 img,
#                 str(int(count)),
#                 (50, 360),
#                 cv2.FONT_HERSHEY_PLAIN,
#                 5,
#                 (255, 0, 0),
#                 7
#             )

#     cap.release()


# def squats(para1):
#     if para1 is None:
#         cap = cv2.VideoCapture(0)
#     else:
#         cap = cv2.VideoCapture(para1)

#     # Check if camera/video opened successfully
#     if not cap.isOpened():
#         print("Error: Could not open video source")
#         return

#     detector = pm.poseDetector()
#     count = 0
#     dir1 = 0
#     dir2 = 0

#     while True:
#         success, img = cap.read()

#         # Check if frame was read successfully
#         if not success or img is None:
#             print("Error: Could not read frame or end of video")
#             break

#         img = detector.findPose(img, False)
#         lmList = detector.getPosition(img, draw=False)

#         if len(lmList) != 0:
#             angle1 = detector.findAngle(img, 24, 26, 28)
#             angle2 = detector.findAngle(img, 23, 25, 27)

#             per1 = np.interp(angle1, (76, 180), (0, 100))
#             per2 = np.interp(angle2, (76, 180), (0, 100))

#             # check for the squat
#             if per1 >= 95 or per2 >= 95:
#                 if dir1 == 0 or dir2 == 0:
#                     count += 0.5
#                     dir1, dir2 = 1, 1

#             if per1 <= 5 or per2 <= 5:
#                 if dir1 == 1 or dir2 == 1:
#                     count += 0.5
#                     dir1, dir2 = 0, 0

#             cv2.rectangle(img, (0, 350), (150, 720), (0, 255, 0), cv2.FILLED)
#             cv2.putText(
#                 img,
#                 str(int(count)),
#                 (50, 460),
#                 cv2.FONT_HERSHEY_PLAIN,
#                 5,
#                 (255, 0, 0),
#                 7
#             )

#     cap.release()


# def bicepCurls(para1):
#     if para1 is None:
#         cap = cv2.VideoCapture(0)
#     else:
#         cap = cv2.VideoCapture(para1)

#     # Check if camera/video opened successfully
#     if not cap.isOpened():
#         print("Error: Could not open video source")
#         return

#     detector = pm.poseDetector()
#     count = 0
#     dir1 = 0
#     dir2 = 0

#     while True:
#         success, img = cap.read()

#         # Check if frame was read successfully
#         if not success or img is None:
#             print("Error: Could not read frame or end of video")
#             break

#         img = detector.findPose(img, False)
#         lmList = detector.getPosition(img, draw=False)

#         if len(lmList) != 0:
#             angle1 = detector.findAngle(img, 12, 14, 16)
#             angle2 = detector.findAngle(img, 11, 13, 15)

#             per1 = np.interp(angle1, (70, 230), (0, 100))
#             per2 = np.interp(angle2, (70, 230), (0, 100))

#             # check for the dumbbell curls
#             if per1 >= 95 or per2 >= 95:
#                 if dir1 == 0 or dir2 == 0:
#                     count += 0.5
#                     dir1, dir2 = 1, 1

#             if per1 <= 5 or per2 <= 5:
#                 if dir1 == 1 or dir2 == 1:
#                     count += 0.5
#                     dir1, dir2 = 0, 0

#             cv2.rectangle(img, (0, 350), (150, 720), (0, 255, 0), cv2.FILLED)
#             cv2.putText(
#                 img,
#                 str(int(count)),
#                 (50, 460),
#                 cv2.FONT_HERSHEY_PLAIN,
#                 5,
#                 (255, 0, 0),
#                 7
#             )

#     cap.release()

# import cv2
# import numpy as np
# import time
# import pose_estimator_module as pm


# def pushUps(para1):
#     # Handle webcam vs file
#     if para1 is None:
#         cap = cv2.VideoCapture(0)  # webcam
#     else:
#         cap = cv2.VideoCapture(para1)

#         # Check if camera/video opened successfully
#     if not cap.isOpened():
#         print("Error: Could not open video source")
#         return

#     detector = pm.poseDetector()
#     count = 0
#     dir1 = 0
#     dir2 = 0

#     # Get FPS of video if using a file
#     fps = int(cap.get(cv2.CAP_PROP_FPS))
#     delay = int(1000 / fps) if fps > 0 else 1  # milliseconds

#     frame_skip = 2  # process every 2nd frame
#     frame_count = 0

#     while True:
#         success, img = cap.read()

#         # Check if frame was read successfully
#         if not success or img is None:
#             print("Error: Could not read frame or end of video")
#             break

#         frame_count += 1
#         if frame_count % frame_skip != 0:
#             continue  # skip frame

#         img = detector.findPose(img, False)
#         lmList = detector.getPosition(img, draw=False)

#         if len(lmList) != 0:
#             angle1 = detector.findAngle(img, 12, 14, 16)  # Right arm
#             angle2 = detector.findAngle(img, 11, 13, 15)  # Left arm

#             per1 = np.interp(angle1, (60, 180), (0, 100))
#             per2 = np.interp(angle2, (60, 180), (0, 100))

#             # check for the push-up
#             if per1 == 100 or per2 == 100:
#                 if dir1 == 0 or dir2 == 0:
#                     count += 0.5
#                     dir1, dir2 = 1, 1

#             if per1 == 0 or per2 == 0:
#                 if dir1 == 1 or dir2 == 1:
#                     count += 0.5
#                     dir1, dir2 = 0, 0

#             # Display counter
#             cv2.rectangle(img, (0, 250), (150, 580), (0, 255, 0), cv2.FILLED)
#             cv2.putText(img, str(int(count)), (50, 360),
#                         cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 7)

#         cv2.imshow("Image", img)

#         # Use delay based on FPS (makes playback real-time speed)
#         if cv2.waitKey(delay) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()


# def squats(para1):
#     if para1 is None:
#         cap = cv2.VideoCapture(0)  # webcam
#     else:
#         cap = cv2.VideoCapture(para1)

#         # Check if camera/video opened successfully
#     if not cap.isOpened():
#         print("Error: Could not open video source")
#         return

#     detector = pm.poseDetector()
#     count = 0
#     dir1 = 0
#     dir2 = 0

#     while True:
#         success, img = cap.read()

#         # Check if frame was read successfully
#         if not success or img is None:
#             print("Error: Could not read frame or end of video")
#             break

#         img = detector.findPose(img, False)
#         lmList = detector.getPosition(img, draw=False)

#         if len(lmList) != 0:
#             angle1 = detector.findAngle(img, 24, 26, 28)  # Right leg
#             angle2 = detector.findAngle(img, 23, 25, 27)  # Left leg

#             per1 = np.interp(angle1, (76, 180), (0, 100))
#             per2 = np.interp(angle2, (76, 180), (0, 100))

#             # check for the squat
#             if per1 == 100 or per2 == 100:
#                 if dir1 == 0 or dir2 == 0:
#                     count += 0.5
#                     dir1, dir2 = 1, 1

#             if per1 == 0 or per2 == 0:
#                 if dir1 == 1 or dir2 == 1:
#                     count += 0.5
#                     dir1, dir2 = 0, 0

#             cv2.rectangle(img, (0, 350), (150, 720), (0, 255, 0), cv2.FILLED)
#             cv2.putText(img, str(int(count)), (50, 460), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 7)

#         cv2.imshow("Image", img)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()


# def bicepCurls(para1):
#     if para1 is None:
#         cap = cv2.VideoCapture(0)  # webcam
#     else:
#         cap = cv2.VideoCapture(para1)

#         # Check if camera/video opened successfully
#     if not cap.isOpened():
#         print("Error: Could not open video source")
#         return

#     detector = pm.poseDetector()
#     count = 0
#     dir1 = 0
#     dir2 = 0

#     while True:
#         success, img = cap.read()

#         # Check if frame was read successfully
#         if not success or img is None:
#             print("Error: Could not read frame or end of video")
#             break

#         img = detector.findPose(img, False)
#         lmList = detector.getPosition(img, draw=False)

#         if len(lmList) != 0:
#             angle1 = detector.findAngle(img, 12, 14, 16)  # Right Arm
#             angle2 = detector.findAngle(img, 11, 13, 15)  # Left Arm

#             per1 = np.interp(angle1, (70, 230), (0, 100))
#             per2 = np.interp(angle2, (70, 230), (0, 100))

#             # check for the dumbbell curls
#             if per1 == 100 or per2 == 100:
#                 if dir1 == 0 or dir2 == 0:
#                     count += 0.5
#                     dir1, dir2 = 1, 1

#             if per1 == 0 or per2 == 0:
#                 if dir1 == 1 or dir2 == 1:
#                     count += 0.5
#                     dir1, dir2 = 0, 0

#             cv2.rectangle(img, (0, 350), (150, 720), (0, 255, 0), cv2.FILLED)
#             cv2.putText(img, str(int(count)), (50, 460), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 7)

#         cv2.imshow("Image", img)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()
