import requests
import uuid
import time
import json

api_url = 'https://7y32xyp5al.apigw.ntruss.com/custom/v1/22746/a95dff560047aeb4f5cd2d25581b2eb3ce725a9f91bd9809a96659dd2ea73d88/document/receipt'
secret_key = 'VU1GclRnbGZwWWd2cVVMR1ZiVmJzYVpSY1pXRml3RmE='
image_file = 'ai/images/02.jpg'

request_json = {
    'images': [
        {
            'format': 'jpg',
            'name': 'demo'
        }
    ],
    'requestId': str(uuid.uuid4()),
    'version': 'V2',
    'timestamp': int(round(time.time() * 1000))
}

payload = {'message': json.dumps(request_json).encode('UTF-8')}
files = [
  ('file', open(image_file,'rb'))
]
headers = {
  'X-OCR-SECRET': secret_key
}

response = requests.request("POST", api_url, headers=headers, data = payload, files = files)

print(response.text)

