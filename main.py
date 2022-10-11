import random


def movement(position):
    """
    takes the player position, roles the dice and return new position.
    :returns:
    int position: player position
    bool double: a flag if the player got a double
    """
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    print(f"dice: ({die1},{die2})")  # checking the dice
    double = (die1 == die2)
    print("is double: ", double)  # checking the double
    position = sum((position, die1, die2))
    position = position - 40 if position >= 40 else position
    print("new position in the function: ", position)
    return position, double


def main():
    position = 0  # the player position on the board out of 40.
    double_streak = 0
    turn_counter = 0
    jail = False  # flag to know if we are in jail or just visiting jail
    for i in range(10):
        position, double = movement(position)
        # landing on go to jail
        if position == 30:
            print("landed on go to jail")
            double = False  # so we won't have another throw
            jail = True
            position = 10
        while double:
            double_streak += 1
            print("streak: ", double_streak)  # checking the double streak counter
            if double_streak == 3:
                print("go to jail because of doubles streak")
                position = 10
                jail = True
                double = False
            else:
                position, double = movement(position)
        # end of turn sequence
        double_streak = 0
        turn_counter += 1
        print("position in main:", position)
        print("end of turn")
        print("# number of turns: ", turn_counter)
        print()


if __name__ == '__main__':
    main()
