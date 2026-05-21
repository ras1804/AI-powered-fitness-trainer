
import cv2
import mediapipe as mp
import numpy as np
import streamlit as st
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


# ================= MAIN PROCESSOR =================

def process_video(video_path, exercise):

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        st.error("Cannot open uploaded video.")
        return

    stframe = st.empty()
    rep_text = st.empty()

    counter = 0
    stage = None

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as pose:

        frame_num = 0

        while True:

            success, frame = cap.read()

            if not success:
                break

            frame_num += 1

            # Skip some frames for Streamlit Cloud performance
            if frame_num % 2 != 0:
                continue

            try:

                frame = cv2.resize(frame, (640, 480))

                # Convert BGR to RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Process pose
                results = pose.process(image)

                if results.pose_landmarks:

                    landmarks = results.pose_landmarks.landmark

                    # ================= BICEP CURL =================

                    if exercise == "Bicep-Curl":

                        shoulder = [
                            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y
                        ]

                        elbow = [
                            landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y
                        ]

                        wrist = [
                            landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y
                        ]

                        angle = calculate_angle(
                            shoulder,
                            elbow,
                            wrist
                        )

                        if angle > 160:
                            stage = "down"

                        if angle < 40 and stage == "down":
                            stage = "up"
                            counter += 1

                    # ================= SQUATS =================

                    elif exercise == "Squats":

                        hip = [
                            landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y
                        ]

                        knee = [
                            landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y
                        ]

                        ankle = [
                            landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y
                        ]

                        angle = calculate_angle(
                            hip,
                            knee,
                            ankle
                        )

                        if angle > 160:
                            stage = "up"

                        if angle < 90 and stage == "up":
                            stage = "down"
                            counter += 1

                    # ================= PUSHUPS =================

                    elif exercise == "Push-Ups":

                        shoulder = [
                            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y
                        ]

                        elbow = [
                            landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y
                        ]

                        wrist = [
                            landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y
                        ]

                        angle = calculate_angle(
                            shoulder,
                            elbow,
                            wrist
                        )

                        if angle > 160:
                            stage = "up"

                        if angle < 90 and stage == "up":
                            stage = "down"
                            counter += 1

                    # Draw landmarks
                    mp_drawing.draw_landmarks(
                        image,
                        results.pose_landmarks,
                        mp_pose.POSE_CONNECTIONS
                    )

                # Draw counter box
                cv2.rectangle(
                    image,
                    (0, 0),
                    (250, 80),
                    (0, 0, 0),
                    -1
                )

                cv2.putText(
                    image,
                    f"REPS: {counter}",
                    (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                    cv2.LINE_AA
                )

                # Show frame
                stframe.image(
                    image,
                    channels="RGB",
                    use_container_width=True
                )

                rep_text.markdown(f"## Reps Count: {counter}")

                # Small delay helps Streamlit refresh
                time.sleep(0.03)

            except Exception as e:
                st.warning(f"Frame skipped due to error: {e}")
                continue

    cap.release()

    st.success(f"Finished Processing! Final Reps: {counter}")


# ================= EXERCISES =================

def bicepCurls(video_path):
    process_video(video_path, "Bicep-Curl")


def squats(video_path):
    process_video(video_path, "Squats")


def pushUps(video_path):
    process_video(video_path, "Push-Ups")


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
