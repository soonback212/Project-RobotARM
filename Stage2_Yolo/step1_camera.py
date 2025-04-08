import os
import cv2
import glob

def capture_image():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("카메라 연결 실패")
        return

    save_directory = "img_capture"
    os.makedirs(save_directory, exist_ok=True)

    class_labels = ["red", "orange", "yellow", "green"]
    current_label = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("프레임 읽기 실패")
            break

        # 현재 라벨 화면에 표시
        cv2.putText(frame, f"Label: {class_labels[current_label]}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Webcam", frame)
        key = cv2.waitKey(1)

        if key == ord('c'):
            label_dir = f"{save_directory}/{class_labels[current_label]}"
            os.makedirs(label_dir, exist_ok=True)
            existing_files = glob.glob(f"{label_dir}/*.jpg")
            image_count = len(existing_files)
            file_name = f"{label_dir}/img_{image_count}.jpg"
            cv2.imwrite(file_name, frame)
            print(f"Saved: {file_name}")

        elif key == ord('n'):
            current_label = (current_label + 1) % len(class_labels)
            print(f"Switched to: {class_labels[current_label]}")

        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


capture_image()
