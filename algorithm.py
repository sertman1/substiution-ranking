import csv
import requests

dictionaryapi = "https://api.dictionaryapi.dev/api/v2/entries/en/"
# sentencefile =  '/Users/sammy/Desktop/substiution-ranking/sentence_word.csv'
# candidatefile = '/Users/sammy/Desktop/substiution-ranking/candidates.csv'
sentencefile = '/home/hulatpc/Downloads/sentence_word.csv'
candidatefile = '/home/hulatpc/Downloads/candidates.csv'
frequencyfile = '/home/hulatpc/Downloads/FrencuenciasEN.csv'

tsvin = open(sentencefile, "rt", encoding='utf-8')
tsvin = csv.reader(tsvin, delimiter=';')
sentencelist = list()

tsvin2 = open(candidatefile, "rt", encoding='utf-8')   
tsvin2 = csv.reader(tsvin2, delimiter='\t')
candidatelist = list()

tsvin3 = open(frequencyfile, "rt", encoding='utf-8')
tsvin3 = csv.reader(tsvin3, delimiter=';')
frequencylist = {}

for row in tsvin:
    sentencelist.append(row)

for row in tsvin2:
    candidatelist.append(row)

for row in tsvin3:
    frequencylist[row[1]] = (row[0], row[2]) # relative rank, raw frequency pair

def lengthmetric(candidate):
    complexity = 0
    wordlength = len(candidate)
    if wordlength >= 5 and wordlength <= 6:
        complexity = 1
    elif wordlength >= 7 and wordlength <= 8:
        complexity = 2
    elif wordlength >= 9 and wordlength <= 10:
        complexity = 3
    else:
        complexity = wordlength - 7

    return complexity

def frequencymetric(candidate):
    complexity = 0
    if candidate in frequencylist:
        complexity = (int((frequencylist[candidate][0])) / 1000)
    else:
        complexity = 5

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

def rankingmetric(target, candidate, context):
    complexity = 0 # 0 indicates the most simple word

    # word length
    complexity += lengthmetric(candidate)

    # type of characters

    # number of words in candidate
    numberofwords = 1
    for c in candidate:
        if c == " ":
            numberofwords += 1
    complexity += numberofwords

    # frequency in copora (consult multiple)
    complexity += frequencymetric(candidate)

    # number of meanings
    complexity += numberofsensesmetric(candidate, numberofwords)

    # number of synnonyms
    
    # number of antonyms
    
    # POS tag

    # CONTEXT

    return complexity 

def tokenizecandidates(candidates):
    listofcandidates = list()
    candidate = ""
    for c in candidates[0]:
        if c != ';' and c != '\n':
            candidate += c
        else:
            listofcandidates.append(candidate)
            candidate = ""
    return listofcandidates


def algorithm(sentence, candidates):
    rankings = {}
    context = sentence[0]
    target = sentence[1]
    candidates = tokenizecandidates(candidates)
    for candidate in candidates:
        rankings[candidate] = rankingmetric(target, candidate, context)

    # sort rankings
    rankings = {k: v for k, v in sorted(rankings.items(), key=lambda item: item[1])}

    # proper formating
    firstentry = True
    lastvalue = 0
    sortedanswers = "{"
    for k, v in rankings.items():
        if firstentry:
            lastvalue = v
            firstentry = False
            sortedanswers += k
        elif v > lastvalue:
            sortedanswers += "} {" + k
        else:
            sortedanswers += ", " + k
        lastvalue = v
    sortedanswers += "}"
    
    return sortedanswers



answer = ""
for i in range(len(sentencelist)):
    answer += "Sentence " + str(i + 1) + " rankings: "
    answer += algorithm(sentencelist[i], candidatelist[i])
    if i + 1 != len(sentencelist):
        answer += "\n"

answerfile = open("answer.txt", "w")
answerfile.write(answer)
answerfile.close()
