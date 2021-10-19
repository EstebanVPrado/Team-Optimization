import pandas as pd


class Participant:
    def __init__(self, name, role, p, c):
        self.name = name
        self.role = role
        self.friends = p  # A list of the teammates that this person wants to work with
        self.c = c  # A list of scores for each challenge
        self.team = ''
        self.x = 0
        self.y = 0

    def to_string(self):
        print(self.name, self.role, self.friends, self.c)


def get_participant_by_name(participants, name):
    for participant in participants:
        if participant.name == name:
            return participant
    return None


def get_participant_index_by_name(participants, name):
    for i, participant in enumerate(participants):
        if participant.name == name:
            return i
    return None


def load_participants_from_csv(csv):

    df = pd.read_csv(csv)

    participant_num = len(df.index)

    participants = []

    for i in range(participant_num):
        name = df.iloc[i, 1]
        role = df.iloc[i, 2]

        friends = []
        for c in range(3):
            friend_name = df.iloc[i, 3 + c]
            if friend_name != "":
                friends.append(friend_name)
            else:
                friends.append(None)

        challenge_preferences = []
        for c in range(4):
            challenge_preferences.append(df.iloc[i, 6 + c])

        participants.append(Participant(name, role, friends, challenge_preferences))

    return participants

