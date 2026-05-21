import cv2
import numpy as np
import pose_estimator_module as pm
import streamlit as st


def process_exercise(video_path, exercise_type):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        st.error("Error: Could not open video")
        return

    detector = pm.poseDetector()

    count = 0
    dir1 = 0
    dir2 = 0

    stframe = st.empty()

    while True:
        success, img = cap.read()

        if not success or img is None:
            break

        img = detector.findPose(img, False)
        lmList = detector.getPosition(img, draw=False)

        if len(lmList) != 0:

            # ================= EXERCISE ANGLES =================

            if exercise_type == "pushup":
                angle1 = detector.findAngle(img, 12, 14, 16)
                angle2 = detector.findAngle(img, 11, 13, 15)

                per1 = np.interp(angle1, (60, 180), (0, 100))
                per2 = np.interp(angle2, (60, 180), (0, 100))

            elif exercise_type == "squat":
                angle1 = detector.findAngle(img, 24, 26, 28)
                angle2 = detector.findAngle(img, 23, 25, 27)

                per1 = np.interp(angle1, (76, 180), (0, 100))
                per2 = np.interp(angle2, (76, 180), (0, 100))

            elif exercise_type == "curl":
                angle1 = detector.findAngle(img, 12, 14, 16)
                angle2 = detector.findAngle(img, 11, 13, 15)

                per1 = np.interp(angle1, (70, 230), (0, 100))
                per2 = np.interp(angle2, (70, 230), (0, 100))

            # ================= REP COUNT =================

            if per1 >= 99 or per2 >= 99:
                if dir1 == 0 or dir2 == 0:
                    count += 0.5
                    dir1, dir2 = 1, 1

            if per1 <= 1 or per2 <= 1:
                if dir1 == 1 or dir2 == 1:
                    count += 0.5
                    dir1, dir2 = 0, 0

            # ================= UI =================

            cv2.rectangle(img, (0, 0), (200, 100), (0, 255, 0), cv2.FILLED)

            cv2.putText(
                img,
                f"Reps: {int(count)}",
                (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (255, 0, 0),
                3
            )

        # Convert BGR to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Display in Streamlit
        stframe.image(img, channels="RGB")

    cap.release()


def pushUps(video_path):
    process_exercise(video_path, "pushup")


def squats(video_path):
    process_exercise(video_path, "squat")


def bicepCurls(video_path):
    process_exercise(video_path, "curl")

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
