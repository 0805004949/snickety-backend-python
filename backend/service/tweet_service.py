"""
service.utweet_service
~~~~~~~~~~~~~~~~~~~
레이어드 아키텍처에서 서비스레이어(비즈니스 로직구현)
프레젠테이션 레이어(view)에게서는 독립적이지만
모델레이어에게 종속적임

- 트윗 작성 단 300자 미만일경우
- 타임라인 반환
"""
class TweetService:
    def __init__(self, tweet_dao):
        self.twett_dao = tweet_dao
        
    def tweet(self, user_id, tweet):
        if len(tweet) > 300:
            return None
        return self.tweet_dao.insert_tweet(user_id, tweet)
    
    def get_timeline(self, user_id):
        return self.tweet_dao.get_timeline(user_id)