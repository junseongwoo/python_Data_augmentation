## 명령어 : 파이썬 경로 파일 경로\aug.py -i 이미지경로 -o 저장될경로

from keras_preprocessing.image import ImageDataGenerator
from keras_preprocessing.image import img_to_array
from keras_preprocessing.image import load_img
import numpy as np
import os

# image: input 이미지 경로
# output: data augmentation의 결과가 저장될 이미지경로
# prefix: image filename의 prefix

class GeneratorImage():
    def Generator_Image(img, count, savePath, saveFileName, rotation, width, height, shear, zoom, horizontal_flip = False):
        image = load_img(img)
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)

        aug = ImageDataGenerator(
            rotation_range=rotation,      # 회전의 각도 범위 제어, 무작위로 ± 30도 회전
            width_shift_range=width,      # 수평 및 수직 이동 변수, 이 경우 30% 
            height_shift_range=height,  
            shear_range=shear,       # 이미지를 기울일 수 있는 라디안으로 시계 반대 방향`의 각도 제어
            zoom_range=zoom,         # [1-zoom_range, 1 + zoom_range] 값의 균일 한 분포에 따라 이미지를 "확대" 또는 "축소"할 수 있는 포인트 값
            horizontal_flip=horizontal_flip,   # 수평으로 전환될 여부를 체크 
            fill_mode="nearest",
            )

        imageGen = aug.flow(
            img,
            batch_size=1,
            save_to_dir="/"+savePath,
            save_prefix=saveFileName,
            save_format="bmp",
            )

        total = 0
        # 그런 다음 imageGen 생성기의 각 이미지를 반복하기 시작합니다. 
        # 내부적으로 imageGen은 루프를 통해 요청 될 때마다 새로운 학습 샘플을 자동으로 생성합니다.
        # 그런 다음 디스크에 기록 된 총 데이터 증가 예제 수를 늘리고 
        # 예제 10 개에 도달하면 스크립트 실행을 중지합니다.
        for image in imageGen:
            total += 1

            if total == count: # 변환된 이미지의 갯수 지정 
                break