# Yolov8 Block Classifier Project - README

## 프로젝트 개요
이 프로젝트는 **YOLOv8**을 이용하여 **4가지 블록 색상(Red, Orange, Yellow, Green)** 을 인식하고, **MyCobot 로봇 암**이 인식된 블록을 지정된 위치로 옮기는 자동화 시스템입니다.

## 전체 스테이지 구성
- **Stage 1: PLC 제어 시스템 구성** *(별도 프로젝트로 관리)*
  - 컨베이어 및 센서 등 외부 시스템 제어
  - PLC 연동 테스트 완료

- **Stage 2: YOLO 기반 블록 인식 및 로봇 제어**
  - 로봇 + 딥러닝 통합 자동화 제어 구현

---

## Stage2_YOLO 폴더 구조
```
STAGE2_YOLO/
├── dataset/                    # YOLO 학습 데이터셋 (이미지 및 라벨)
├── img_capture/               # 수집 이미지 저장용 폴더
├── runs/                      # YOLO 학습 결과 (weights, predict 등)
├── yolov8n.pt                 # 사전 학습된 YOLOv8n 가중치 (optional)
├── gripper_calibration.py     # 그리퍼 벌어짐 수치 보정 테스트
├── step1_camera.py            # 카메라 연결 및 테스트 확인
├── step2_deeplearning.py      # YOLOv8 객체 인식 단독 테스트
├── step3_block_position.py    # 블록 적재 위치 조정 및 각도 저장
├── step4_pickandplace.py      # 분류에 따른 픽앤 플레이스
├── step5_placeandcarrying.py  # 분류, 적재 동시에 수행
```

---

## 단계별 구성 파일 및 설명

### Step 1: `step1_camera.py` - 카메라 점검
- **목적**: OpenCV를 통해 카메라 연결 여부 및 영상 출력 상태 점검
- 카메라 캡처 → 실시간 화면 출력
- 디버깅 시 화면이 잘 나오는지 확인하는 초기 테스트용 코드

### Step 2: `step2_deeplearning.py` - 딥러닝 모델 테스트
- **목적**: 학습된 YOLOv8 모델을 불러와 실시간 객체 감지 수행
- 모델 로딩 + 프레임 단위 예측 → 예측 결과 시각화
- 블록의 감지가 실제로 잘 되는지 확인 가능

### Step 3: `step3_block_position.py` - 블록 적재 위치 조정
- **목적**: 블록을 적재할 위치를 수동으로 지정
- 눈대중으로 각 색상의 블록을 둘 위치를 조절하고,
- 해당 위치의 관절 각도를 `send_angles()`로 기록하여 픽 앤 플레이스용 각도 확보

### Step 4: `step4_pickandplace.py` - 분류 TEST
- **목적**: YOLO 인식 + 집기 + 지정 위치로 이동까지 단일 수행
- 한 개 블록 인식 시 → 그에 맞는 위치로 이동해 놓기
- `pick()` 함수 내에서 카메라 ON, 인식, 집기 수행
- 라벨에 따라 `red_one()`, `green()`, 등 위치 분기 함수 호출

### Step 5: `step5_placeandcarrying.py` - 분류, 적재 통합 TEST
- **목적**: 블록을 인식하고 색상에 따라 지정된 위치로 옮긴 후 반복
- 각 색상별로 1회, 2회, 3회차 위치로 옮기도록 카운터 방식 적용 예정
- `pick()`으로 인식 후 → 라벨에 따라 카운터 증가 → 해당 위치로 이동
- `q` 키 누르면 로봇 암이 `[0,0,0,0,0,0]`으로 안전하게 이동 후 종료

---

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

---

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

---

## 향후 개선 사항
- 물체 인식 정확도 추가 향상 (추가 수집 및 재학습)
- 블록 위치 보정 (depth estimation or multi-frame fusion)
- 그리퍼 속도 및 거리 조절 파라미터 튜닝
- 각 색상별 위치 3단계 운반 기능 완성 (step5 활용)

---

**참고 문서**
- [Ultralytics YOLO 공식 문서](https://docs.ultralytics.com/)
- [MyCobot SDK 문서](https://docs.elephantrobotics.com/)
