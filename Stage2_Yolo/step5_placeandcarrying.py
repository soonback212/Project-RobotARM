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

    def pick(self, mc, model, cap):
        # 스캔 위치로 이동
        mc.set_gripper_value(40, 40)
        time.sleep(2)
        mc.send_angles([95.8, 33.48, -44.47, -47.72, 84.11, 0.35], 30)
        time.sleep(2)

        # 인식 시작
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
            
            
            for box in boxes:
                cls = int(box.cls)
                label = names[cls]
                if label in ["Red", "Orange", "Yellow", "Green"]:
                    label_count[label] = label_count.get(label, 0) + 1

            time.sleep(0.1)

        for label, count in label_count.items():
            if count >= 1:
                result_label = label
                break

        if result_label:
            print(f"[PICK] Detected object: {result_label}")
            mc.send_angles([89.64, 3.42, -70.57, -23.63, 89.82, 3.42], 30)
            time.sleep(2)
            mc.set_gripper_value(13, 40)
            time.sleep(2)
            mc.send_angles([95.8, 33.48, -44.47, -47.72, 84.11, 0.35], 30)
            time.sleep(2)
            mc.send_angles([60.55, 6.24, -27.5, -31.11, 26.36, 0.17], 30)
            time.sleep(2)

        return result_label
        
    def angleReset(self, mc):
        mc.send_angles([0, 0, 0, 0, 0, 0], 20)
        time.sleep(2)
        
    def red_one(self, mc):
        self.angleReset(mc)
        mc.send_angles([-3.69, -32.16, -18, -19.33, 97.91, 5.44], 40)
        time.sleep(2)
        mc.set_gripper_value(60, 40)
        time.sleep(2)
        mc.send_angles([1.58, -35.85, -7.73, 6.5, 91.05, -4.04], 40)
        time.sleep(2)

    def red_two(self, mc):
        self.angleReset(mc)
        mc.send_angles([1.4, -38, 7.5, -35.4, 90.08, -0.08], 40)
        time.sleep(2)
        mc.set_gripper_value(60, 40)
        time.sleep(2)
        mc.send_angles([1.58, -34, -7.73, 6.5, 91.05, -4.04], 40)
        
    def red_three(self, mc):
        self.angleReset(mc)
        mc.send_angles([1.4, -37, 17, -40, 90.08, -0.08], 40)
        time.sleep(2)
        mc.set_gripper_value(60, 40)
        time.sleep(2)
        mc.send_angles([1.58, -35.85, -7.73, 6.5, 91.05, -4.04], 40)
        time.sleep(2)
        
    def orange_one(self, mc):
        self.angleReset(mc)
        mc.send_angles([0.96, -16.52, -30.76, -33.75, 90, 2.1], 40)
        time.sleep(2)
        mc.set_gripper_value(60, 40)
        time.sleep(2)
        mc.send_angles([6.76, -6.15, -35.06, -19.42, 85.86, 10.19], 40)
        time.sleep(2)

    def orange_two(self, mc): 
        self.angleReset(mc)
        mc.send_angles([0.96, -11, -28, -35, 90, 2.1], 40)
        time.sleep(2)
        mc.set_gripper_value(60, 40)
        time.sleep(2)
        mc.send_angles([6.76, -6.15, -35.06, -19.42, 85.86, 10.19], 40)
        time.sleep(2)
        
    def orange_three(self, mc): 
        self.angleReset(mc)
        mc.send_angles([0.96, -10, -16, -41.25, 89, 2.1], 40)
        time.sleep(2)
        mc.set_gripper_value(60, 40)
        time.sleep(2)
        mc.send_angles([6.76, -15, -15, -19.42, 85.86, 10.19], 40)
        time.sleep(2)

    def yellow_one(self, mc):
        self.angleReset(mc)
        time.sleep(2)
        mc.send_angles([2.9, 24.87, -72, -27.5, 90.43, 1.14], 40)
        time.sleep(2)
        mc.set_gripper_value(40, 40)
        time.sleep(2)
        mc.send_angles([8.61, 43.68, -80.41, -12.39, 83.23, 5.09], 40)
        time.sleep(2)

    def yellow_two(self, mc): 
        self.angleReset(mc)
        mc.send_angles([-1.05, 14.5, -52, -37, 93.07, 0.52], 40)
        time.sleep(2)
        mc.set_gripper_value(40, 40)
        time.sleep(2)
        mc.send_angles([4.92, 30.41, -62.05, -12.39, 85.34, 5.18], 40)
        time.sleep(2)
        
    def yellow_three(self, mc):
        self.angleReset(mc)
        mc.send_angles([8.61, 20, -47, -41.9, 85.34, 1.14], 40)
        time.sleep(2)
        # mc.send_angles([4.92, 33.41, -65.05, -32.20, 89.34, 5.18], 40)
        # time.sleep(2)
        mc.set_gripper_value(40, 40)
        time.sleep(2)
        mc.send_angles([4.92, 30.41, -54.05, -20.39, 85.34, 5.18], 40)
        time.sleep(2)

    def green_one(self, mc):
        self.angleReset(mc)
        mc.send_angles([-41.22, -37.08, -24.78, -19.68, 93.51, 4.3], 40)
        time.sleep(2)
        mc.set_gripper_value(60, 40)
        time.sleep(2)
        mc.send_angles([-41.22, -27, -24.78, -19.68, 93.51, 4.3], 40)
        time.sleep(2)
        self.angleReset(mc)
        time.sleep(2)

    def green_two(self, mc):
        self.angleReset(mc) 
        mc.send_angles([-41.22, -37.08, -24.78, -19.68, 93.51, 4.3], 40)
        time.sleep(2)
        mc.set_gripper_value(60, 40)
        time.sleep(2)
        mc.send_angles([-41.22, -27, -24.78, -19.68, 93.51, 4.3], 40)
        time.sleep(2)
        self.angleReset(mc)
        time.sleep(2)
        
    def green_three(self, mc):
        self.angleReset(mc) 
        mc.send_angles([-41.22, -37.08, -24.78, -19.68, 93.51, 4.3], 40)
        time.sleep(2)
        mc.set_gripper_value(60, 40)
        time.sleep(2)
        mc.send_angles([-41.22, -27, -24.78, -19.68, 93.51, 4.3], 40)
        time.sleep(2)
        self.angleReset(mc)
        time.sleep(2)

def main():
    myArm = MyArm("COM5", 115200)
    mc = myArm.connect()
    mc.set_gripper_mode(0)

    model = YOLO("runs/no_aug_final/weights/best.pt")

    color_count = {
        "Red": 0,
        "Orange": 0,
        "Yellow": 0,
        "Green": 0
    }

    # 카메라 초기화 & warm-up
    cap = cv2.VideoCapture(0)
    time.sleep(1.5)
    for _ in range(10): cap.read()

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("Returning to origin (0,0,0,0,0,0)")
            mc.send_angles([0, 0, 0, 0, 0, 0], 30)
            break

        label = myArm.pick(mc, model, cap)

        if label in color_count:
            color_count[label] += 1
            count = color_count[label]

            if label == "Red":
                if count == 1:
                    myArm.red_one(mc)
                elif count == 2:
                    myArm.red_two(mc)
                elif count == 3:
                    myArm.red_three(mc)

            elif label == "Orange":
                if count == 1:
                    myArm.orange_one(mc)
                elif count == 2:
                    myArm.orange_two(mc)
                elif count == 3:
                    myArm.orange_three(mc)

            elif label == "Yellow":
                if count == 1:
                    myArm.yellow_one(mc)
                elif count == 2:
                    myArm.yellow_two(mc)
                elif count == 3:
                    myArm.yellow_three(mc)

            elif label == "Green":
                if count == 1:
                    myArm.green_one(mc)
                elif count == 2:
                    myArm.green_two(mc)
                elif count == 3:
                    myArm.green_three(mc)
        else:
            print("No valid object detected.")

        mc.send_angles([95.8, 33.48, -44.47, -47.72, 84.11, 0.35], 30)
        time.sleep(2)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()