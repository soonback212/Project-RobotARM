# MyCobot 블록 분류 프로젝트 (YOLOv8)

## 프로젝트 개요

발표: **MyCobot M5Stack-basic**

다른 화상의 나무 블록 (**Red, Orange, Yellow, Green**) 등장 결과를 YOLOv8을 통해 검색 효율을 판단하고, 검색 결과에 따라 MyCobot이 자동으로 작동하도록 구성한 프로젝트입니다.

---

## 데이터 수집

사용자가 OpenCV 을 이용하여 **컬렉션 당 60장 정도의 이미지 수집**을 진행.

| 컬렉스 | 이미지 수 |
|-------------|--------------|
| Red         | 60장         |
| Orange      | 60장         |
| Yellow      | 60장         |
| Green       | 60장         |

- OpenCV 와 카메라를 이용해 이미지 촬영
- `c` 키로 저장, `n` 키로 컬렉스 전환
- YOLOv8 형식의 레이벨 및 이미지 구조로 export

---

## 모델 학습 (YOLOv8)

- 모델: `YOLOv8n`
- 학습 횟수: 50에포트 / 100에포트
- 이미지 크기: 640x640
- 학습 명령:

```python
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
model.train(
    data="dataset/data.yaml",
    epochs=50,
    imgsz=640,
    project="runs",
    name="color_classifier"
)
```

---

## 시험 결과

### 지원이 없는 증가 (Epoch 50)

| 컬렉스 | mAP50 | mAP50-95 |
|-------------|--------|-----------|
| Red         | 0.995  | 0.667     |
| Orange      | 0.995  | 0.604     |
| Yellow      | 0.995  | 0.832     |
| Green       | 0.995  | 0.624     |

- 전체적으로 합격점이 너무 높음
- 60장의 적적인 화상수집으로도 최고 효과 담병

### 증가 적용 학습 (Epoch 100, hsv + flip + mixup)

- Red / Orange 값 규칙 필름 가장 크게 드러날 수 있음
- 기본 미규칙의 효과가 가장 훨씬 좋음

---

## 트러블슈팅 정보

| 문제 | 원인 / 해결 |
|--------|---------------------|
| `data.yaml` 컬렉스 순서 다른 문제 | YOLOv8은 컬렉스 단위 순서대로 자동 정렬… |
| HSV 증가 때 검색 두발 | 화상 그룹과 모드 중에 그룹가 검색 연속구 분류에 복합 문제 발생 |

---

## 효율적인 최종 구조

- 카메라 + YOLOv8 + 웹캠을 이용한 검색
- pymycobot 버전의 angles 관리 기준 자동 지정
- 최종으로 `.txt`로 값을 저장하고 자동으로 지정값 발사 가능

