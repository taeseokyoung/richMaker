import random,re
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


# 비밀번호만 검증
def validated_password(password):
    password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    password_match = re.match(password_pattern, password)
    return bool(password_match)

# 유저 이름 검증
def validated_username(username):
    check = [
        lambda element: len(element) == len(element.replace(" ", "")),
        # 공백이 포함 되어 있을 경우 False
        lambda element: True if (len(element) > 1 and len(element) < 21) else False,
        # 전달된 값의 개수가 1~20 사이일 경우 True
    ]
    for i in check:
        if not i(username):
            return False
    return True

# email,password,username 검증
def validated_data(email,password,username):
    password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    password_match = re.match(password_pattern, password)
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    email_match = re.match(email_pattern, email)

    if not bool(password_match):
        return "비밀번호가 올바르지 않습니다."
    elif not bool(email_match):
        return "이메일이 올바르지 않습니다."

    check =[
        lambda element: len(element) == len(element.replace(" ", "")),
        # 공백이 포함 되어 있을 경우 False
        lambda element: True if (len(element) > 1 and len(element) < 21) else False,
        # 전달된 값의 개수가 1~20 사이일 경우 True
    ]
    for i in check:
        if not i(username):
            return "유저이름이 올바르지 않습니다."

    return True


