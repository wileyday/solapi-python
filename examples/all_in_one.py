import json
import time
import datetime
import uuid
import hmac
import hashlib
import requests

# apiKey, apiSecret 입력 필수
apiKey = 'INPUT YOUR API KEY'
apiSecret = 'INPUT YOUR SECRET KEY'

# 아래 값은 필요시 수정
protocol = 'https'
domain = 'api.solapi.com'
prefix = ''

def unique_id():
    return str(uuid.uuid1().hex)

def get_iso_datetime():
    utc_offset_sec = time.altzone if time.localtime().tm_isdst else time.timezone
    utc_offset = datetime.timedelta(seconds=-utc_offset_sec)
    return datetime.datetime.now().replace(tzinfo=datetime.timezone(offset=utc_offset)).isoformat()

def get_signature(key, msg):
    return hmac.new(key.encode(), msg.encode(), hashlib.sha256).hexdigest()

def get_headers(apiKey, apiSecret):
    date = get_iso_datetime()
    salt = unique_id()
    data = date + salt
    return {
      'Authorization': 'HMAC-SHA256 ApiKey=' + apiKey + ', Date=' + date + ', salt=' + salt + ', signature=' +
                             get_signature(apiSecret, data),
      'Content-Type': 'application/json; charset=utf-8'
    }

def getUrl(path):
  url = '%s://%s' % (protocol, domain)
  if prefix != '':
    url = url + prefix
  url = url + path
  return url

def sendMany(data):
  return requests.post(getUrl('/messages/v4/send-many'), headers=get_headers(apiKey, apiSecret), json=data)

# 한번 요청으로 1만건의 메시지 발송이 가능합니다.
if __name__ == '__main__':
  data = {
    'messages': [
      {
        'to': '01000000001',
        'from': '029302266',
        'text': '한글 45자, 영자 90자 이하 입력되면 자동으로 SMS타입의 메시지가 추가됩니다.'
      },
      {
        'to': '01000000002',
        'from': '029302266',
        'text': '한글 45자, 영자 90자 이상 입력되면 자동으로 LMS타입의 문자메시자가 발송됩니다. 0123456789 ABCDEFGHIJKLMNOPQRSTUVWXYZ'
      },
      {
        'type': 'SMS',
        'to': '01000000003',
        'from': '029302266',
        'text': 'SMS 타입에 한글 45자, 영자 90자 이상 입력되면 오류가 발생합니다. 0123456789 ABCDEFGHIJKLMNOPQRSTUVWXYZ'
      },
      {
        'to': [ '01000000004', '01000000005' ], # 수신번호를 array로 입력하면 같은 내용을 여러명에게 보낼 수 있습니다.
        'from': '029302266',
        'text': '한글 45자, 영자 90자 이하 입력되면 자동으로 SMS타입의 메시지가 발송됩니다.'
      },
      # 해외발송
      {
        'country': '1', # 미국(1), 일본(81), 중국(86) 등 국가번호 입력
        'to': '01000000006', # 수신번호를 array로 입력하면 같은 내용을 여러명에게 보낼 수 있습니다.
        'from': '029302266',
        'text': '한글 45자, 영자 90자 이하 입력되면 자동으로 SMS타입의 메시지가 발송됩니다.'
      },
      # 알림톡 발송
      {
        'to': '01000000004',
        'from': '029302266',
        'kakaoOptions': {
          'pfId': 'KA01PF200323182344986oTFz9CIabcx',
          'templateId': 'KA01TP200323182345741y9yF20aabcx',
          # 변수: 값 형식으로 모든 변수에 대한 변수값 입력
          'variables': {
            '#{변수1}': '변수1의 값',
            '#{변수2}': '변수2의 값',
            '#{버튼링크1}': '버튼링크1의 값',
            '#{버튼링크2}': '버튼링크2의 값',
            '#{강조문구}': '강조문구의 값'
          }
        }
      }
      # ...
      # 1만건까지 추가 가능
    ]
  }
  res = sendMany(data)
  print(json.dumps(res.json(), indent=2, ensure_ascii=False))
