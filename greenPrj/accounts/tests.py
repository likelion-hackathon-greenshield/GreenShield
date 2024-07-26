from django.test import TestCase

# Create your tests here.

# 서버 아이디 : 가영이다1234 (6자 ~ 20자 제한/중복검사 통과),
# 비밀번호 :rkduddlek1234@ (문자, 숫자, 특수문자 포함 8자~20자/확인-재확인 동일조건 반영 통과)
# 이름 : 권가영, 전화번호 : 01012345678 (11자 제한)
# 이메일 : 1234@naver.com (이메일 필드), 생년월일 : 2003년 5월 24일(날짜선택기 사용/YYYY-MM-DD형식으로 처리)