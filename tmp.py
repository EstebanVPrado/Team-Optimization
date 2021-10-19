import math
import cairo
import Participant
from PIL import Image
import numpy as np
import random

if __name__ == "__main__":
    participants = Participant.load_participants_from_csv('dummy_data.csv')

    participants[0].to_string()

    for friend in participants[0].friends:
        if isinstance(friend, str):
            print(friend)