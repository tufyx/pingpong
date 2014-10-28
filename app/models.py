from app import db
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, DateTime

ROLE_USER  = 0
ROLE_ADMIN = 1

class User(db.Model):
    __tablename__ = "users"
    
    id         = Column(Integer, primary_key = True)
    email      = Column(String(255), index = True, unique = True)
    password   = Column(String(255))
    first_name = Column(String(255))
    last_name  = Column(String(255))
    confirmed  = Column(Integer)
    
    @staticmethod
    def getByID(userID):
        user = User.query.get(userID)
        return user.serialize() if user else None
    
    @staticmethod
    def getNameForUserID(userID = -1):
        if userID == "-1":
            return "bye"
        else:
            user = User.query.get(userID)
            user = user.serialize() if user else None
            if user:
                return user.get("name", "")
            else:
                return "-"
        
    @staticmethod
    def all():
        users = User.query.order_by("id").filter_by(confirmed = 1).all()
        return [user.serialize() for user in users]
    
    def serialize(self):
        return {
            'id': self.id, 
            'email': self.email,
            'first_name':self.first_name,
            'last_name':self.last_name,
            'name': self.first_name + " " + self.last_name
        }
    
    def __repr__(self):
        return '<User %r>' % (self.email)

class Match(db.Model):
    __tablename__ = "matches"
    
    id             = Column(Integer, primary_key = True)
    competition_id = Column(String(255))
    match_id       = Column(String(255))
    date           = Column(DateTime)
    round          = Column(Integer) # 0 - group, 1,2.... knockout stages
    pool           = Column(String(1))
    player_a       = Column(String(255))
    player_b       = Column(String(255))
    nr_sets        = Column(Integer)
    
    
    @staticmethod
    def getById(matchID):
        matches = Match.query.filter_by(match_id = matchID).all()
        return [match.serialize() for match in matches]
    
    @staticmethod
    def getByCompetitionID(self, competitionID):
        matches = Match.query.filter_by(competition_id = competitionID).order_by(round).all()
        return [match.serialize() for match in matches]
    
    @staticmethod
    def all():
        matches = Match.query.all()
        return [match.serialize() for match in matches]
    
    def __repr__(self):
        return '<Match %r>' % (self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'competition_id': self.competition_id,
            'match_id':self.match_id,
            'round':self.round,
            'player_a':self.player_a,
            'player_b':self.player_b,
            'player_a_name':User.getNameForUserID(self.player_a),
            'player_b_name':User.getNameForUserID(self.player_b),
            'sets':self.nr_sets
        }
    
class Result(db.Model):
    __tablename__ = "results"
    
    id       = Column(Integer, primary_key = True)
    match_id = Column(String(255))
    set_id   = Column(Integer)
    result_a = Column(Integer)
    result_b = Column(Integer)
    
    @staticmethod
    def getByMatchID(matchID):
        results = Result.query.filter_by(match_id = matchID).order_by("set_id").all()
        return [result.serialize() for result in results]
        
    def serialize(self):
        return {
            'id': self.id,
            'match_id': self.match_id,
            'set_id': self.set_id,
            'result_a': self.result_a,
            'result_b': self.result_b,
        }