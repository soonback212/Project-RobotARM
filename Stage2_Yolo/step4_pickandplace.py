import cv2
import time
from ultralytics import YOLO
from pymycobot.mycobot import MyCobot

class MyArm:
    def __init__(self, port="COM5", baurd=115200):
        self.port = port
        self.baurd = baurd

    def connect(self):
        return MyCobot(self.port, self.baurd)

    def pick(self, mc, model):
        # 스캔 위치로 이동
        mc.set_gripper_value(40, 40)
        time.sleep(2)
        mc.send_angles([95.8, 33.48, -44.47, -47.72, 84.11, 0.35], 30)
        time.sleep(2)

        # 카메라 ON + 감지
        cap = cv2.VideoCapture(0)
        start_time = time.time()
        label_count = {}
        result_label = None

        while time.time() - start_time < 5:
            ret, frame = cap.read()
            if not ret:
                continue

            results = model(frame)
            boxes = results[0].boxes
            names = results[0].names
            
            annotated_frame = results[0].plot()
            cv2.imshow("Object Detection", annotated_frame)
            cv2.waitKey(1)
            
            for box in boxes:
                cls = int(box.cls)
                label = names[cls]
                if label in ["Red", "Orange", "Yellow", "Green"]:
                    label_count[label] = label_count.get(label, 0) + 1

            time.sleep(0.1)

        cap.release()
        cv2.destroyAllWindows()

        # 1초 이상(10회 이상) 감지된 라벨만 인정
        for label, count in label_count.items():
            if count >= 2:
                result_label = label
                break

        if result_label:
            print(f"[PICK] Detected object: {result_label}")

            # 집기 동작
            mc.send_angles([89.64, 3.42, -70.57, -23.63, 89.82, 3.42], 30)
            time.sleep(2)
            mc.set_gripper_value(13, 40)
            time.sleep(2)
            mc.send_angles([95.8, 33.48, -44.47, -47.72, 84.11, 0.35], 30)
            time.sleep(2)
            mc.send_angles([60.55, 6.24, -27.5, -31.11, 26.36, 0.17], 30)
            time.sleep(2)

        return result_label

    def red_one(self, mc):
        mc.send_angles([1.4, -42.89, 10.45, -39.11, 90.08, -0.08], 30)
        time.sleep(2)
        mc.set_gripper_value(60, 40)
        time.sleep(2)
        mc.send_angles([1.58, -35.85, -7.73, 6.5, 91.05, -4.04], 30)
        time.sleep(2)

    def orange_one(self, mc):
        mc.send_angles([0.96, -16.52, -30.76, -33.75, 90, 2.1], 30)
        time.sleep(2)
        mc.set_gripper_value(60, 40)
        time.sleep(2)
        mc.send_angles([6.76, -6.15, -35.06, -19.42, 85.86, 10.19], 30)
        time.sleep(2)

    def yellow_one(self, mc):
        mc.send_angles([2.9, 24.87, -73.91, -27.5, 90.43, 1.14], 30)
        time.sleep(2)
        mc.set_gripper_value(40, 40)
        time.sleep(2)
        mc.send_angles([8.61, 43.68, -80.41, -12.39, 83.23, 5.09], 30)
        time.sleep(2)

    def green(self, mc):
        mc.send_angles([40.25, -24.69, -59.76, -3.16, 92.98, 5.62], 30)
        time.sleep(2)
        mc.set_gripper_value(60, 40)
        time.sleep(2)
        mc.send_angles([40.86, -3.33, -27.68, -37.44, 90.61, -4.04], 30)
        time.sleep(2)

def main():
    myArm = MyArm("COM5", 115200)
    mc = myArm.connect()
    mc.set_gripper_mode(0)

    model = YOLO("runs/no_aug_final/weights/best.pt")

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("Returning to origin (0,0,0,0,0,0)")
            mc.send_angles([0, 0, 0, 0, 0, 0], 30)
            break
        
        label = myArm.pick(mc, model)

        if label == "Red":
            myArm.red_one(mc)
        elif label == "Orange":
            myArm.orange_one(mc)
        elif label == "Yellow":
            myArm.yellow_one(mc)
        elif label == "Green":
            myArm.green(mc)
        else:
            print("No valid object detected.")

        # 감지 여부와 관계없이 스캔 위치로 복귀
        mc.send_angles([95.8, 33.48, -44.47, -47.72, 84.11, 0.35], 30)
        time.sleep(2)

if __name__ == '__main__':
    main()
