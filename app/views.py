'''
Created on 19 Aug 2014

@author: tufyx
'''
from app import app, db
from flask.globals import request
from flask_cors import cross_origin
from flask.json import jsonify

from models import User
from app.matches import build_knockout
from app.utils import generate_password, verify, generate_result
from random import randrange
from sqlalchemy.exc import IntegrityError
from os.path import sys
from app.models import Match, Result
from app.utils import prepare_response

# SEASON ENDPOINTS
@app.route('/users', methods = ['GET'])
@app.route('/user/<userID>', methods = ['GET'])
@cross_origin()
def getUser(userID = None):
    if userID:
        response = User.getByID(userID)
    else:
        response = User.all()
    return prepare_response(response)
     
 
@app.route('/user/add', methods = ['POST'])
@cross_origin()
def addUser():
    data = request.json;
    user = User(email = data['email'],
                first_name = verify(data['first_name']),
                last_name = verify(data['last_name']),
                password  = generate_password(),
                confirmed = 1)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        return prepare_response(False, "integrity_error")
    
    return prepare_response(True)
 
@app.route('/user/addmore/<int:nrUsers>',methods=['GET'])
@cross_origin()
def addMore(nrUsers):
    count = 0
    firstnames = ["John","Jack","Jill","Mike","Shaun","Dan","Emily","Hellen"]
    lastnames = ["Moore","Doe","Snow","Anderson","Ruby","Green","Cooper"]
    used_emails = []
    while count < nrUsers:
        count += 1
        validEmail = False
        firstname = ""
        lastname = ""
        while not validEmail:
            firstname = firstnames[randrange(0,len(firstnames))]
            lastname = lastnames[randrange(0,len(lastnames))] 
            email = ".".join([firstname, lastname]).lower()
            if email not in used_emails:
                used_emails.append(email)
                validEmail = True
                
        user = User(email = email + "@mydomain.nl",
                    first_name = firstname,
                    last_name = lastname,
                    password = generate_password(),
                    confirmed = 1)
        db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        print sys.exc_info()
        return "Error while inserting data"
        
    return "True"
    
     
@app.route('/user/edit/<userID>', methods=['POST'])
@cross_origin()
def editUser(userID):
    data = request.json;
    user = User.getByID(userID)
    if user:
        db.session.query(User).filter_by(id = userID).update({"email":data['email'],
                                                              "first_name":data['firstName'],
                                                              "last_name":data['lastName'],
                                                              "password":data['password']
                                                              })
        db.session.commit()
        return jsonify(response = True)
    else:
        return jsonify(response = False, error = "ID %r NOT FOUND" %seasonID.encode())
    
@app.route('/matches', methods=['GET'])    
@app.route('/matches&stage=<stage>', methods=['GET'])
@app.route('/matches/competition/<competitionID>&stage=<stage>', methods=['GET'])
@cross_origin()
def getMatchesInCompetition(stage = None, competitionID = None):
    if competitionID:
        response = Match.getByCompetitionID(competitionID)
    else:
        response = Match.all()
        
    all_matches = {}
    aux = []
    if stage is not None:
        aux = [match for match in response if match['round'] == int(stage) or match['round'] == int(stage)+1]
    else:
        aux = response
    
    response = aux
    for match in response:
        r = match['round']
        match['result'] = Result.getByMatchID(match['match_id'])
        if r not in all_matches.keys():
            all_matches[r] = []
#         match['offset'] = 2**(match['round'] - 1) - 1
#         match['height'] = 2**match['round'] - 1
#         match['offset'] = 2**(len(all_matches) - 1) - 1
#         match['height'] = 2**len(all_matches) - 1
        match['offset'] = 2**(len(all_matches) - 1) - 1
        match['height'] = len(all_matches)**2 - len(all_matches)
        all_matches[r].append(match)
    return prepare_response(all_matches)

@app.route('/results/randomize', methods=['GET'])
@app.route('/results/randomize/<stage>', methods=['GET'])
def generateResults(stage = None):
    response = Match.all()
    results = []
    for match in response:
        if match['round'] == int(stage):
            if match['player_a'] == str(-1) or match['player_b'] == str(-1):
                continue
            set_count = 0
            w_a = 0
            w_b = 0
            while set_count < match['sets']:
                set_count += 1
                result = generate_result()
                if result[0] > result[1]:
                    w_a += 1
                else:
                    w_b += 1
                
                r = Result(match_id = match['match_id'],
                           set_id = set_count,
                           result_a = result[0],
                           result_b = result[1])
                results.append(r.serialize())
                db.session.add(r)
                if w_a == 3 or w_b == 3:
                    break
    try:
        db.session.commit()
    except:
        print sys.exc_info()
        return prepare_response(None, "Error while inserting")
    return prepare_response(True)

def calculate_winner(player_a, player_b, results, match_id):
    if player_a == str(-1):
        db.session.query(Match).filter_by(player_a = match_id).update({"player_a":player_b})
        db.session.query(Match).filter_by(player_b = match_id).update({"player_b":player_b})
    elif player_b == str(-1):
        db.session.query(Match).filter_by(player_a = match_id).update({"player_a":player_a})
        db.session.query(Match).filter_by(player_b = match_id).update({"player_b":player_a})
    else:
        score = {"a":0, "b":0}
        for result in results:
            if result['result_a'] > result['result_b']:
                score['a'] += 1
            else:
                score['b'] += 1
        if score['a'] > score['b']:
            db.session.query(Match).filter_by(player_a = match_id).update({"player_a":player_a})
            db.session.query(Match).filter_by(player_b = match_id).update({"player_b":player_a})
        elif score['a'] < score['b']:
            db.session.query(Match).filter_by(player_a = match_id).update({"player_a":player_b})
            db.session.query(Match).filter_by(player_b = match_id).update({"player_b":player_b})
            
    db.session.commit()

@app.route('/results/check', methods=['GET'])
@app.route('/results/check/<matchID>', methods=['GET'])
@cross_origin()
def check_results(matchID = None):
    if matchID is None:
        matches = Match.all()
    else:
        matches = Match.getById(matchID)
         
    for match in matches:
        match['results'] = Result.getByMatchID(match['match_id'])
        calculate_winner(match['player_a'], match['player_b'], match['results'], match['match_id'])
        
    return prepare_response(True)    
    

@app.route('/matches/generate&format=<tournament_format>', methods=['GET'])    
@app.route('/matches/generate&format=<tournament_format>&group_size=<group_size>', methods=['GET'])    
@cross_origin()
def generateTournament(tournament_format, group_size = 0):
    users = User.all()
    players = [user.get("id",-1) for user in users]
    
    if tournament_format == "knockout":
        status = create_knockout_tournament(players)
    elif tournament_format == "roundrobin":
        status = build_roundrobin(players)
    elif tournament_format == "mixed":
        status = build_mixed(players)
    else:
        return jsonify(response = False, status = status)
    
    return jsonify(response = True, status = status)

def create_knockout_tournament(players):
    matches = build_knockout(players)
    
    for match in matches:
            m = Match(competition_id = match[0],
                      match_id = match[1],
                      player_a = match[2],
                      player_b = match[3],
                      round = match[4],   
                      pool  = "-",
                      nr_sets = 5)
            db.session.add(m)
    try:
        db.session.commit()
    except:
        print sys.exc_info()
        return 400
    return 200

def build_roundrobin(players):
    return 200

def build_mixed(players):
    return 200