import pandas as pd
import numpy as np
import random

physics_participant_number = 8
software_participant_number = 8
business_participant_number = 4
friend_probability_threshold = 1

names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
roles = ['physics', 'business', 'software']
challenges = ['c1', 'c2', 'c3', 'c4']

if __name__ == "__main__":
    total_participants = physics_participant_number + software_participant_number + business_participant_number
    # total_participants = 2

    participants = np.full((total_participants, 10), "", dtype=np.dtype('U100'))

    for i in range(total_participants):

        # Name
        name = names[i]

        # Role
        if i < 8:
            role = 'physics'
        elif i < 16:
            role = 'business'
        else:
            role = 'software'

        # Teammate Preference
        other_names = names[:total_participants].copy()
        other_names.remove(name)
        random.shuffle(other_names)
        friends = other_names[:3]

        # Challenge Preference
        c = np.random.randint(5, size=4) + 1

        participants[i] = ["-", name, role, friends[0], friends[1], friends[2], c[0], c[1], c[2], c[3]]

    df = pd.DataFrame(participants, columns=['timestamp', 'name', 'role', 'p1', 'p2', 'p3', 'c1', 'c2', 'c3', 'c4'])
    df.to_csv('dummy_data.csv', index=False, na_rep='Unknown')
    print(df)
