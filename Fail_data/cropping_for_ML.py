import os
import cv2
import dlib
import numpy as np
import pandas as pd
from tqdm import tqdm

class FaceEyeCropping:
    def __init__(self):
        datFile = 'C:/Users/jungh/final_project/landmarks/shape_predictor_68_face_landmarks.dat'
        self.predictor = dlib.shape_predictor(datFile)
        self.detector = dlib.get_frontal_face_detector()
        self.color_f = (0, 0, 255) # 얼굴은 빨강
        self.color_l_out = (255, 0, 0) # 랜드마크 바깥쪽 - 파랑
        self.color_l_in = (0, 255, 0) # 랜드마크 안쪽 - 초록
        self.line_width = 2
        self.circle_r = 1
        self.fontSize = 2
        
        #왼쪽 눈 영역
        self.left_eye_region = [37, 38, 41]
        
        # 데이터 프레임을 위한 빈 리스트 만들기
        self.face_crop_list = []
        self.face_color_bgr_list = []
        self.face_color_lab_list = []
        self.eye_color_hsv_list = []
        self.eye_color_bgr_list = []
        self.label = []

    def face_eye_detecter(self, file_path):
        try:
            img = cv2.imread(file_path)
            dets = self.detector(img, 1)

            # 인식된 얼굴 개수만큼 반복하여 얼굴 윤곽 표시
            # k: 얼굴의 인덱스., d: 얼굴의 좌표
            for k, d in enumerate(dets):
                shape = self.predictor(img, d)
                print(type(shape))  # 테스트용 확인후 바로 지움
                eye_landmarks = shape.part(self.left_eye_region[0:self.left_eye_region[2]+1])
                eye_points = [(landmark.x, landmark.y) for landmark in eye_landmarks]
                cv2.polylines(img, [np.array(eye_points)], isClosed=True, color=self.color_f, thickness=self.line_width)
                eye_crop = img[min([point[1] for point in eye_points]):max([point[1] for point in eye_points]), min([point[0] for point in eye_points]):max([point[0] for point in eye_points])]

                # 얼굴에 사각형 그림
                cv2.rectangle(img, (d.left(), d.top()), (d.right(), d.bottom()), self.color_f, self.line_width)
                face_crop = img[d.top():d.bottom(), d.left():d.right()]

            return face_crop, eye_crop
        except Exception as e:
            print("Error in face_eye_detecter:", str(e))

    def face_color_extract_convert(self, face_crop):
        face_color_bgr = np.median(face_crop, axis=(0, 1)).round().astype(np.uint8)
        face_color_lab = cv2.cvtColor(face_color_bgr.reshape(1, 1, 3), cv2.COLOR_BGR2LAB).squeeze()
        return face_color_bgr, face_color_lab

    def eye_color_extract_convert(self, eye_crop):
        eye_color_bgr = np.median(eye_crop, axis=(0, 1)).round().astype(np.uint8)
        eye_color_hsv = cv2.cvtColor(eye_color_bgr.reshape(1, 1, 3), cv2.COLOR_BGR2HSV).squeeze()
        return eye_color_bgr, eye_color_hsv

    def collect_data(self, folder_path):
        for warm_cool in ['warm', 'cool']:
            for celebrities in tqdm(os.listdir(os.path.join(folder_path, warm_cool))):
                for file_name in os.listdir(os.path.join(folder_path, warm_cool, celebrities)):
                    file_path = os.path.join(folder_path, warm_cool, celebrities, file_name)

                    result = self.face_eye_detecter(file_path)
                    if result is not None:
                        face_crop, eye_crop = result
                        face_color_bgr, face_color_lab = self.face_color_extract_convert(face_crop)
                        eye_color_bgr, eye_color_hsv = self.eye_color_extract_convert(eye_crop)

                        self.face_crop_list.append(face_crop)
                        self.face_color_bgr_list.append(face_color_bgr)
                        self.face_color_lab_list.append(face_color_lab)
                        self.eye_color_bgr_list.append(eye_color_bgr)
                        self.eye_color_hsv_list.append(eye_color_hsv)

                        if celebrities.startswith("spring"):
                            self.label.append("spring")
                        elif celebrities.startswith("summer"):
                            self.label.append("summer")
                        elif celebrities.startswith("fall"):
                            self.label.append("fall")
                        else:
                            self.label.append("winter")

    def create_dataframe(self):
        data = {
            'face_crop': self.face_crop_list,
            'face_color_bgr': self.face_color_bgr_list,
            'face_color_lab': self.face_color_lab_list,
            'eye_color_bgr': self.eye_color_bgr_list,
            'eye_color_hsv': self.eye_color_hsv_list,
            'label': self.label
        }
        df = pd.DataFrame(data)
        return df