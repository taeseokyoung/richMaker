import requests
import uuid
import time
import json


def AiCheck(base64_string):
    # 응답 받기
    file_format = base64_string.split(',')[0].split('/')[1].split(';')[0]
    only_string = base64_string.split(',')[1]
    api_url = 'https://7y32xyp5al.apigw.ntruss.com/custom/v1/22746/a95dff560047aeb4f5cd2d25581b2eb3ce725a9f91bd9809a96659dd2ea73d88/document/receipt'
    secret_key = 'VU1GclRnbGZwWWd2cVVMR1ZiVmJzYVpSY1pXRml3RmE='

    request_json = {
        'images': [
            {
                'format': file_format,
                'name': 'demo',
                'data': only_string
            }
        ],
        'requestId': str(uuid.uuid4()),
        'version': 'V2',
        'timestamp': int(round(time.time() * 1000))
    }

    payload = json.dumps(request_json).encode('UTF-8')
    headers = {
        'X-OCR-SECRET': secret_key,
        'Content-Type': 'application/json'
    }

    response = requests.request(
        "POST", api_url, headers=headers, data=payload, timeout=10)
    response_dict = json.loads(response.text)
    # print(response.text)
    
    # 추출
    store_info = response_dict['images'][0]['receipt']['result']['storeInfo']
    payment_info = response_dict['images'][0]['receipt']['result']['paymentInfo']
    sub_results = response_dict['images'][0]['receipt']['result']['subResults']
    total_price_dict = response_dict['images'][0]['receipt']['result']['totalPrice']
    
    biz_name = store_info['name']['formatted'].get('value', "") # 사업장 이름
    biz_num = store_info['bizNum']['formatted'].get('value', "") # 사업자 등록번호
    biz_address = store_info['addresses'][0]['formatted'].get('value', "") # 사업장 주소
    biz_tel = store_info['tel'][0]['formatted'].get('value', "") # 사업장 전화번호
    payment_date = payment_info['date'].get('text', "") # 거래 날짜
    payment_time = payment_info['time'].get('text', "") # 거래 시간
    payment_card = payment_info['cardInfo']['company']['formatted'].get('value', "") # 카드 회사
    payment_card_number = payment_info['cardInfo']['number']['formatted'].get('value', "") # 카드 번호
    payment_approved_number = payment_info['confirmNum'].get('text', "") # 승인 번호
    items = {} # 구매한 아이템
    for item in sub_results[0]['items']:
        items[item['name']['formatted']['value']] = item['count']['formatted']['value']
    total_price = total_price_dict['price']['formatted'].get('value', "") # 총 금액
    
    return {
        'biz_name': biz_name,
        'biz_num': biz_num,
        'biz_address': biz_address,
        'biz_tel': biz_tel,
        'payment_date': payment_date,
        'payment_time': payment_time,
        'payment_card': payment_card,
        'payment_card_number': payment_card_number,
        'payment_approved_number': payment_approved_number,
        'items': items,
        'total_price': total_price
    }
    


    
    
    
    
    
    
    
    
    print(storeInfo)
    hopeful_data_list = ['storeInfo', ]
    meaningful_data = {}
    need_visit = []
    # need_visit.append()
    while need_visit:
        pass


    