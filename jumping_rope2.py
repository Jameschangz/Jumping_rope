import cv2
import mediapipe as mp
import math

# 定义一个函数，用于计算两个关键点之间的角度
def get_angle(a, b):
    radians = math.atan2(b.y - a.y, b.x - a.x)
    angle = math.degrees(radians)
    return angle

# 创建视频捕获对象
cap = cv2.VideoCapture(0)

# 创建一个实例来进行姿势估计
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# 初始化变量
jumping = False
count = 0

# 创建两个 OpenCV 窗口
cv2.namedWindow("健身功能", cv2.WINDOW_NORMAL)
cv2.namedWindow("人体点位图", cv2.WINDOW_NORMAL)

while True:
    # 读取视频帧
    success, image = cap.read()
    if not success:
        print("无法读取视频")
        break

    # 转换颜色空间
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 进行姿势估计
    results = pose.process(image)

    # 在图像中绘制关键点
    if results.pose_landmarks is not None:
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # 获取跳绳需要检测的关键点
        left_ankle = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE]
        right_ankle = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE]
        left_knee = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]
        right_knee = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE]

        # 计算腿部角度
        left_leg_angle = get_angle(left_ankle, left_knee)
        right_leg_angle = get_angle(right_ankle, right_knee)

        # 判断是否符合跳绳动作
        if left_leg_angle > 160 and right_leg_angle > 160:
            if not jumping:
                jumping = True
                count += 1
        else:
            jumping = False

        # 显示跳绳次数
        cv2.putText(image, "跳绳次数: {}".format(count), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # 在另一个窗口中显示人体点位图
        annotated_image = image.copy()
        mp_drawing.draw_landmarks(annotated_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        cv2.imshow("人体点位图", annotated_image)

    # 显示图像
    cv2.imshow("健身功能", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        breakq

# 释放资源
cap.release()
cv2.destroyAllWindows()
