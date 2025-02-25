


import random
random_words = ('flower','house','python','mother','church','monster')

word = random.choice(random_words)


print('Welcome to the word guessing game!')
print()

print(f'Your hint is: ', end='')
for index in range(len(word)):
    print('_ ', end='')

print()
guess = input('What is you guess? ')
count = 1
hint = []

#Fill hint with the word as an array
for i in range(len(word)):
    hint.append(word[i])

#Test it guess and word don't match
while guess.lower() != word.lower():
    #Test if same size
    if len(guess) == len(word):
        #test if same index, if exists in word or add a underscore mask
        for i in range(len(word)):
            if guess[i].lower() in word.lower():
                if word[i].lower() == guess[i].lower():
                    hint[i] = word[i].upper()
                else:
                    hint[i] = guess[i].lower()
            else:
                hint[i] = '_ '
        print()
        print(f'Your hint is: ', end='')
        for index in range(len(hint)):
            print(f'{hint[index]} ', end='')
    else :
        print()
        #Hint on the amount of characteres on the guess
        print(f'The guess must have {len(word)} characteres. Try again! ')

    print()
    count += 1
    guess = input('What is you guess? ')

 
print()
print('Congratulations! You guessed it!')
print(f'It took you {count} guesses!')