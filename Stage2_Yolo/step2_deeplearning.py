from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # 또는 yolov8s.pt로 해도 좋아!

model.train(
    data="dataset/data.yaml",
    epochs=100,
    imgsz=640,
    project="runs",
    name="no_aug_final"  # 이전 실험과 구분하기 좋음
)
