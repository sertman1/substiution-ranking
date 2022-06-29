import csv
import requests

dictionaryapi = "https://api.dictionaryapi.dev/api/v2/entries/en/"

sentencefile = 'sentence_word.csv'
candidatefile = 'candidates.csv'
frequencyfile = 'FrencuenciasEN.csv'
wikifrequencyfiles = 'wikifrequencies.csv'

frequencylist = {}
wikifrequencylist = {}

def lengthmetric(candidate):
    # complexity = 0
    # wordlength = len(candidate)
    # if wordlength >= 5 and wordlength <= 6:
    #     complexity = 1
    # elif wordlength >= 7 and wordlength <= 8:
    #     complexity = 2
    # elif wordlength >= 9 and wordlength <= 10:
    #     complexity = 3
    # else:
    #     complexity = wordlength - 7
        
    wordlength = len(candidate)
    if wordlength <= 2: # accounts for complicating technical terms, etc. 'x' 'pn'
        complexity = wordlength + 4
    else:
        complexity = wordlength
    return complexity

# take into account POS/plurals etc?
# how to handle multiword scenarios
def frequencymetric(candidate):
    complexity = 0
    if candidate in frequencylist:
        complexity = (int((frequencylist[candidate][0])) / 1000)
    else:
        complexity = 9

    return complexity

def numberofsensesmetric(candidate, numberofwords):
    complexity = 0
    numberofmeanings = 0
    dictionaryentry = requests.get(dictionaryapi + candidate)
    if dictionaryentry.status_code == 200:
        for i in range(len(dictionaryentry.json()[0]['meanings'])):
            numberofmeanings += len(dictionaryentry.json()[0]['meanings'][i]['definitions'])
        if numberofmeanings >= 4 and numberofmeanings <= 5:
            complexity = 1
        elif numberofmeanings >= 6 and numberofmeanings <= 7:
            complexity = 2
        elif numberofmeanings >= 8 and numberofmeanings <= 9:
            complexity = 3
        elif numberofmeanings >= 10 and numberofmeanings <= 12:
            complexity = 4
        elif numberofmeanings >= 13 and numberofmeanings <= 16:
            complexity = 5
        elif numberofmeanings >= 17 and numberofmeanings <= 20:
            complexity = 6
        elif numberofmeanings >= 21 and numberofmeanings <= 23:
            complexity = 7
        elif numberofmeanings >= 24 and numberofmeanings <= 27:
            complexity = 8
        elif numberofmeanings >= 28 and numberofmeanings <= 30:
            complexity = 9
        elif numberofmeanings >= 31:
            complexity = 10
    else:
        # TODO: handle case where not in dictionary
        if numberofwords == 1:
            complexity = 3
        else:
            complexity = 2
        print("Not in dictionary API: " + candidate)

    return complexity

# HIGHEST: 0.3518569192354564
# CONTEXT, MULTIWORD

def rankingmetric(target, candidate, context):
    complexity = 0 # 0 indicates the most simple word
    numberofwords = 1
    for c in candidate:
        if c == " ":
            numberofwords += 1

    # type of characters (-, x, c, z, etc..?)

    ## DECIMALS ARE DICEY. NEED TO NORMALIZE FOR TIES??
    complexity += 0.85 * lengthmetric(candidate)
    complexity += 0.7 * numberofwords
    if numberofwords >= 3:
        complexity += 1
    complexity += 1 * frequencymetric(candidate)

    # number of meanings
    # complexity += numberofsensesmetric(candidate, numberofwords)
    # number of synnonyms
    # number of antonyms
    # POS tag
    # CONTEXT

    return complexity 

def orderbyfrequency(candidates):
    orderedlist = {}

    for candidate in candidates:
        if candidate in frequencylist:
            orderedlist[candidate] = int(frequencylist[candidate][1])
        else:
            orderedlist[candidate] = 0

    # sort by most present
    orderedlist = {k: v for k, v in sorted(orderedlist.items(), key=lambda item: item[1], reverse=1)}
    return orderedlist

def tokenizecandidates(candidates):
    listofcandidates = list()
    candidate = ""
    for c in candidates[0]:
        if c != ';' and c != '\n':
            candidate += c
        else:
            listofcandidates.append(candidate)
            candidate = ""
    listofcandidates.append(candidate)
    return listofcandidates

def adjustrankingbyfreq(rankings, candidatesorderedbyfreq):
    for k, v in rankings.items():
        i = 0
        # reachedendties = False # used to recognize if we've reached the end of list with no frequency such that ties are valued equally
        for k2, v2 in candidatesorderedbyfreq.items():
            # if v2 == 0:
            #     reachedendties = True
            if k2 == k:
                if i == 0:
                    rankings[k] = v + 1
                else:
                    rankings[k] = v + (i * 4.5)
                break
            # if not reachedendties:
            #     i += 1
            i += 1
    return rankings

def algorithm(sentence, candidates):
    rankings = {}
    context = sentence[0]
    target = sentence[1]
    candidates = tokenizecandidates(candidates)
    candidatesorderedbyfreq = orderbyfrequency(candidates)

    # perform metric 
    for candidate in candidates:
        rankings[candidate] = rankingmetric(target, candidate, context)
    
    # adjust individual scores for relative frequencies
    rankings = adjustrankingbyfreq(rankings, candidatesorderedbyfreq)
    
    # sort rankings
    rankings = {k: v for k, v in sorted(rankings.items(), key=lambda item: item[1])}

    # proper formating
    # TODO:: create 'tie' range *********************************************************************
    firstentry = True
    lastvalue = 0
    sortedanswers = "{"
    for k, v in rankings.items():
        if firstentry:
            lastvalue = v
            firstentry = False
            sortedanswers += k
        elif v > lastvalue + 0.1: # accounts for close ties
            sortedanswers += "} {" + k
        else:
            sortedanswers += ", " + k
        lastvalue = v
    sortedanswers += "}"
    
    return sortedanswers

def retrieve_data_from_files(sentence_list, candidate_list):
    tsvin = open(sentencefile, "rt", encoding='utf-8')
    tsvin = csv.reader(tsvin, delimiter=';')

    tsvin2 = open(candidatefile, "rt", encoding='utf-8')   
    tsvin2 = csv.reader(tsvin2, delimiter='\t')
    tsvin3 = open(frequencyfile, "rt", encoding='utf-8')
    tsvin3 = csv.reader(tsvin3, delimiter=';')

    for row in tsvin:
        sentence_list.append(row)

    for row in tsvin2:
        candidate_list.append(row)

    for row in tsvin3:
        frequencylist[row[1]] = (row[0], row[2]) # relative rank, raw frequency pair

def main():
    sentence_list = list()
    candidate_list = list()
    retrieve_data_from_files(sentence_list, candidate_list)

    answer = ""
    for i in range(len(sentence_list)):
        answer += "Sentence " + str(i + 1) + " rankings: "
        answer += algorithm(sentence_list[i], candidate_list[i])
        if i + 1 != len(sentence_list):
            answer += "\n"

    answerfile = open("./script/answer.txt", "w")
    answerfile.write(answer)
    answerfile.close()

if __name__ == '__main__':
    main()