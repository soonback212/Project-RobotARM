import cv2
from ultralytics import YOLO


model = YOLO("runs/no_aug_final/weights/best.pt")  # 학습된 모델 불러오기
cap = cv2.VideoCapture(0)  # 웹캠 활성화

while True:
    ret, frame = cap.read()
    results = model(frame)  # 모델 예측
    annotated_frame = results[0].plot()  # 예측 결과 그리기
    cv2.imshow("webcam", annotated_frame)  # 창에 표시
    print(annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q'를 누르면 종료
        break

cap.release()
cv2.destroyAllWindows()