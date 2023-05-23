import random
import re
from django.core.mail import EmailMessage
# 검증 및 이메일 발송
def send_email(email):
    code = "".join([str(random.randint(0, 9)) for _ in range(6)])
    title = "💰리.치.메.이.커.💰"
    string = "리치메이커에서 회원님의 가입 인증을 위한 코드를 발송했습니다.\n"
    string += "스파르타 코딩클럽 학생들의 팀 프로젝트이니 혹여 요쳥하신적이 없다면 무시해주세요.\n"
    string += "요청하신분이 맞다면, 아래의 인중코드를 인증란에 작성해주십시오.\n"
    string += code
    content = string
    mail = EmailMessage(title,content,to=[email])
    mail.send()
    return code


def validated_password(password):
    check = [
        lambda element: all(
            x.isdigit() or x.islower() or x.isupper() or (x in ['!', '@', '#', '$', '%', '^', '&', '*', '_']) for x
            in element),
        # 요소 하나 하나를 순환하며 숫자,소문자,대문자,지정된 특수문자 제외한 요소가 있을경우 False
        lambda element: len(element) == len(element.replace(" ", "")),
        # 공백이 포함 되어 있을 경우 False
        lambda element: True if (len(element) > 7 and len(element) < 21) else False,
        # 전달된 값의 개수가 8~20 사이일 경우 True
        lambda element: any(x.islower() or x.isupper() for x in element),
        # 요소 하나하나를 순환하며, 요소중 대문자 또는 소문자가 있어야함(숫자로만 가입 불가능)
        lambda element: any(map(lambda x: x in element, ['!', '@', '#', '$', '%', '^', '&', '*', '_'])),
        # 요소를 순환하며 최소 하나 이상의 특수기호가 있는지 확인
    ]
    for i in check:
        if not i(password):
            return False
    return True
    # good bye...
    # pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    # match = re.match(pattern, password)
    # return bool(match)

