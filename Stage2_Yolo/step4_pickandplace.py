import cv2
import time
from collections import deque
from ultralytics import YOLO
from pymycobot.mycobot import MyCobot

# 1. MyCobot 연결
mc = MyCobot('/dev/ttyUSB0')  # 포트는 환경에 맞게 수정
mc.set_gripper_state(0, 50)  # 그리퍼 열기 (초기화)

# 2. YOLO 모델 불러오기
model = YOLO("best.pt")  # 네가 학습한 색상 분류용 모델로 바꿔줘야 함

# 3. 웹캠 설정
cap = cv2.VideoCapture(0)

# 4. 색상별 타워 위치 (get_coords()로 티칭한 좌표 넣어줘!)
tower_positions = {
    "red":    [200, 0, 50, 0, 0, 90],
    "blue":   [220, 0, 50, 0, 0, 90],
    "green":  [240, 0, 50, 0, 0, 90],
    "yellow": [260, 0, 50, 0, 0, 90]
}

# 5. 파라미터 설정
block_height = 30
z_pick = 40
z_safe = 80

# 6. 픽셀 → 로봇 좌표 변환 함수 (보정 필요)
def pixel_to_robot(u, v):
    # 이 부분은 사용 환경에 맞게 보정 필요!
    scale_x = 0.4
    scale_y = 0.4
    offset_x = 100
    offset_y = -50
    x = u * scale_x + offset_x
    y = v * scale_y + offset_y
    z = z_pick
    return [x, y, z, 0, 0, 90]

# 7. 중심 좌표 정지 판단 버퍼
pos_buffer = deque(maxlen=10)
ready_to_pick = False
last_detection_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # 1) YOLO로 블록 감지
    results = model(frame)
    boxes = results[0].boxes

    if len(boxes) == 1:
        box = boxes[0]
        cls_id = int(box.cls)
        class_name = model.names[cls_id]
        x1, y1, x2, y2 = box.xyxy[0]
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)
        pos_buffer.append((cx, cy))

        # 2) 움직임 거의 없음 → 1초 정지 감지
        if len(pos_buffer) == 10:
            dx = max(p[0] for p in pos_buffer) - min(p[0] for p in pos_buffer)
            dy = max(p[1] for p in pos_buffer) - min(p[1] for p in pos_buffer)
            if dx < 5 and dy < 5:
                if not ready_to_pick:
                    last_detection_time = time.time()
                    ready_to_pick = True
            else:
                ready_to_pick = False

        # 3) 1초 이상 정지 → 픽앤플레이스 시작
        if ready_to_pick and (time.time() - last_detection_time) >= 1.0:
            robot_coords = pixel_to_robot(cx, cy)
            place_coords = tower_positions[class_name]

            # 픽앤플레이스 실행
            print(f"[INFO] {class_name} 블록 픽앤플레이스 시작")

            # 1. 픽
            mc.send_coords([*robot_coords[0:3], 0, 0, 90], 50, 0)
            time.sleep(1)
            mc.set_gripper_state(1, 50)
            time.sleep(1)
            mc.send_coords([robot_coords[0], robot_coords[1], z_safe, 0, 0, 90], 50, 0)
            time.sleep(1)

            # 2. 플레이스
            z_place = place_coords[2]
            mc.send_coords([place_coords[0], place_coords[1], z_safe, 0, 0, 90], 50, 0)
            time.sleep(1)
            mc.send_coords([place_coords[0], place_coords[1], z_place, 0, 0, 90], 50, 0)
            time.sleep(1)
            mc.set_gripper_state(0, 50)
            time.sleep(1)
            mc.send_coords([place_coords[0], place_coords[1], z_safe, 0, 0, 90], 50, 0)

            # 초기화
            pos_buffer.clear()
            ready_to_pick = False
            print("[INFO] 완료. 다음 블록 대기 중...")

    else:
        pos_buffer.clear()
        ready_to_pick = False

    time.sleep(0.05)
