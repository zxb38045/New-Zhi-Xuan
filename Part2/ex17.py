# TODO: Refer to the objective and sample output and figure out your own code!
# Time to graduate :p

import random

#Ask for users' name
name = input("What is your name? ")

#List of random ajectives and animals for codename generation
adjectives = ['Covert'
    , 'Stealthy'
    , 'Surrepititious'
    , 'Sneaky'
    , 'Confidential'
    , 'Secretive']
animals = ['Pigeon'
    , 'Catfish'
    , 'Octopus'
    , 'Owl'
    , 'Squirrel']

#Print the codename
print(name 
    + ", your codename is: " 
    + (random.choice(adjectives) ) 
    + " " 
    + (random.choice(animals))
    )

#Print the users' lucker number
print("Your lucky number is: " + str(random.randint(0,100)))
