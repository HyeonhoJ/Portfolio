import csv
import os
from flask import Flask, request, render_template, session, redirect, url_for, send_from_directory
# from flask_restful import Api, Resource
from flask_cors import CORS
from flask import jsonify
from PIL import Image
from models.face.find_personal_color import SkinToneClassifier # 얼굴 모델
# from models.ContentsBased import ContentBasedRecommendation
from models.RS_models import  popularity_based, contents_based, collaborative, get_reco_prd_info
from database import Customer, Product, Product_score, Purchase, Recommend
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
import pandas as pd
import random
import string
import pymysql
import json

def generate_secret_key(length=32):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

app = Flask(__name__)
app.secret_key = generate_secret_key()
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app)
UPLOAD_FOLDER = './static/img/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
results = {}

def on_json_loading_failed_return_dict(e):
    return {}
# user_id 컬럼의 nickname, id가 존재하는지의 대한 판단 주석
@app.route('/user_id_exist', methods=['GET'])
def check_nickname_exist():
    user_id_data = Customer()
    # user_id_data
    # print('user_id_data', user_id_data)
    AppData.nickname = app_data.nickname
    print(AppData.nickname)
    user_names_set = set(entry['user_name'] for entry in user_id_data)
    # if AppData.nickname is None:
        # return jsonify({'message': 'user_id is not'}), 400
    if AppData.nickname in user_names_set:    
        response = {'result': True}
<<<<<<< HEAD
        print(type(response))
=======
>>>>>>> 405bd414216966947ce40d37de2cfbe44c1f672d
    elif AppData.nickname == None:
        response = {'result': False}
    else:
        response = {'result': False}
    return jsonify(response)

@app.route('/review_counts', methods=['GET'])
def check_review_count():
    AppData.nickname = app_data.nickname
    user_id_data = Customer()
    data = pd.read_csv('purchase_data.csv')
    user_id_data = pd.DataFrame(user_id_data)
    # data = pd.DataFrame(data)
    user_idx = user_id_data[user_id_data['user_name'] == AppData.nickname].index[0]
    id_counts = len(data[data['user_idx'] == user_idx])
    print('리뷰는 몇개인가요오오오오오오오오',id_counts)

    if id_counts >= 10:
        response = {'result': True}
    else:
        response = {'result': False}
    return jsonify(response)

def user_index():
    AppData.nickname = app_data.nickname
    user_id_data = Customer()
    user_id_data = pd.DataFrame(user_id_data)
    # data = pd.DataFrame(data)
    user_idx = user_id_data[user_id_data['user_name'] == AppData.nickname].index[0]
    return user_idx

@app.route('/')
def main():
    return render_template('main.html')

class AppData:
    nickname = None
    skin_tone = None
<<<<<<< HEAD
    keyword = None

app_data = AppData()
skin_tone = AppData()
keyword = AppData()
=======

app_data = AppData()
skin_tone = AppData()
>>>>>>> 405bd414216966947ce40d37de2cfbe44c1f672d

# 사용자의 이미지, 닉네임을 입력받은 값을 서버에서 받아 이미지는 저장해주고
# nickname 값은 class 변수에 저장
@app.route('/second', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        image_file = request.files['image']
        nickname = request.values['nickname']
        
        if image_file is not None:
            image_name = 'img.jpg'
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
            
            image_file.save(image_path)
            print(image_path)

            app_data.nickname = nickname
            print(app_data.nickname)
        
            season, person, explain, season_background, jewelry, hair, blusher, lip = get_prediction_data(image_path)

            response = {
                'season': season,
                'person': person,
                'explain': explain,
                'season_background': season_background,
                'jewelry': jewelry,
                'hair': hair,
                'blusher': blusher,
                'lip': lip,
            }
            
            return jsonify(response)
        else:
            response = {'message': 'No image file received'}
            return jsonify(response), 400
    else:
        return render_template('second.html')


# 이미지 파일을 사용하는 퍼스널 컬러 진단 모델
def get_prediction_data(image_path):
    classifier = SkinToneClassifier()
    cropped_face = classifier._get_face_region(image_path)
    if cropped_face is not None:
        skin_tone = classifier.classify_skin_tone(image_path)

        if skin_tone == 'spring_warm':
            season_background = '../static/img/spring.png'
            season = '봄 웜'
            person = '#수지 #아이유 #이제훈'
            explain = '#밝은 #부드러운 #귀여운 #따뜻한'
            jewelry = '골드/브론즈/내츄럴진주'
            hair = '다크브라운/라이트브라운'
            blusher = '코랄/오렌지 계열'
            lip = '핑크베이지/살몬핑크 계열'
        elif skin_tone == 'summer_cool':
            season_background = '../static/img/summer.png'
            season = '여름 쿨'
            person = '#송강 #아이린 #김연아'
            explain = '#맑은 #깨끗한 #세련된 #청량한'
            jewelry = '실버/화이트골드/백진주'
            hair = '블론드/블랙'
            blusher = '푸른빛 핑크/라벤더 계열'
            lip = '베이비핑크/로즈핑크 계열'       
        elif skin_tone == 'fall_warm':
            season_background = '../static/img/fall.png'
            season = '가을 웜'
            person = '#제니 #유승호 #이효리'
            explain = '#내츄럴 #섹시한 #편안한 #차분한'
            jewelry = '골드/브론즈/내추럴진주'
            hair = '카키브라운/애쉬브라운'
            blusher = '인디핑크/테라코타'
            lip = '말린장미/오렌지레드 계열'
        else:
            season_background = '../static/img/winter.png'
            season = '겨울 쿨'
            person = '#선미 #차은우 #카리나'
            explain = '#시크한 #섹시한 #카리스마'
            jewelry = '실버/화이트골드/백진주'
            hair = '블론드/블루블랙'
            blusher = '푸른빛이 강한 핑크계열'
            lip = '버건디/딥로즈/첼리 계열'

        AppData.skin_tone = season
        print(AppData.skin_tone)
        return season, person, explain, season_background, jewelry, hair, blusher, lip  
    else:
        season_background =''
        season = '얼굴이 없으십니다.'
        person = ''
        explain = ''
        jewelry = ''
        hair = ''
        blusher = ''
        lip = ''

        return season, person, explain, season_background, jewelry, hair, blusher, lip

# result.html에게 nickname을 응답해 준다.
# @app.route('/give_nick_skin', methods=['GET'])
# def give_nickname():
#     # nickname = request.form.get('nickname')
#     AppData.nickname = app_data.nickname
#     season= AppData.skin_tone
#     print(AppData.nickname)
#     print(season)
#     data = {
#         'nickname': AppData.nickname,
#         'skin_tone': season
#         }
#     return jsonify(data)

# get_prediction_data 함수를 사용해서 퍼스널 컬리 진단 결과를 result로 보내준다.
@app.route('/result', methods=['GET', 'POST'])
def result_page():
    image_path = './static/img/img.jpg'
    AppData.nickname = app_data.nickname
    season, person, explain, season_background, jewelry, hair, blusher, lip = get_prediction_data(image_path)
    return render_template('result.html', people=AppData.nickname, season=season, person=person, explain=explain, image_url=image_path, season_background=season_background, jewelry=jewelry, hair=hair, blusher=blusher, lip=lip)    

<<<<<<< HEAD
@app.route('/user_keywords', methods=['POST'])
def skin_data():
    global results
    keywords = request.json # keyword
    # print(keywords)
    AppData.keyword = keywords
    print("AppData.keyword = ", AppData.keyword)

    season = AppData.skin_tone
    print('계절 알려주세요', season)

    cosmetic_type = AppData.keyword["cosmetic_type"]
    del AppData.keyword["cosmetic_type"]
=======
@app.route('/user_keywords', methods=['GET','POST'])
def skin_data():
    keywords = request.json # keyword
    print(keywords)

    season = AppData.skin_tone
    print('계절 알려주세요',season)
>>>>>>> 405bd414216966947ce40d37de2cfbe44c1f672d

    recommend = Recommend()
    recommend = pd.DataFrame(recommend)
    print('recommend', recommend)
    
    product_score = Product_score()
    product_score = pd.DataFrame(product_score)
    print('product_score', product_score)
    
    product = Product()
    product = pd.DataFrame(product)
    print('product', product)

    popularity_result = popularity_based(recommend, product_score, keywords, season)
    print('popularity_result', popularity_result)
    recommended_items = get_reco_prd_info(product, popularity_result)
    print('recommended_items',recommended_items)
    # return recommended_items

<<<<<<< HEAD
    results["jh"] = recommended_items
    return redirect('/final_without_name')
=======
    return render_template('final_page.html')
>>>>>>> 405bd414216966947ce40d37de2cfbe44c1f672d

# content_based로 연결 되도록 라우터 정의
@app.route('/content_based')
def content_based():
    return render_template('content_based.html')

# @app.route('/get_recommendation', methods=['GET'])
<<<<<<< HEAD
def get_recommendation():    # collaborative를 위한 함수
=======
def get_recommendation():
>>>>>>> 405bd414216966947ce40d37de2cfbe44c1f672d
    recommend_type = request.args.get('recommend_type')
    print('######################',recommend_type)
    product_score = Product_score()
    product_score = pd.DataFrame(product_score)
    print('@@@@@@@@@@@@@', product_score)
<<<<<<< HEAD
    purchase = Purchase()
    purchase = pd.DataFrame(purchase)
    # purchase = pd.read_csv('purchase_data.csv')
    # print('!!!!!!!!!!')
    product = Product()
    product = pd.DataFrame(product)
    # print('((()))')
    recommend = Recommend()
    recommend = pd.DataFrame(recommend)
    # print('*********')
    AppData.nickname = app_data.nickname
    # print('&&&&&&&&&&')
=======
    # purchase = Purchase()
    purchase = pd.read_csv('purchase_data.csv')
    print('!!!!!!!!!!')
    product = Product()
    product = pd.DataFrame(product)
    print('((()))')
    recommend = Recommend()
    recommend = pd.DataFrame(recommend)
    print('*********')
    AppData.nickname = app_data.nickname
    print('&&&&&&&&&&')
>>>>>>> 405bd414216966947ce40d37de2cfbe44c1f672d
    season = AppData.skin_tone
    print(season)

    if recommend_type == 'plus':
        result = collaborative(product_score, purchase, user_index(), season)
        print('협업필터링의 result입니다', result)
        data = get_reco_prd_info(product, result)
        print('여기를 통과했다면 리뷰가 10개 이상인 겁니다.')
        return data
    elif recommend_type == 'less':
        result = contents_based(recommend, purchase, user_index(), season)
        print('콘텐츠베이스의 result입니다',result)
        data = get_reco_prd_info(product, result)
        print('여기를 통과했다면 리뷰가 10개가 안되는 겁니다.')
        return data
    
@app.route('/final_page', methods=['GET'])
def final_page():
    global results
    cosmetic_type = request.args.get('cosmetic_type')
<<<<<<< HEAD
    without = request.args.get('without')
    result = None

    if without == 'true':
        result = results["jh"][cosmetic_type]
    else:
        print('코스메틱 타입 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!',cosmetic_type) # 이게 프린트가 되지 않고 다음으로 넘어감
        if app_data.nickname not in results:
            results[app_data.nickname] = get_recommendation()
        print('올해의 노벨코딩상은 노재희씨에게', results[app_data.nickname]) # data is a dictionary which should have 3 keys, not..

        # 립만 받아오고, 아이랑 블러셔는 안 받아오고 있음 
        if cosmetic_type in results[app_data.nickname]: # data should be a dictionary consists of 3keys, cosmetic_type is a dictionary key, [lip_data, eyeshadow_data,blusher_data]
            result = results[app_data.nickname][cosmetic_type] # result should be a dictionary 
            print('재희씨 금연 1일차',result) 
        else:
            result = {}
=======
    print('코스메틱 타입 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!',cosmetic_type) # 이게 프린트가 되지 않고 다음으로 넘어감
    if app_data.nickname not in results:
        results[app_data.nickname] = get_recommendation()
    print('올해의 노벨코딩상은 노재희씨에게', results[app_data.nickname]) # data is a dictionary which should have 3 keys, not..

    # 립만 받아오고, 아이랑 블러셔는 안 받아오고 있음 
    if cosmetic_type in results[app_data.nickname]: # data should be a dictionary consists of 3keys, cosmetic_type is a dictionary key, [lip_data, eyeshadow_data,blusher_data]
        result = results[app_data.nickname][cosmetic_type] # result should be a dictionary 
        print('재희씨 금연 1일차',result) 
    else:
        result = {}
>>>>>>> 405bd414216966947ce40d37de2cfbe44c1f672d

    return render_template('final_page.html', **result)

if __name__ == '__main__':
    app.run(debug=True)