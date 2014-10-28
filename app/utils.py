import random
from flask.json import jsonify
from random import randrange

def generate_password(size=10):
    return ''.join(random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRTSUVWXYZ0123456789") for _ in range(size))

def verify(fieldValue):
    return fieldValue if fieldValue else "N/A"

def prepare_response(result, error = None):
    if result:
        return jsonify(response = result)
    else:
        return jsonify(response = False, error = error if error else "resource_not_found")
    
def generate_result():
    r_a = randrange(10,21)
    r_b = randrange(10,21)
    if r_a > r_b:
        r_a = 21
    elif r_b > r_a:
        r_b = 21
    elif r_a == r_b:
        if r_a == 20 or r_a == 21:
            r_a += 2
        else:
            r_b = 21
        
    return (r_a,r_b)