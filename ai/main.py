import requests
import uuid
import time
import json
import os


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
    response_dict = response_dict['images'][0]
    
    store_name = response_dict.get('receipt', {}).get('result', {}).get('storeInfo', {}).get('name', {}).get('formatted', '')
    biz_num = response_dict.get('receipt', {}).get('result', {}).get('storeInfo', {}).get('bizNum', {}).get('formatted', '')
    address = response_dict.get('receipt', {}).get('result', {}).get('storeInfo', {}).get('addresses', [{}])[0].get('formatted', '')
    phone_number = response_dict.get('receipt', {}).get('result', {}).get('storeInfo', {}).get('tel', [{}])[0].get('formatted', '')
    payment_date = response_dict.get('receipt', {}).get('result', {}).get('paymentInfo', {}).get('date', {}).get('formatted', '')
    payment_time = response_dict.get('receipt', {}).get('result', {}).get('paymentInfo', {}).get('time', {}).get('formatted', '')
    card_company = response_dict.get('receipt', {}).get('result', {}).get('paymentInfo', {}).get('cardInfo', {}).get('company', {}).get('formatted', '')
    card_number = response_dict.get('receipt', {}).get('result', {}).get('paymentInfo', {}).get('cardInfo', {}).get('number', {}).get('formatted', '')
    confirm_number = response_dict.get('receipt', {}).get('result', {}).get('paymentInfo', {}).get('cardInfo', {}).get('confirmNum', {}).get('formatted', '')
    item_name = response_dict.get('receipt', {}).get('result', {}).get('subResults', [{}])[0].get('items', [{}])[0].get('name', {}).get('formatted', '')
    item_count = response_dict.get('receipt', {}).get('result', {}).get('subResults', [{}])[0].get('items', [{}])[0].get('count', {}).get('formatted', '')
    total_price = response_dict.get('receipt', {}).get('result', {}).get('totalPrice', {}).get('price', {}).get('formatted', '')
                

    
    return {
    'store_name': store_name,
    'biz_num': biz_num,
    'address': address,
    'phone_number': phone_number,
    'payment_date': payment_date,
    'payment_time': payment_time,
    'card_company': card_company,
    'card_number': card_number,
    'confirm_number': confirm_number,
    'item_name': item_name,
    'item_count': item_count,
    'total_price': total_price,
    }
