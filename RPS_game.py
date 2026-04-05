def play(player1, player2, num_games, verbose=False):
    p1_prev_play = ""
    p2_prev_play = ""
    results = {"p1": 0, "p2": 0, "tie": 0}

    for _ in range(num_games):
        p1_play = player1(p2_prev_play)
        p2_play = player2(p1_prev_play)

        if p1_play == p2_play:
            results["tie"] += 1
            winner = "Tie"
        elif (p1_play == "P" and p2_play == "R") or (p1_play == "R" and p2_play == "S") or (p1_play == "S" and p2_play == "P"):
            results["p1"] += 1
            winner = "Player 1"
        elif p2_play in ["R", "P", "S"]:
            results["p2"] += 1
            winner = "Player 2"
        else:
            results["p1"] += 1
            winner = "Player 1 by default"

        if verbose:
            print(f"Player 1: {p1_play}, Player 2: {p2_play}, Winner: {winner}")

        p1_prev_play = p1_play
        p2_prev_play = p2_play

    games_won = results["p1"]
    games_lost = results["p2"]
    win_rate = games_won / num_games * 100 if num_games else 0

    if verbose:
        print("\nFinal results:", results)
        print(f"Player 1 win rate: {win_rate:.2f}%")

    return win_rate


def quincy(prev_play, counter=[0]):
    choices = ["R", "R", "P", "P", "S"]
    play = choices[counter[0] % len(choices)]
    counter[0] += 1
    return play


def kris(prev_play):
    return "P"


def mrugesh(prev_opponent_play, opponent_history=[]):
    if prev_opponent_play:
        opponent_history.append(prev_opponent_play)

    if len(opponent_history) > 2:
        recent = opponent_history[-10:]
        most_frequent = max(set(recent), key=recent.count)
        return {"P": "S", "R": "P", "S": "R"}[most_frequent]

    return "R"


def abbey(prev_opponent_play, opponent_history=[], play_order=[
    {"RRR": 0, "RRP": 0, "RRS": 0, "RPR": 0, "RPP": 0, "RPS": 0, "RSR": 0, "RSP": 0, "RSS": 0,
     "PRR": 0, "PRP": 0, "PRS": 0, "PPR": 0, "PPP": 0, "PPS": 0, "PSR": 0, "PSP": 0, "PSS": 0,
     "SRR": 0, "SRP": 0, "SRS": 0, "SPR": 0, "SPP": 0, "SPS": 0, "SSR": 0, "SSP": 0, "SSS": 0}
]):
    if prev_opponent_play:
        opponent_history.append(prev_opponent_play)

    if len(opponent_history) > 2:
        last_three = "".join(opponent_history[-3:])
        play_order[0][last_three] += 1

    prediction = "R"
    if len(opponent_history) > 1:
        last_two = "".join(opponent_history[-2:])
        potential = [last_two + "R", last_two + "P", last_two + "S"]
        sub_order = {k: play_order[0][k] for k in potential}
        prediction = max(sub_order, key=sub_order.get)[-1]

    return {"P": "S", "R": "P", "S": "R"}[prediction]
