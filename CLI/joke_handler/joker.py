import random
import time


def joke_returner():
    '''
    Function for returning unique jokes. Not the same joke twice, that's for sure!
    '''

    jokelist = joke_lister()

    while True:
        choice = input("\nWould you like a [1] Safe For Work-, a [2] Punny- or a [3] Your Mama-joke? Press [Q] to quit: >")

        if choice == "1" and len(jokelist["SFW"]) > 0:
            told_joke = jokelist["SFW"].pop(random.randint(0, (len(jokelist["SFW"])-1 )))
            print(told_joke)
            time.sleep(2)

        elif choice == "2" and len(jokelist["Punny"]) > 0:
            told_joke = jokelist["Punny"].pop(random.randint(0, (len(jokelist["Punny"])-1 )))
            print(told_joke)
            time.sleep(2)
        
        elif choice == "3" and len(jokelist["YourMom"]) > 0:
            told_joke = jokelist["YourMom"].pop(random.randint(0, (len(jokelist["YourMom"])-1 )))
            print(told_joke)
            time.sleep(2)

        elif choice == "q" or choice == "Q":
            break

        else:
            print("No joke available.")
            time.sleep(2)
            pass

def joke_lister():
    '''
    The function that contains our joke material
    '''

    init_jokes = {
        "SFW": ["What's the difference between a boss and an employee? The boss is always right.", "Get back to work."],
        "Punny": ["What do you do with the cake at an orc birthday party? You start goblin it up."],
        "YourMom": ["Your mom is so shallow, she probably thinks this quip is about her.", "Your mom is so sensitive, I wouldn't want to hurt her.", "Your mom is so exhilarating, we call her a theme park."],
    }

    return init_jokes
    