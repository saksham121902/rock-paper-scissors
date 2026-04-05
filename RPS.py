import random
from collections import Counter, defaultdict


MOVES = ("R", "P", "S")
BEATS = {"R": "S", "P": "R", "S": "P"}
COUNTER = {"R": "P", "P": "S", "S": "R"}


def _most_common(sequence):
    counts = Counter(sequence)
    # Stable tie-break order keeps behavior deterministic.
    return max(MOVES, key=lambda m: (counts[m], -MOVES.index(m)))


def _predict_with_ngram(history, n):
    if len(history) <= n:
        return None

    key = tuple(history[-n:])
    next_counts = Counter()

    for i in range(len(history) - n):
        if tuple(history[i : i + n]) == key:
            next_counts[history[i + n]] += 1

    if not next_counts:
        return None

    return max(MOVES, key=lambda m: (next_counts[m], -MOVES.index(m)))


def _predict_quincy(turn_index):
    cycle = ("R", "R", "P", "P", "S")
    return cycle[turn_index % len(cycle)]


def _predict_kris():
    return "P"


def _predict_mrugesh(my_history):
    if len(my_history) > 2:
        most_frequent = _most_common(my_history[-10:])
        return COUNTER[most_frequent]
    return "R"


def _predict_abbey(my_history):
    # Abbey predicts our next move from our last 2 moves, then counters it.
    if len(my_history) < 2:
        predicted_our_move = "R"
        return COUNTER[predicted_our_move]

    last_two = tuple(my_history[-2:])
    continuations = Counter()

    for i in range(len(my_history) - 2):
        if tuple(my_history[i : i + 2]) == last_two:
            continuations[my_history[i + 2]] += 1

    if continuations:
        predicted_our_move = max(MOVES, key=lambda m: (continuations[m], -MOVES.index(m)))
    else:
        predicted_our_move = "R"

    return COUNTER[predicted_our_move]


def player(prev_play, state={}):
    if prev_play == "" or "initialized" not in state:
        state.clear()
        state["initialized"] = True
        state["opponent_history"] = []
        state["my_history"] = []
        state["scores"] = defaultdict(float)
        state["last_predictions"] = {}

        for name in (
            "quincy",
            "kris",
            "mrugesh",
            "abbey",
            "opp_ngram_2",
            "opp_ngram_3",
            "opp_majority",
        ):
            state["scores"][name] = 0.0

    if prev_play in MOVES:
        state["opponent_history"].append(prev_play)

        # Reward predictors that matched the opponent's actual last move.
        for name, predicted in state["last_predictions"].items():
            if predicted == prev_play:
                state["scores"][name] += 2.0
            else:
                state["scores"][name] -= 0.3

        # Slight decay to adapt to strategy changes.
        for name in state["scores"]:
            state["scores"][name] *= 0.97

    opponent_history = state["opponent_history"]
    my_history = state["my_history"]
    turn_index = len(opponent_history)

    predictions = {}
    predictions["quincy"] = _predict_quincy(turn_index)
    predictions["kris"] = _predict_kris()
    predictions["mrugesh"] = _predict_mrugesh(my_history)
    predictions["abbey"] = _predict_abbey(my_history)

    p2 = _predict_with_ngram(opponent_history, 2)
    p3 = _predict_with_ngram(opponent_history, 3)
    predictions["opp_ngram_2"] = p2 if p2 else random.choice(MOVES)
    predictions["opp_ngram_3"] = p3 if p3 else random.choice(MOVES)

    if opponent_history:
        predictions["opp_majority"] = _most_common(opponent_history)
    else:
        predictions["opp_majority"] = random.choice(MOVES)

    state["last_predictions"] = predictions

    # Pick the predictor with best running score.
    best_model = max(predictions, key=lambda name: state["scores"][name])
    predicted_opponent_move = predictions[best_model]

    # Beat the predicted opponent move.
    move = COUNTER[predicted_opponent_move]

    state["my_history"].append(move)
    return move
