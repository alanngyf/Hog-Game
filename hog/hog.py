"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100 # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################

# Taking turns

def roll_dice(num_rolls, dice=six_sided):
    """Roll DICE for NUM_ROLLS times.  Return either the sum of the outcomes,
    or 1 if a 1 is rolled (Pig out). This calls DICE exactly NUM_ROLLS times.

    num_rolls:  The number of dice rolls that will be made; at least 1.
    dice:       A zero-argument function that returns an integer outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    "*** YOUR CODE HERE ***"
    i = num_rolls
    score = 0
    pigout = 0
    while i > 0:
        die = dice()
        score += die
        i-=1
        if die == 1:
            pigout = 1
    if pigout == 1:
        return 1
    else:
        return score


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    "*** YOUR CODE HERE ***"
    score = 0 
    ##Free Bacon Rule
    if num_rolls == 0:
        a = (opponent_score - opponent_score % 10) // 10
        b = opponent_score % 10
        return 1 + max(a,b)
    return roll_dice(num_rolls, dice)


# Playing a game

def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    """
    "*** YOUR CODE HERE ***"
    ##Hog Wild Rule
    if (score + opponent_score) % 7 == 0: 
        return four_sided
    else: 
        return six_sided

def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who

def play(strategy0, strategy1, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    """
    who = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    score0, score1 = 0, 0
    while (score0 < goal and score1 < goal): 
        if who == 0: 
            num_of_dice = strategy0(score0, score1)
            score0 += take_turn(num_of_dice, score1, select_dice(score0, score1))
        else: 
            num_of_dice = strategy1(score1, score0)
            score1 += take_turn(num_of_dice, score0, select_dice(score1, score0))
        if (score0 == 2*score1) or (2*score0 == score1): #Swine swap
            score0, score1 = score1, score0
        who = other(who) #Switch to player0
    return score0, score1  # You may wish to change this line.

#######################
# Phase 2: Strategies #
#######################

# Basic Strategy


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy

# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    6.0

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 1.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 6.0.
    """
    "*** YOUR CODE HERE ***"
    def avg(*args): 
        i = num_samples
        total = 0
        while (i > 0):
            total += fn(*args)
            i -= 1
        return total / num_samples
    return avg

def max_scoring_num_rolls(dice=six_sided):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE.  Print all averages as in
    the doctest below.  Assume that dice always returns positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    1 dice scores 3.0 on average
    2 dice scores 6.0 on average
    3 dice scores 9.0 on average
    4 dice scores 12.0 on average
    5 dice scores 15.0 on average
    6 dice scores 18.0 on average
    7 dice scores 21.0 on average
    8 dice scores 24.0 on average
    9 dice scores 27.0 on average
    10 dice scores 30.0 on average
    10
    """
    "*** YOUR CODE HERE ***"
    i = 1
    avg_score = 0
    averaged_dice = make_averaged(roll_dice)
    while i < 11:
        exp_score = averaged_dice(i, dice)
        if exp_score > avg_score:
            avg_score = exp_score
            max_num = i
        i += 1
    return max_num


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1

def average_win_rate(strategy, baseline=always_roll(5)):
    """Return the average win rate (0 to 1) of STRATEGY against BASELINE."""
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)
    return (win_rate_as_player_0 + win_rate_as_player_1) / 2 # Average results

def run_experiments():
    """Run a series of strategy experiments and report results."""
    if False: # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False: # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False: # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False: # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if True: # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"

# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    "*** YOUR CODE HERE ***"
    a = (opponent_score - opponent_score % 10) // 10
    b = opponent_score % 10
    if margin <= 1 + max(a,b):
        return 0
    else:
        return num_rolls


def swap_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice when it would result in a beneficial swap and
    rolls NUM_ROLLS if it would result in a harmful swap. It also rolls
    0 dice if that gives at least MARGIN points and rolls
    NUM_ROLLS otherwise.
    """
    "*** YOUR CODE HERE ***"
    tens = opponent_score // 10
    ones = opponent_score % 10
    if ((2 * (score + 1 + max(tens,ones))) == opponent_score):
        return 0
    elif ((score + 1 + max(tens,ones)) == (2 * opponent_score)):
        return num_rolls
    elif (margin <= 1 + max(tens,ones)):
        return 0
    else:
        return num_rolls


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.
    do not roll zero dice if it results harmful swap    
    roll zero dice if i end up score greater or equal to 100 in the case you do not result a harmful swap after it; 
    roll zero dice if it results benefical swap
    roll zero dice if it results sum of score and opponent_score can be divied by 7 after adding the value to score
    do not roll zero dice if your opponent is able to roll zero dice to leave you four sided dice to use
    if leading, we can choose margin value 8 over 4 rolls (taking less risk than your opponent)
    if losing, we wanna roll more than 5 rolls, say 6, if we r not making margin value 10 or better (taking more risk)
    """
    "*** YOUR CODE HERE ***"
    a = (opponent_score - opponent_score % 10)//10
    b = opponent_score % 10
    zero_add = max(a,b) + 1
    c = ((score+zero_add) -  ((score+zero_add)%10))//10
    d = (score+zero_add) % 10
    op_zero_add = max(c,d) + 1
    zero_win = (score+zero_add) >= GOAL_SCORE
    benef_swap = ((2 * (score + zero_add)) == opponent_score) or ((2*score + zero_add) == opponent_score+zero_add)
    harm_swap = (((score+zero_add) == (2*opponent_score)) or ((score+zero_add) == (2*(opponent_score+op_zero_add))))
    benef_hogwild = ((score+zero_add+opponent_score)%7 == 0)
    harm_hogwild = ((score+zero_add+opponent_score+op_zero_add)%7 == 0)
    e = (score - score % 10)//10
    f = score % 10
    zero_add_op = max(e,f) + 1
    if harm_swap:
        return 5
    elif zero_win or benef_swap:
        return 0 
    elif harm_hogwild:
        return 4
    elif benef_hogwild:
        return 0
    elif score > opponent_score:
        return bacon_strategy(score, opponent_score, 8, 4)  
    elif score < opponent_score:
        return bacon_strategy(score, opponent_score, 10, 6)   
    else:
        return bacon_strategy(score, opponent_score, 8, 5)




##########################
# Command Line Interface #
##########################

# Note: Functions in this section do not need to be changed.  They use features
#       of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')
    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
