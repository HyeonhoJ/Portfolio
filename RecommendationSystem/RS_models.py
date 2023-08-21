
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Dataset, Reader, prediction_algorithms


# popularity score keyword
def keywords_processing(keywords):
    # keywords예시
        # USER_KEYWORD = {
        #     'tags':['잡티', '각질', '트러블'],
        #     'skin_tone':'중성',
        #     'score_weight':'발색력'
        # }
    new_row = {
        'product_idx':-1,
        'tag1':0,
        'tag2':0,
        'tag3':0,
        'tag4':0,
        'tag5':0,
        'tag6':0,
        'tag7':0,
        'tag8':0,
        'tag9':0,
        'skin_type1':0,
        'skin_type2':0,
        'skin_type3':0,
        'skin_type4':0,
        'skin_type5':0,
    }

    for tag in keywords['tags']:
        if tag ==  '잡티':
            new_row['tag1']=1
        elif tag ==  '각질':
            new_row['tag2']=1
        elif tag == '트러블':
            new_row['tag3']=1
        elif tag == '민감성':
            new_row['tag4']=1
        elif tag == '모공':
            new_row['tag5']=1
        elif tag == '홍조':
            new_row['tag6']=1
        elif tag == '아토피':
            new_row['tag7']=1
        elif tag == '주름':
            new_row['tag8']=1
        elif tag == '피지과다':
            new_row['tag9']=1

    if keywords['skin_type'] == '지성':
        new_row['skin_type1']=1
    elif keywords['skin_type'] == '건성':
        new_row['skin_type2']=1
    elif keywords['skin_type'] == '복합성':
        new_row['skin_type3']=1
    elif keywords['skin_type'] == '약건성':
        new_row['skin_type4']=1
    elif keywords['skin_type'] == '중성':
        new_row['skin_type5']=1

    if keywords['importance'] == '발색력':
        selected_detail_score = 'detail_score1'
    elif keywords['importance'] == '지속력':
        selected_detail_score = 'detail_score2'
    elif keywords['importance'] == '발림성':
        selected_detail_score = 'detail_score3'

    return new_row, selected_detail_score


# popularity score 
def weighted_score(df, selected_detail_score, w=0.5):
    return w * df['color_score'] + (1 - w) * (df[selected_detail_score] + df['detail_score1'] + df['detail_score2'] + df['detail_score3'] - df['weight']) / (3 - df['weight'])



def recommend(reco_rank, reco_size = 3):

    final_lips = list(reco_rank[reco_rank.product_type == '립'][:reco_size]['product_idx'])
    final_shadows = list(reco_rank[reco_rank.product_type == '섀도우'][:reco_size]['product_idx'])
    final_cheeks = list(reco_rank[reco_rank.product_type == '블러셔'][:reco_size]['product_idx'])

    # 추천 결과
    items_product_idx ={
        '립':final_lips,
        '섀도우':final_shadows,
        '블러셔':final_cheeks
    }
    
    return items_product_idx

def get_reco_prd_info(product_data, items_product_idx):
    
    item_info = {
        '립': '',
        '섀도우':'',
        '블러셔':''
    }

    
    for prd_type in items_product_idx:
        type_item_info = {
            "mainImg": [],
            "colorImg": [],
            "itemUrl": [],
            "brand": [],
            "itemName": [],
            "color": [],
            "price": []
        }

        for prd in items_product_idx[prd_type]:
            prd_info = product_data[product_data['product_idx']==prd]
            type_item_info['mainImg'].append(prd_info['product_img'].values[0])
            type_item_info['colorImg'].append(prd_info['color_img'].values[0])
            type_item_info['itemUrl'].append(prd_info['product_link'].values[0])
            type_item_info['brand'].append(prd_info['brand'].values[0])
            type_item_info['itemName'].append(prd_info['product_name'].values[0])
            type_item_info['color'].append(prd_info['color_name'].values[0])
            type_item_info['price'].append(prd_info['price'].values[0])
            
        item_info[prd_type] = type_item_info
    
    return type_item_info

def popularity_based(recommend_data, score_data, keywords, SKIN_TONE):                       #product_score_data

    ######################db로 대체########################
    # recommend_data = pd.read_csv("data/contents_based_all.csv")
    # recommend_data.rename(columns = {'index':'product_idx', 'type':'product_type'}, inplace=True)
    # product_score_data = pd.read_csv("data/score_data.csv")
    # product_score_data.rename(columns={'detail_socre1':'detail_score1','index':'product_idx','type':'product_type'}, inplace=True)
    ########################################################

    new_row, selected_detail_score =  keywords_processing(keywords)

    RS_pop = recommend_data[recommend_data['skin_tone'].str.contains(SKIN_TONE)]
    RS_pop = RS_pop[['product_idx','tag1','tag2','tag3','tag4','tag5','tag6','tag7','tag8','tag9', 'skin_type1','skin_type2','skin_type3','skin_type4','skin_type5', 'product_type','skin_tone']]

    RS_pop_matrix = RS_pop.iloc[:, :-2]
    new_row = pd.DataFrame(new_row, index=[RS_pop_matrix.index[-1]+1])
    RS_pop_matrix = pd.concat([RS_pop_matrix, new_row])

    idx = RS_pop['product_idx'].copy()
    matrix = RS_pop.iloc[:,1:-2].copy()

    sim_data = cosine_similarity(matrix, matrix)
    sim = sim_data[-1]
    sim_rank = pd.DataFrame({'product_idx':idx,'sim':sim}).sort_values(by='sim', ascending =False)
    sim_rank = sim_rank.merge(RS_pop[['product_idx', 'product_type','skin_tone']], how='left', on='product_idx')[1:]

    # 유사 상품 10개
    score_data = score_data[['product_idx','color_score','detail_score1','detail_score2','detail_score3', 'weight']]
    score_data['weighted_score']  = weighted_score(score_data, selected_detail_score, w=0.5)
    score_data = score_data[['product_idx','weighted_score']]

    # 정렬된 유사 상품
    reco_rank = sim_rank.merge(score_data, how='left', on = 'product_idx')    
    
    return recommend(reco_rank, 3)


def contents_based(recommend_data, purchase_data, USER_ID, SKIN_TONE):
    ######################### db로 대체 #########################
    # recommend_data = pd.read_csv("data/contents_based_all.csv")
    # recommend_data.rename(columns = {'index':'product_idx', 'type':'product_type'}, inplace=True)
    #############################################################

    user_purchase_df = purchase_data[purchase_data.user_idx==USER_ID]
    RS_con = recommend_data[recommend_data['skin_tone'].str.contains(SKIN_TONE)]
    user_best_product = user_purchase_df.sort_values(by = 'processed_score', ascending = False).product_idx.values[0]

    idx = RS_con['product_idx']
    matrix = RS_con.drop(columns = ['product_idx','skin_tone','product_type'])
    sim_data = cosine_similarity(matrix, matrix)
    sim = sim_data[user_best_product]
    sim_rank = pd.DataFrame({'product_idx':idx,'sim':sim}).sort_values(by='sim', ascending =False)
    user_purchase_list = user_purchase_df.product_idx

    for purchase in user_purchase_list:
        if purchase in sim_rank['product_idx']:
            sim_rank = sim_rank[sim_rank['product_idx']!=purchase]

    reco_rank = sim_rank.merge(RS_con[['product_idx', 'product_type','skin_tone']], how='left', on='product_idx')[1:]

    return recommend(reco_rank, 3)


def collaborative(product_score_data, purchase_data, USER_ID, SKIN_TONE):
    purchase_data = purchase_data[['user_idx','product_idx','processed_score']]
    purchase_data.dropna(inplace=True)
    purchase_data = purchase_data.drop_duplicates(subset=['reviewers','index'])
    purchase_data['processed_score'] = purchase_data['processed_score'] * (5/3.5)

    reader = Reader(rating_scale=(0.7, 5))
    data = Dataset.load_from_df(purchase_data[['user_idx','product_idx','processed_score']],
                                reader=reader)
    model = prediction_algorithms.baseline_only.BaselineOnly()
    trainset = data.build_full_trainset()
    model.fit(trainset)
    # 사용자가 구매한 상품 목록 list
    user_purchase = purchase_data[purchase_data['user_idx']==USER_ID]['index'].tolist()
    # 전체 상품 목록 list
    total_prd = purchase_data['product_idx'].unique().tolist()

    # 사용자가 구매하지 않은 상품 목록 list
    user_not_purchase = [prd for prd in total_prd if prd not in user_purchase]

    # 구매하지 않은 상품에 대한 평가 예측 list
    predictions = [model.predict(USER_ID, prd) for prd in user_not_purchase]

    # 평가 데이터 정렬
    def sortkey_est(pred):
            return pred.est
    predictions.sort(key=sortkey_est, reverse=True)


    target_user_rating = [pred.iid for pred in predictions]
    target_user_rating = pd.DataFrame({'product_idx':target_user_rating})        

    reco_rank = target_user_rating.merge(product_score_data[['skin_tone', 'product_type', 'product_idx']], how='left', on='product_idx')
    reco_rank = reco_rank.dropna(subset='product_type')

    reco_rank = reco_rank[reco_rank['skin_tone'].str.contains(SKIN_TONE)]

    return recommend(reco_rank, 3)