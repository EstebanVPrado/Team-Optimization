import numpy as np
import random
import Participant
import matplotlib.pyplot as plt


def kronecker_delta(a, b):
    if a == b:
        return 1
    else:
        return 0


def penalty_total(participants, pairs, u):
    # pen({Ci})
    penalty_c = 0

    for k, participant in enumerate(participants):
        challenge_dissatisfaction = (5 - participant.c[u[k]])^2

        partner_dissatisfaction = 1
        for p_name in participant.friends:
            p_index = Participant.get_participant_index_by_name(participants, p_name)
            partner_dissatisfaction *= 2**(1-kronecker_delta(u[p_index], u[k]))

        penalty_c += challenge_dissatisfaction + partner_dissatisfaction

    # pen({Ci})
    penalty_pairs = 0

    for pair in pairs:
        p_index_1 = Participant.get_participant_index_by_name(participants, pair[0])
        p_index_2 = Participant.get_participant_index_by_name(participants, pair[1])
        penalty_pairs += 9*(1-kronecker_delta(u[p_index_1], u[p_index_2]))

    # pentot(~u)
    penalty_total = penalty_c + penalty_c

    return penalty_total


def shuffle(array):
    a = array.copy()
    random.shuffle(a)
    return a


def find_pairs(participants):
    # Finding Pairs:
    pairs = []  # Pairs of people who mutually indicated they want to work together
    for participant in participants:
        for p_name in participant.friends:
            p = Participant.get_participant_by_name(participants, p_name)
            if participant.name in p.friends:
                pair = [participant.name, p_name]
                pair.sort()
                if pair not in pairs:
                    pairs.append(pair)
    return pairs


def generate_random_u():
    u = np.zeros(20, dtype=int)
    u[:8] = shuffle([0, 1, 2, 3, 0, 1, 2, 3])
    u[8:16] = shuffle([0, 1, 2, 3, 0, 1, 2, 3])
    u[16:] = shuffle([0, 1, 2, 3])
    return u


def random_swap(arr, idx_range):
    pair_to_swap = shuffle(list(range(idx_range[0], idx_range[1])))[:2]
    idx1, idx2 = pair_to_swap[0], pair_to_swap[1]
    arr[idx1], arr[idx2] = arr[idx2], arr[idx1]
    return arr


# Each column of the Matrix constellation represents a vector n_k
def generate_n(u):
    N = np.tile(u, (20, 1))

    for k in range(4):
        N[k] = random_swap(u, [0, 8])
    for k in range(4):
        N[k+8] = random_swap(u, [8, 16])
    for k in range(4):
        N[k+16] = random_swap(u, [16, 20])

    return N


def optimize(participants, pairs, starting_vector):
    penalties = []

    local_optimum = starting_vector
    for i in range(100):
        N = generate_n(local_optimum)

        penalty = [penalty_total(participants, pairs, nk) for nk in N]
        mp_min_idx = np.argmin(penalty)
        penalty = penalty[mp_min_idx]

        cp = penalty_total(participants, pairs, local_optimum)

        if penalty <= cp:
            local_optimum = N[mp_min_idx]
            penalties.append(penalty)

    return local_optimum, penalties


if __name__ == "__main__":

    participants = Participant.load_participants_from_csv('dummy_data.csv')
    pairs = find_pairs(participants)

    plt.figure(figsize=(22, 10), dpi=80)

    optima = []
    final_penalties = []
    for i in range(10):
        plt.subplot(2, 5, i + 1)
        plt.xlabel('iteration', fontsize=10)
        plt.ylabel('penalty', fontsize=10)

        starting_vector = generate_random_u()
        local_optimum, penalties = optimize(participants, pairs, starting_vector)
        optima.append(local_optimum)
        final_penalties.append(penalties[-1])

        plt.title('Min. Penalty:' + str(penalties[-1]))
        plt.plot(penalties)

    optimum = optima[np.argmin(final_penalties)]
    print(optimum)

    plt.show()






