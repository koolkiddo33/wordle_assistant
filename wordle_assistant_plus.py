"""
Brayden Taylor
Wordle Assistant Plus
April 2022
"""

import re
import os
import time

os.system("")

file = open("five_letter_words.txt")
txt = file.read().split("\",\"")
file.close()
txt.sort()

with open("possible_answers.txt", "r") as reader:
    possible_answers = reader.read().split("\",\"")
    reader.close()

print("\033[0;36;48mWelcome to Wordle Assistant Plus v1.04")
print("Coded by Brayden Taylor")
print("Last updated April 2022")
print()
print("\033[0;37;48mThe Wordle Assistant is a device used to help you solve Wordles by giving you words that are possible answers and words that give you the most info.")
print("An example entry where the word is \"apple\" may look something like this: ")
print("\033[0;37;48m----------")
print("\033[1;32;48mGreen letters (other letters represented by \"-\"): \033[1;37;48ma-p-e")
print("\033[1;33;48mYellow letters (seperated by \" \"): \033[1;37;48ml")
print("\033[1;33;48mPosition(s) of yellow \"l\": \033[1;37;48m1 2")
print("\033[1;30;48mBlack letters (seperated by \" \"): \033[1;37;48mr o s")
print("\033[0;37;48m----------")
print("Note: You must input ALL of the info, not just the latest word that you guessed. (If a yellow letter's position is revealed (turns green) you may omit its entry)")
print()

while True:
    raw_user_green = (input("\033[1;32;48mGreen letters (other letters represented by \"-\"): ")).lower()
    if len(raw_user_green) != 5 and raw_user_green != "":
        print("Incorrect number of characters")
        continue
    rez = []
    all_green_pos = []
    i = 0
    for letter in raw_user_green:
        rez.append((letter, i))
        if letter != "-":
            all_green_pos.append(i)
        i += 1
    user_green = rez
    # Check for correct input
    user_yellow = input("\033[1;33;48mYellow letters (seperated by \" \"): ").lower().split(" ")
    if user_yellow == [""]:
        user_yellow = []
    # I could get the positions of user_yellow by asking the user for the 
    # position(s) of each letter if user_yellow is given Worked!
    if len(user_yellow) > 0:
        user_yellow_0 = (user_yellow[0], input("Position(s) of yellow \"" + user_yellow[0][0] + "\": ").split(" "))
        user_yellow[0] = user_yellow_0
    if len(user_yellow) > 1:
        user_yellow_1 = (user_yellow[1], input("Position(s) of yellow \"" + user_yellow[1][0] + "\": ").split(" "))
        user_yellow[1] = user_yellow_1
    if len(user_yellow) > 2:
        user_yellow_2 = (user_yellow[2], input("Position(s) of yellow \"" + user_yellow[2][0] + "\": ").split(" "))
        user_yellow[2] = user_yellow_2
    if len(user_yellow) > 3:
        user_yellow_3 = (user_yellow[3], input("Position(s) of yellow \"" + user_yellow[3][0] + "\": ").split(" "))
        user_yellow[3] = user_yellow_3
    if len(user_yellow) > 4:
        user_yellow_4 = (user_yellow[4], input("Position(s) of \"" + user_yellow[4][0] + "\": ").split(" "))
        user_yellow[4] = user_yellow_4
    user_black = input("\033[1;30;48mBlack letters (seperated by \" \"): ").lower().split(" ")
    print("\033[0;37;48mProcessing...")
    letter_index = 0
    for letter in user_black:
        for tup in user_yellow:
            if letter in raw_user_green or letter in tup:
                user_black = user_black[:letter_index] + user_black[letter_index + 1:]
        letter_index += 1

    matching_words = []
    for word in txt:
        matching_words.append(word)

    if user_yellow != []:
        word_index = 0
        for word in matching_words:
            word_copy = word
            for letter in user_yellow:
                i = 0
                for letter2 in word_copy:
                    if letter[0] == letter2:
                        word_copy = word_copy[:i] + word_copy[i + 1:]
                        i -= 1
                        break
                    i += 1
            if len(word_copy) != 5 - len(user_yellow):
                matching_words = matching_words[:word_index] + matching_words[word_index + 1:]
                word_index -= 1
            word_index += 1
        
        # BUG: If a letter is yellow and it is in the position of a green letter,
        # it's informational value should be 0
        # SOLUTION?: Set the position of every yellow letter if there's a green letter
        # Search if the yellow already has the position, if not append the pos
        # If yellow letter in green letters, remove yellow letter Worked!
        user_green_stripped = []
        for letter in raw_user_green:
            if letter != "-":
                user_green_stripped.append(letter)
        tup_index = 0
        for tup in user_yellow:
            if tup[0] in user_green_stripped:
                user_yellow = user_yellow[:tup_index] + user_yellow[tup_index + 1:]
                tup_index -= 1
            for pos in all_green_pos:
                for letter in user_green_stripped:
                    if str(pos + 1) not in tup[1] and tup[0] != letter:
                        tup[1].append(str(pos + 1))
            tup_index += 1
        
        word_index = 0
        for word in matching_words:
            word_tuple = []
            i = 0
            for letter in word:
                word_tuple.append((letter, i))
                i += 1
            i = 0
            break_out_flag = False
            for letter in user_yellow:
                if break_out_flag:
                    break
                for pos in letter[1]:
                    pos = int(pos)
                    if break_out_flag:
                        break
                    for letter2 in word_tuple:
                        if (letter[0], pos) == (letter2[0], int(letter2[1] + 1)):
                            matching_words = matching_words[:word_index] + matching_words[word_index + 1:]
                            word_index -= 1
                            break_out_flag = True
                            break
            word_index += 1
    print("17% Processed Yellow", end="\r")
    
    if user_black != [""]:
        word_index = 0
        for word in matching_words:
            for letter in user_black:
                match = re.search(letter, word)
                if match:
                    matching_words = matching_words[:word_index] + matching_words[word_index + 1:]
                    word_index -= 1
                    break
            word_index += 1
    print("33% Processed Black", end="\r")
    
    pre_green_matching_words = matching_words
    
    if user_green != "":
        word_index = 0
        for word in matching_words:
            word_tuple = []
            i = 0
            for letter in word:
                word_tuple.append((letter, i))
                i += 1
            i = 0
            for tup in user_green:
                if tup[0] == "-":
                    i += 1
                    continue
                if tup != word_tuple[i]:
                    matching_words = matching_words[:word_index] + matching_words[word_index + 1:]
                    word_index -= 1
                    break
                i += 1
            word_index += 1
    print("50% Processed Green", end="\r")
    
    # OPTIMIZATION: remove the non 5 letter words from the csv and
    # access that so it doesn't have to every time Worked? Can't really tell the diff :/
    
    # Consider using a dif list:
    # https://www.wordfrequency.info/samples.asp
        # https://www.wordfrequency.info/files/entriesWithoutCollocates.txt
        # https://www.wordfrequency.info/samples/words_219k.txt
    # vvvvv
    # https://raw.githubusercontent.com/IlyaSemenov/wikipedia-word-frequency/master/results/enwiki-20190320-words-frequency.txt
        # https://github.com/IlyaSemenov/wikipedia-word-frequency/blob/master/results/enwiki-20210820-words-frequency.txt
    # ^^^^^ This one seems good
    # I could combine multiple lists and average them to get the most complete set?
    
    most_frequent_words_all = []
    f = open("freq_five_letters_2.txt", "r")
    for line in f:
        line = line.strip("\n")
        most_frequent_words_all.append((line[:5], line[6:]))
    f.close()
    
    most_frequent_words = []
    for tup in most_frequent_words_all:
        if tup[0] in matching_words:
            most_frequent_words.append(tup)
    print("67% Created Most Common Words", end="\r")
    
    # Most frequent letters in matching words using a list of tuples
    most_frequent_letters = [("a", 0), ("b", 0), ("c", 0), ("d", 0), ("e", 0), ("f", 0), ("g", 0), ("h", 0), ("i", 0), ("j", 0), ("k", 0), ("l", 0), ("m", 0), \
                             ("n", 0), ("o", 0), ("p", 0), ("q", 0), ("r", 0), ("s", 0), ("t", 0), ("u", 0), ("v", 0), ("w", 0), ("x", 0), ("y", 0), ("z", 0)]
    for word in matching_words:
        for letter in word:
            if letter in raw_user_green or letter in user_yellow:
                continue
            if letter == "a":
                most_frequent_letters[0] = (most_frequent_letters[0][0], most_frequent_letters[0][1] + 1)
            if letter == "b":
                most_frequent_letters[1] = (most_frequent_letters[1][0], most_frequent_letters[1][1] + 1)
            if letter == "c":
                most_frequent_letters[2] = (most_frequent_letters[2][0], most_frequent_letters[2][1] + 1)
            if letter == "d":
                most_frequent_letters[3] = (most_frequent_letters[3][0], most_frequent_letters[3][1] + 1)
            if letter == "e":
                most_frequent_letters[4] = (most_frequent_letters[4][0], most_frequent_letters[4][1] + 1)
            if letter == "f":
                most_frequent_letters[5] = (most_frequent_letters[5][0], most_frequent_letters[5][1] + 1)
            if letter == "g":
                most_frequent_letters[6] = (most_frequent_letters[6][0], most_frequent_letters[6][1] + 1)
            if letter == "h":
                most_frequent_letters[7] = (most_frequent_letters[7][0], most_frequent_letters[7][1] + 1)
            if letter == "i":
                most_frequent_letters[8] = (most_frequent_letters[8][0], most_frequent_letters[8][1] + 1)
            if letter == "j":
                most_frequent_letters[9] = (most_frequent_letters[9][0], most_frequent_letters[9][1] + 1)
            if letter == "k":
                most_frequent_letters[10] = (most_frequent_letters[10][0], most_frequent_letters[10][1] + 1)
            if letter == "l":
                most_frequent_letters[11] = (most_frequent_letters[11][0], most_frequent_letters[11][1] + 1)
            if letter == "m":
                most_frequent_letters[12] = (most_frequent_letters[12][0], most_frequent_letters[12][1] + 1)
            if letter == "n":
                most_frequent_letters[13] = (most_frequent_letters[13][0], most_frequent_letters[13][1] + 1)
            if letter == "o":
                most_frequent_letters[14] = (most_frequent_letters[14][0], most_frequent_letters[14][1] + 1)
            if letter == "p":
                most_frequent_letters[15] = (most_frequent_letters[15][0], most_frequent_letters[15][1] + 1)
            if letter == "q":
                most_frequent_letters[16] = (most_frequent_letters[16][0], most_frequent_letters[16][1] + 1)
            if letter == "r":
                most_frequent_letters[17] = (most_frequent_letters[17][0], most_frequent_letters[17][1] + 1)
            if letter == "s":
                most_frequent_letters[18] = (most_frequent_letters[18][0], most_frequent_letters[18][1] + 1)
            if letter == "t":
                most_frequent_letters[19] = (most_frequent_letters[19][0], most_frequent_letters[19][1] + 1)
            if letter == "u":
                most_frequent_letters[20] = (most_frequent_letters[20][0], most_frequent_letters[20][1] + 1)
            if letter == "v":
                most_frequent_letters[21] = (most_frequent_letters[21][0], most_frequent_letters[21][1] + 1)
            if letter == "w":
                most_frequent_letters[22] = (most_frequent_letters[22][0], most_frequent_letters[22][1] + 1)
            if letter == "x":
                most_frequent_letters[23] = (most_frequent_letters[23][0], most_frequent_letters[23][1] + 1)
            if letter == "y":
                most_frequent_letters[24] = (most_frequent_letters[24][0], most_frequent_letters[24][1] + 1)
            if letter == "z":
                most_frequent_letters[25] = (most_frequent_letters[25][0], most_frequent_letters[25][1] + 1)
                
    def most_frequent_letters_sort(tup):
        return tup[1]
    most_frequent_letters.sort(reverse=True, key=most_frequent_letters_sort)
    print("83% Created Most Frequent Letters", end="\r")

    # From that, print a word that contains the most amount of most frequent 
    # letters
    # (add all of the values of the letters for every matching word and return 
    # the highest value word?) Worked!
    # BUG: Not printing words if it has a black letter in it
    informational_words = []
    for word in pre_green_matching_words:
        frequency_score = 0
        for letter in word:
            output = list(filter(lambda x:letter in x, most_frequent_letters))
            frequency_score += output[0][1]
            if word.count(letter) > 1:
                frequency_score -= output[0][1]
        informational_words.append((word, frequency_score))
    def informational_words_sort(tup):
        return tup[1]
    informational_words.sort(reverse=True, key=informational_words_sort)
    print("100% Created Informational Words")
    
    for index, word in enumerate(most_frequent_words):
        if word[0] not in possible_answers:
            most_frequent_words = most_frequent_words[:index] + most_frequent_words[index + 1:]
            index -= 1
    
    total_freq = 0
    for word in most_frequent_words:
        freq = int(word[1])
        total_freq += freq

    most_frequent_words_stripped = []
    for word in most_frequent_words:
        most_frequent_words_stripped.append(word[0])

    print("\033[1;37;48m----------")
    print(str(len(most_frequent_words)) + " possible word(s)")
    print("----------")
    if len(most_frequent_words_stripped) < 200 and len(most_frequent_words_stripped) != 0:
        print(most_frequent_words_stripped)
        print("\n----------")
    # Consider printing the info along with the percentage
    print("10 most common words:")
    for i in range(len(most_frequent_words)):
        percentage = ((int(most_frequent_words[i][1]))*100/total_freq + 100/len(most_frequent_words))/2
        percentage = round(percentage, 2)
        print(str(i + 1) + ": " + most_frequent_words[i][0] + " (" + str(percentage) + "%)")
        if i == 9:
            break
    print("----------")
    print("10 recommended words for maximum info: ")
    for i in range(len(informational_words)):
        if informational_words[i][0] in most_frequent_words_stripped:
            print(informational_words[i][0] + " (" + str(informational_words[i][1]) + ")*")
        else:
            print(informational_words[i][0] + " (" + str(informational_words[i][1]) + ")")
        if i == 9:
            break
    print("* Possible answer")
    print()
