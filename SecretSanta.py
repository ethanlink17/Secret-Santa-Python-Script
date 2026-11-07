import random
import time
import pathlib

#########################################################
#                                                       #
# SecretSanta.py                                        #
#                                                       #
# Script for randomly generating Secret Santa           #
# matches for a family, with a number of                #
# conditions added to ensure quality of output          #
#                                                       #
# Revision History:                                     #
# 11/24/2025: Link - Initial revision                   #
# 10/24/2026: Link - Adding check for previous year     #
#                                                       #
#########################################################

# Used to output data for this year's matches, as well as making sure
# we don't match last year's matches
current_year = 2026
current_year_str = str(current_year)

# Make a folder for this year's data (if it doesn't already exist)
dir_path = pathlib.Path(current_year_str + "/emails/")
dir_path.mkdir(parents=True, exist_ok=True)

dir_path = pathlib.Path(current_year_str + "/matches/")
dir_path.mkdir(parents=True, exist_ok=True)

# Initialize a dictionary to hold all the matches, and a list of the participant names
matches = {"Mark":"", "Kyra":"", "Bronte":"", "Renee":"", "Eva":"", "Isaac":"", "Ethan":""}

# It's helpful to have the names in a list
santas = list( matches.keys() )

# Initialize the lists to hold the matches
num_of_santas = len(santas)
nums1 = [0] * num_of_santas
nums2 = [0] * num_of_santas

# Initialize the lists to hold last's years matches
prevNums1 = [0] * len(santas)
prevNums2 = [0] * len(santas)

# Matches work based on the index numbers in the nums1 and nums2 lists, here are the indexes for each person
# Mark   0 
# Kyra   1
# Bronte 2
# Renee  3
# Eva    4
# Isaac  5
# Ethan  6

# When talking about pairs, using a dictionary makes sense to hold "bad matches"
# Bad matches are essentially couples (people we don't want matches up as
# part of this game), but if people had multiple bad matches this dictionary may need
# to be modified to use strings as values instead of ints. Future problem :)
bad_matches = {0:1, 1:0, 2:3, 3:2, 4:6, 6:4}

# Randomly generate matches for everyone
# Brute force method, not efficient but simple
def matchy_matchy():
    
    for i in range(0, num_of_santas):
        while(True):
            temp1 = random.randint(0, num_of_santas - 1)
            temp2 = random.randint(0, num_of_santas - 1)
            if( (temp1 != i) and (temp2 != i) and (temp1 != temp2)):
                nums1[i] = temp1
                nums2[i] = temp2
                break

# This function does some file operations to makes read in last years matches 
# from a folder `./<prev year>/matches/`, and recreates a dictionary of the same
# structure that gets creates from the `matchy_matchy()` function.
#
# This way, we can make sure that the generated matches aren't the same as the
# previous year
#
# NOTE: I haven't tested what might happen if the Santa list is different than the 
# previous year, it probably has an issue but that's another future problem to figure
# out :)
def getLastYearsMatches():
    
    #  For each Santa, read last year's matches from a file located at
    # `./<prev year>/matches/<Santa>.txt`
    for i in range(0, num_of_santas):
        with open( "./" + str(current_year - 1) + "/matches/" +  santas[i] + ".txt", "r") as f:
            lines = f.readlines()
            for j in range(0, num_of_santas):
                if( lines[0].strip() == santas[j]):
                    prevNums1[i] = j
                elif( lines[1].strip() == santas[j]):
                    prevNums2[i] = j


# This is the main function, ensures that matches are quality by checking
# a variety of conditions
def verify_matches():
    match_good = True
    num_of_matches = [0] * num_of_santas

    # Count up how many times everyone got matched
    for i in range(0, num_of_santas):
        num_of_matches[ nums1[i] ] += 1
        num_of_matches[ nums2[i] ] += 1

    # Make sure everyone got matched exactly twice
    for i in range(0, num_of_santas):
        if num_of_matches[i] != 2:
            match_good = False

        # Make sure that couples don't get gifts for their partners
        # Need to make sure you don't try to find keys that aren't in the dictionary
        # aka people who don't have bad matches
        if i in bad_matches:
            if (bad_matches[i] == nums1[i]) or (bad_matches[i] == nums2[i]):
                match_good = False

        # Make sure that a person doesn't get gifts for both people in a couple
        # Again, need to make sure you don't get a KeyError
        #if nums1[i] in bad_matches:
        #    if (bad_matches[ nums1[i] ] == nums2[i] ):
        #         match_good = False

        # Make sure that 2 people don't have the same matches
        for j in range(i+1,num_of_santas):
            if ((nums1[i] == nums1[j]) and (nums2[i] == nums2[j])) or ((nums1[i] == nums2[j]) and (nums2[i] == nums1[j])):
                match_good = False

        # Check if both of last year's matches are the same as this year's
        for i in range(0, num_of_santas):
            match1 = (nums1[i] == prevNums1[i]) or (nums1[i] == prevNums2[i])
            match2 = (nums2[i] == prevNums1[i]) or (nums2[i] == prevNums2[i])

            # If only 1 is the same, it's probably fine
            if (match1 and match2):
                match_good = False

    return match_good


# Main program execution starts here
print("=======================================")
print("Welcome to the Secret Santa Randomizer!")
print("=======================================")

print("Here are my participants: \r\n")
for i in range(0,num_of_santas):
    print( santas[i] )

# Empty print to make the output look right
print()


print("=======================================")
print("Press ENTER to start the matching!")
print("=======================================")
input()

counter = 0;

# Pre-read last's year's matches into a global
getLastYearsMatches()

# Generate a match, check whether it's quality
# If not, try again
# Keep count how many attempts it takes
while(True):
    counter += 1
    matchy_matchy()
    done = verify_matches()
    if done:
        break

# Flavor text
print("Gathering the elves...\r\n")
time.sleep(2)
print("Cleaning the chimney...\r\n")
time.sleep(2)
print("Giving Winnie a dental bone...\r\n")
time.sleep(2)
print("Wrapping the gifts...\r\n")
time.sleep(2)
print("Fireproofing the suit...\r\n")
time.sleep(2)
print("Feeding the reindeer...\r\n")
time.sleep(2)
print("It took " + str(counter) + " calculations, but Santa made the list and checked it twice!\r\n")
time.sleep(2)


print("=======================================")
print("=       Outputting the results!       =")
print("=======================================\r\n")

for i in range(0, num_of_santas):
    matches[ santas[i] ] = santas[ nums1[i] ] + " and " + santas[ nums2[i] ]

    # Debug print statement for verification
    #print(santas[i] + ": " + matches[santas[i] ])

    # Write the results directly to a file for next year
    with open( "./" + current_year_str + "/matches/" + santas[i] + ".txt", "w") as f1:
        f1.write( santas[nums1[i]] + "\r\n")
        f1.write( santas[nums2[i]])
        
    # Write the results directly to a file for sharing
    with open( "./" + current_year_str + "/emails/" + santas[i] + ".txt", "w") as f2:
        f2.write("=============================================\r\n")
        f2.write("=     Your Secret Santa Results - 2026!     =\r\n")
        f2.write("=============================================\r\n\r\n")
        f2.write("It took " + str(counter) + " calculations, but Santa made the list and checked it twice!\r\n\r\n")
        f2.write("You are getting gifts for " + matches[santas[i] ] + "!\r\n\r\n")
        f2.write("Make sure to keep it a secret :)\r\n\r\n")
        f2.write("      ____\r\n")
        f2.write("     {} _  \\\r\n")
        f2.write("        |__ \\\r\n")
        f2.write("       /_____\\\r\n")
        f2.write("       \\o o)\\)_______\r\n")
        f2.write("       (<  ) /#######\\\r\n")
        f2.write("     __{'~` }#########|\r\n")
        f2.write("    /  {   _}_/########|\r\n")
        f2.write("   /   {  / _|#/ )####|\r\n")
        f2.write("  /   \\_~/ /_ \\  |####|\r\n")
        f2.write("  \\______\\/  \\ | |####|\r\n")
        f2.write("   \\__________\\|/#####|\r\n")
        f2.write("    |__[X]_____/ \\###/ \r\n")
        f2.write("    /___________\\\r\n")
        f2.write("     |    |/    |\r\n")
        f2.write("     |___/ |___/\r\n")
        f2.write("    _|   /_|   /\r\n")
        f2.write("   (___,_(___,_)\r\n")
