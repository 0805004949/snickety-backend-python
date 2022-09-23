"""
service.user_service
~~~~~~~~~~~~~~~~~~~
레이어드 아키텍처에서 서비스레이어(비즈니스 로직구현)
프레젠테이션 레이어(view)에게서는 독립적이지만
모델레이어에게 종속적임

- 로그인
- 회원가입
- 유저가 팔로잉
- 유저가 언팔로잉
- 유저의 타임라인
- 로그인후 세션유지를 위한 토큰 발행
- 로그인 확인을 위한 비밀번호 생성 

"""
import jwt
import bcrypt

from datetime import datetime, timedelta

class UserService:
    def __init__(self, user_dao, config):
        self.user_dao = user_dao
        self.config   = config
    
    def create_new_user(self, new_user):
        new_user['password'] = bcrypt.hashpw(
            new_user['password'].encode('utf8'),
            bcrypt.gensalt()
        )
        
        new_user_id = self.user_dao.inser_user(new_user)
        
        return new_user_id
    
    def login(self, credential):
        email = credential['email']
        password = credential['password']
        user_credential = self.user_dao.get_user_id_and_password(email)
        
        authorized = user_credential and bcrypt.checkpw(password.encode('utf8'),
                                                        user_credential['hashed_password'].encode('utf8'),
                                                        )
        return authorized
    
    def follow(self, user_id, follow_id):
        return self.user_dao.insert_follow(user_id, follow_id)
    
    def unfollow(self, user_id, unfollow_id):
        return self.user_dao.insert_unfollow(user_id, unfollow_id)
    
    def generate_token(self, user_id):
        payload = {
            'user_id' : user_id,
            'exp' : datetime.utcnow() + timedelta(seconds = 60 * 60 * 24)
        }
        token = jwt.encode(payload, self.config.JWT_SECRET_KEY, 'HS256')
        
        return token.decode('utf-8')
    
    def get_user_id_and_password(self, email):
        return self.user_dao.get_user_id_and_password(email)