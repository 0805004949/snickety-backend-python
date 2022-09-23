"""
model.tweet_dao
~~~~~~~~~~~~~~~~~~~
레이어드 아키텍처에서 모델부 (디비 연결부분)
- tweet 작성
- 타임라인 반환
"""
from sqlalchemy import text 

class TweetDao:
    def __init__(self,database) -> None:
        self.db = database
    
    def insert_tweet(self, user_id, tweet):
        sql = text("""
        INSERT INTO tweets (
            user_id, tweet
        ) VALUES ( :id, :tweet)
        """)
        return self.db.execute(sql,
                                 {'id':user_id, 
                                  'tweet':tweet}
                                 ).rowcount
    
    def get_timeline(self, user_id):
        sql = text("""
                   SELECT t.user_id, t.tweet 
                   FROM tweets t
                   LEFT JOIN users_follow_list ufl 
                   ON ufl.user_id =: user_id
                   WHERE t.user_id = :user_id
                   OR t.user_id = ufl.follow_user_id
                   """)
        timeline = self.db.execute(sql,
                               {'user_id':user_id}
                               ).fetchall()
        
        return [{'user_id':tweet['user_id'], 'tweet':tweet['tweet']} for tweet in timeline]
        