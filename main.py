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
    for i in range(10):
        position, double = movement(position)
        double_streak = double_streak + 1 if double else 0
        print("streak: ", double_streak)  # checking the double streak counter
        if double_streak == 3:
            print("You need to go to jail")
        print("position in main:", position)
        print("adding only for jail branch")

# check this
if __name__ == '__main__':
    main()
