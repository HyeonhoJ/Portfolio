import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import random


class ContentBasedRecommendation:
    def __init__(self, csv_path):
        # 데이터 읽어오기
        self.df = pd.read_csv(csv_path)
        # 1. df를 객체로 저장(pickle이라는 라이브러리 사용)
        # 2. DB에 저장

        # 필요한 데이터프레임 형성 (1. product_id_name, 2. product_df, 3. product_feature_df, 4. all_features)
        self.product_id_name = self.df[['product_id', 'product_name']]
        self.product_id_name.drop_duplicates(inplace=True)
        
        self.product_df = self.df[['product_id', 'product_name', 'reviewers', '발색력', '지속력', '발림성', '수분감']]
        
        self.product_feature_df = self.product_df.groupby('product_id')[['발색력', '지속력', '발림성', '수분감']].mean()
        
        self.all_features = self.product_feature_df.merge(self.product_id_name, on='product_id', how='left')

        # 코사인 유사도 (수치형 자료라서 원핫인코딩 실시하지 않음)... 그냥 범주형으로 내버려두고 원핫인코딩 할까? 
        self.item_cos_matrix = cosine_similarity(self.product_feature_df)

    def nickname_to_df(self, user_nickname):
        # user_nickname = input("please insert your oliveyoung nickname")
        user_sort_df = self.product_df.loc[self.product_df['reviewers'] == user_nickname]
        result = user_sort_df.groupby('product_id')[['발색력', '지속력', '발림성', '수분감']].mean()
        return result 

    def top_favorites_from_df(self,input_df):
        input_df['sum'] = input_df['발색력'] + input_df['지속력'] + input_df['발림성'] + input_df['수분감'] # 피쳐의 합계 구하기 
        input_df = input_df.sort_values(by='sum', ascending=False) # 줄세우기
        print('input_df.index',input_df.index)
        # if input_df.index is None:
        #     return 0
        input_df.index[0]  # -> 'A000000158991'
        important_num = list(self.product_feature_df.index).index(input_df.index[0]) # product_feature_df의 index에서 'A000000158991'는 몇번째야? 
        return important_num

    def make_recommendation(self, user_nickname):
        user_df = self.nickname_to_df(user_nickname)
        target_item_id = self.top_favorites_from_df(user_df)  # 어떤 제품이랑 비슷한거 뽑을까? (이 값을 입력받아야 함)
        top_k = 3 # 몇 개 추천해줄까?

        # 아이템 유사성 보고 탑3개 고르기
        top_items = self.item_cos_matrix[target_item_id, :].argsort()[-top_k:][::-1]
        similar_items = [self.product_feature_df.index[e] for e in top_items]

        # 해당 ID에 해당하는 제품명 뽑기
        result_list = []
        for i in similar_items:
            product = self.product_id_name.loc[self.product_id_name['product_id']==i]['product_name'].iloc[0]
            result_list.append(product)
        return print(f'당신에게 어울리는 화장품은 \n첫번째: {result_list[0]},\n두번째: {result_list[1]},\n세번째: {result_list[2]}')

# # Create an instance of the RecommendationSystem class

# csv_filepath = "C:/project/face_color_detection/TellMeYourColor/data/crwaling_result/review_product_data_example.csv"
# rec_system = ContentBasedRecommendation(csv_filepath)
# # Call the make_recommendation() method to get the recommendations
# rec_system.make_recommendation()