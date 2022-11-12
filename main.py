import random
from tqdm import tqdm

"""
general assumptions:
1) only one person goes across the board
1) if you get to jail after a double you don't get another throw of dice
2) every time you have a get out of jail free card you will use it
3) you use the chance card before the community chest card
4) for now, you don't pay to get out of jail early
5) when the chance/cc deck is empty we shuffle it again
"""


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


def chance(position: int, chance_list: list, goj: bool):
    # dictionary of chance cards:
    chance_dict = {
        1: "Advance to boardwalk",
        2: "Advance to go (Collect $200)",
        3: 'Advance to Illinois Avenue. If you pass Go collect $200',
        4: 'Advance to St. Charles Place. If you pass Go, collect $200',
        5: 'Advance to the nearest Railroad. If unowned, you may buy it from the Bank. If owned, pay wonder twice the '
           'rental to which they are otherwise entitled',
        6: 'Advance to the nearest Railroad. If unowned, you may buy it from the Bank. If owned, pay wonder twice the '
           'rental to which they are otherwise entitled',
        7: 'Advance token to nearest Utility. If unowned, you may buy it from the Bank. If owned, throw dice and pay '
           'owner a total ten times amount thrown.',
        8: 'Bank pays you dividend of %50',
        9: 'Get out of Jail Free',
        10: 'Go Back 3 Spaces',
        11: 'Go to Jail. Go directly to Jail, do not pass Go, do not collects $200',
        12: 'Make general repairs on all your property. For each house pay $25. For each hotel pay $100',
        13: 'Speeding fine $15',
        14: 'Take a trip to Reading Railroad. If your pass Go, collect $200',
        15: 'You have been elected Chairman of the Board. Pay each player $50',
        16: 'Your building loan matures. Collect $150'
    }
    collect = False
    jail = False
    # resetting the chance list when it is empty
    if len(chance_list) == 0:
        print('There are no more chance card, we will reshuffle the deck')
        chance_list = [n for n in range(1, 17)]
        if goj:
            chance_list.remove(9)

    card = random.choice(chance_list)
    print(card, ':', chance_dict[card])
    chance_list.remove(card)
    if card in [8, 12, 13, 15, 16]:
        print("no action taken")
    elif card == 9:
        print("you get a get out of jail free card")
        goj = True
    elif card == 1:
        position = 39
        print('moved to boardwalk')
    elif card == 2:
        position = 0
        print('moved to go')
    elif card == 3:
        if position > 24:
            collect = True
        position = 24
        print("you moved to Illinois avenue")
    elif card == 4:
        if position > 11:
            collect = True
        position = 11
        print("you moved to St.Charles Place")
    elif card in [5, 6]:
        if position == 7:
            position = 15
            print("you moved to Pensylvania Railroad")
        elif position == 22:
            position = 25
            print('You moved to B&O Railroad')
        elif position == 36:
            position = 5
            print("You moved to Reading railroad")
        else:
            print('Error you are not on a chance')
    elif card == 7:
        if position in [7, 36]:
            position = 12
            print('You moved to Electric Company')
        elif position == 22:
            position = 28
            print("You moved to Water Works")
    elif card == 10:
        position = position - 3
        if position == 4:
            print('To bad! You moved to Income tax')
        elif position == 33:
            print('You moved to community chest!')
        elif position == 19:
            print('You moved to New York Avenue')
        else:
            print('Error! wrong position')
    elif card == 11:
        print('Oh no! you went to jail')
        jail = True
        position = 10
    elif card == 14:
        collect = True
        position = 5
        print('You moved to Reading Railroad')

    if collect:
        print("you collect money")
    print(f'{chance_list = } in function')

    return position, chance_list, goj, jail


def main():
    # initializing variables
    position = 0  # the player position on the board out of 40.
    double_streak = 0
    turn_counter = 0
    jail = False  # flag to know if we are in jail or just visiting jail
    jail_count = 0
    chance_goj = False  # does the player have a get out of jail card
    cc_goj = False  # community chest get out of jail card
    chance_list = [n for n in range(1, 17)]
    print("chance list: ", chance_list)

    # playing 10 turns
    for i in tqdm(range(10), desc="player turns", colour='blue'):
        if chance_goj and jail:
            print("You used the get out of jail card")
            jail_count = 0
            jail = False
            chance_goj = False

        if jail:
            position = 10  # to make sure that the player is in the jail position
            # playing if the player is in jail
            # in the future i need to add the option of the player paid to get out of the jail.
            jail_count += 1  # the number of consecutive turn in jail.
            print(f'you are {jail_count} turns in jail')
            die1 = random.randint(1, 6)
            die2 = random.randint(1, 6)
            print(f'you got {die1}, {die2}')
            double = (die1 == die2)
            if double:
                print("double! you get out of jail")
                position = sum((position, die1, die2))
                jail_count = 0
                jail = False
            elif jail_count == 3:
                # it is a different 'if' statement so in the future i will be able to add the money factor to the game.
                print("you pay the fine and get out of jail")
                position = sum((position, die1, die2))
                jail_count = 0
                jail = False

        else:
            # normal turn (not in jail)
            position, double = movement(position)
            # landing on go to jail
            if position == 30:
                print("landed on go to jail")
                double = False  # so we won't have another throw
                jail = True
                position = 10
            # landing on chance card
            if position in [7, 22, 36]:
                print("You get a chance card")
                position, chance_list, chance_goj, jail = chance(position, chance_list, chance_goj)
                if jail:
                    double = False  # so if i go to jail and have a double i won't play a double
            # playing the double rule
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
        print(f'{chance_list=} in main')
        print("end of turn")
        print("# number of turns: ", turn_counter)
        print()


if __name__ == '__main__':
    main()
