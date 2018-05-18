DISTANCE = 200


def check_distance():
    global DISTANCE
    DISTANCE -= 1

    if DISTANCE <= 150:
        DISTANCE = 200
        return True
    return False
