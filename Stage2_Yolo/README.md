# Yolov8 Block Classifier Project - README

## 프로젝트 개요
이 프로젝트는 **YOLOv8**을 이용하여 **4가지 블록 색상(Red, Orange, Yellow, Green)** 을 인식하고, **MyCobot 로봇 암**이 인식된 블록을 지정된 위치로 옮기는 자동화 시스템입니다.

## 주요 구성 요소
- **YOLOv8 모델 (Ultralytics)**: 색상 분류 학습
- **MyCobot (M5Stack-Basic)**: 픽 앤 플레이스 동작
- **OpenCV**: 카메라 캡처 및 객체 시각화
- **Python 3.11 + PyTorch (CPU)** 환경

## 학습 데이터 구성
- 총 이미지 수: 각 클래스별 **60장**씩 수집
- 총 240장 (Red, Orange, Yellow, Green)
- Label Format: Pascal VOC
- 주석 도구: Roboflow 이용

## 학습 결과 (YOLOv8 v8.3.78 / CPU Inference 기준)
```
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95)
                   all         12         11      0.895          1      0.953      0.817
                 Green          2          2      0.647          1      0.828      0.663
                Orange          3          3      0.988          1      0.995      0.895
                   Red          3          3      0.971          1      0.995      0.854
                Yellow          3          3      0.976          1      0.995      0.854
```

## 단계별 구성 파일 및 설명

### Step 1: `step1_camera.py`
- **목적**: OpenCV를 통해 카메라 연결 여부 및 영상 출력 상태 점검
- 카메라 캡처 → 실시간 화면 출력
- 디버깅 시 화면이 잘 나오는지 확인하는 초기 테스트용 코드

### Step 2: `step2_deeplearning.py`
- **목적**: 학습된 YOLOv8 모델을 불러와 실시간 객체 감지 수행
- 모델 로딩 + 프레임 단위 예측 → 예측 결과 시각화
- 블록의 감지가 실제로 잘 되는지 확인 가능

### Step 3: `step3_block_position.py`
- **목적**: 블록을 적재할 위치를 수동으로 지정
- 눈대중으로 각 색상의 블록을 둘 위치를 조절하고,
- 해당 위치의 관절 각도를 `send_angles()`로 기록

### Step 4: `step4_pickandplace.py`
- **목적**: 전체 로직 통합 실행
- 로봇이 스캔 위치로 이동 → 카메라 ON → YOLO 객체 인식 수행
- 감지된 라벨에 따라 블록을 집고 해당 색상에 맞는 위치로 옮김
- 감지 후 다시 스캔 위치로 복귀하여 반복 수행
- **`q` 키 입력 시 [0,0,0,0,0,0] 위치로 이동 후 종료**

### 기타 파일
- `gripper_calibration.py`: 그리퍼가 지나치게 벌어지는 현상을 조절하기 위한 테스트 코드
- `yolov8n.pt`: 사전 학습된 YOLOv8n 모델 (백업용)
- `runs/no_aug_final/weights/best.pt`: 최종 학습 완료된 모델 가중치

## 최종 구조 흐름 요약
1. MyCobot이 **스캔 위치**로 이동
2. YOLOv8으로 **5초간 객체 감지**
3. 감지된 라벨이 일정 횟수 이상 반복되면 유효한 감지로 판단
4. 감지된 색상에 따라 해당 위치로 이동 후 블록 배치
5. 다시 스캔 위치로 복귀 → 루프 반복
6. `q` 입력 시 전체 동작 중단 및 초기 위치 복귀

## 트러블슈팅 기록
| 이슈 | 해결 방법 |
|------|-----------|
| 데이터 증강 시 Red/Orange 혼동 | 증강 제거 후 성능 개선 (no_aug_final 모델 사용) |
| 모델 정확도 하락 | 클래스 수 재정의 및 60장 균일 수집 |
| 그리퍼가 지나치게 벌어짐 | `set_gripper_value(40, 40)` 값 수동 조절 (13~60 사이 조정함) |
| 감지 안됨 | 라벨명 대소문자 불일치 → "Red" 대신 "red" → 정규화된 라벨 사용으로 해결 |
| 카메라 미표시 | `cv2.imshow()` + `cv2.waitKey(1)`로 실시간 표시 추가 |
| 객체 인식만 되고 동작 안함 | pick 함수에서 결과만 return하고, main에서 처리하지 않던 문제 → **main에서 분기 처리 추가**하여 해결 |
| q 키 입력으로 종료 안됨 | `cv2.waitKey()` 루프 외부에서도 키 입력 받아 종료 조건 처리 |

## 주요 코드 구조 요약
```python
label = myArm.pick(mc, model)

if label == "Red":
    myArm.red_one(mc)
...

if key == ord('q'):
    mc.send_angles([0,0,0,0,0,0], 30)
```

## 향후 개선 사항
- 물체 인식 정확도 추가 향상 (추가 수집 및 재학습)
- 블록 위치 보정 (depth estimation or multi-frame fusion)
- 그리퍼 속도 및 거리 조절 파라미터 튜닝

---
프로젝트 진행을 위해 [Ultralytics YOLO 공식 문서](https://docs.ultralytics.com/) 와 [MyCobot SDK 문서](https://docs.elephantrobotics.com/) 참고

