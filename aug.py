## 명령어 : 파이썬 경로 파일 경로\aug.py -i 이미지경로 -o 저장될경로

from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
from imutils import paths
import argparse
import numpy as np
import os

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True)
ap.add_argument("-o", "--output", required=True)
ap.add_argument("-p", "--prefix", type=str, default="image")
args = vars(ap.parse_args())

# image: input 이미지 경로
# output: data augmentation의 결과가 저장될 이미지경로
# prefix: image filename의 prefix

print("[INFO] loading example image...")
image = load_img(args["image"])
image = img_to_array(image)
image = np.expand_dims(image, axis=0)  # 맨 앞 1차원 추가

# 목표는 입력 이미지를 약간 수정하여 클래스 레이블 자체를 변경하지 않고 새 학습 샘플을 생성하는 것이므로 이러한 유형의 데이터 증가를 적용 할 때 주의해야 합니다.
# ImageDataGenerator가 초기화되면 실제로 새로운 학습 예제를 생성 할 수 있습니다.
aug = ImageDataGenerator(
    rotation_range=30,      # 회전의 각도 범위 제어, 무작위로 ± 30도 회전
    width_shift_range=0.3,  # 수평 및 수직 이동 변수, 이 경우 30% 
    height_shift_range=0.3,  
    shear_range=0.2,        # 이미지를 기울일 수 있는 라디안으로 시계 반대 방향의 각도 제어
    zoom_range=0.2,         # [1-zoom_range, 1 + zoom_range] 값의 균일 한 분포에 따라 이미지를 "확대" 또는 "축소"할 수 있는 포인트 값
    horizontal_flip=True,   # 수평으로 전환될 여부를 체크 
    fill_mode="nearest",    
)

# 증강 이미지를 구성하는 데 사용되는 Python 생성기를 초기화합니다. 출력 이미지 파일 경로, 각 파일 경로의 접두사 및 이미지 파일 형식을 지정하기 위한
# 몇 가지 추가 매개 변수와 함께 입력 이미지 인 batch_size 1을 전달합니다 (하나의 이미지 만 증가 시키므로).
print("[INFO] generating images...")
imageGen = aug.flow(
    image,
    batch_size=1,
    save_to_dir=args["output"],
    save_prefix=args["prefix"],
    save_format="bmp",
)

total = 0
# 그런 다음 imageGen 생성기의 각 이미지를 반복하기 시작합니다. 내부적으로 imageGen은 루프를 통해 요청 될 때마다 새로운 학습 샘플을 자동으로 생성합니다.
# 그런 다음 디스크에 기록 된 총 데이터 증가 예제 수를 늘리고 예제 10 개에 도달하면 스크립트 실행을 중지합니다.
for image in imageGen:
    total += 1

    if total == 4: # 변환된 이미지의 갯수 지정 
        break
