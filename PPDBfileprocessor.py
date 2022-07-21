import csv
import re

# if cloning from github, make sure to download the PPDB file, which can be found here:
# http://paraphrase.org/#/download (it is the XXL all English pack)

PPBDfile = 'assets/relativesimilarities.txt' # optional: can use the non-large file, but make sure to download the L pack

PPDBdictionary = {} # maps a target word to a list of possible replacements and their associated PPDB2.0 score

def write_to_csv(dict):
    with open('assets/PPDBsmall.csv', 'w') as file:
        for key in dict.keys():
            file.write("%s," % key)
            for item in dict[key]:
                file.write("%s:%s " % (item[0],item[1]))
            file.write("\n")

def processPPDBfile(line):
    target = ""
    sub = ""
    temp = "" # used for traversing through the line of text and storing its chars
    i = 0
    passedinitalsection = False
    doneparsing = False # used to quick break the loop once desired information is recieved
    while i < len(line) and not doneparsing:
        if line[i] == '|' and line[i + 1] == '|' and line[i + 2] == '|': # 3 pipes indicates a new section of the line
            i += 3 # advance to next section
            temp = temp.strip() # remove leading and trailing white spaces
            if not passedinitalsection:
                passedinitalsection = True
            elif target == "":
                target = temp
            elif sub == "":
                sub = temp
                doneparsing = True
            temp = ""
        temp += line[i]
        i += 1
    # i now points to the start of the PPDV2.0Score section
    score = ""
    doneparsing = False
    while i < len(line) and not doneparsing:
        if line[i] == "=":
            i += 1 # i now points to the score
            while line[i] != " ":
                score += line[i]
                i += 1 
            doneparsing = True
        i += 1
    if target in PPDBdictionary:
        PPDBdictionary[target].append((sub, float(score)))
    else:
        PPDBdictionary[target] = list()
        PPDBdictionary[target].append((sub, float(score)))

def traversePPDBfile():
    with open(PPBDfile) as fp:
        line = fp.readline()
        processPPDBfile(line)
        count = 0
        while line:
            processPPDBfile(line)
            line = fp.readline()
            count += 1
            print(count)
            if count % 1000000 == 0:
                write_to_csv(PPDBdictionary)  

def main():
    traversePPDBfile()

if __name__ == '__main__':
    main()

    