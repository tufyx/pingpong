from random import shuffle
from math import ceil, log, pow
from time import time

def build_knockout(players):
    
    shuffle(players)
    p_count = len(players)
    max_size = int(ceil(log(p_count, 2)))
    players.extend([-1] * (int(pow(2, max_size)) - p_count))

    half = len(players) / 2
    seed1 = players[0:half]
    seed2 = players[half:]

    matches = []
    stage = 1
    competition_id = "K_" + str(int(round(time())))
    for (index, _) in enumerate(seed1):
        match_id = competition_id + "_" + str(len(matches) + 1)
        matches.append((competition_id, match_id, seed1[index], seed2[index], stage))

    shuffle(matches)
    stage += 1
    matches = build_pyramid(competition_id, matches, stage)
    return matches


def build_pyramid(competition_id, matches, stage):
    current_round = [match for match in matches if match[4] == stage-1]
    next_round = []
    for match_index in range(0, len(current_round), 2):
        match_id = competition_id + "_" + str(len(matches) + len(next_round) + 1)
        next_round.append((competition_id, match_id, current_round[match_index][1], current_round[match_index+1][1], stage))
    new_matches_count = len(next_round)
    all_matches = matches + next_round
    if new_matches_count > 1:
        stage += 1
        return build_pyramid(competition_id, all_matches, stage)
    else:
        return all_matches


def print_matches(matches):
    current_round = -1
    for match in matches:
        if match[4] > current_round:
            current_round = match[4]
            print "-------------"
            print "ROUND ", current_round
        print match