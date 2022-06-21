import csv
import requests

dictionaryapi = "https://api.dictionaryapi.dev/api/v2/entries/en/"
sentencefile = '/home/hulatpc/Downloads/sentence_word.csv'
candidatefile = '/home/hulatpc/Downloads/candidates.csv'

tsvin = open(sentencefile, "rt", encoding='utf-8')
tsvin = csv.reader(tsvin, delimiter=';')
sentencelist = list()

tsvin2 = open(candidatefile, "rt", encoding='utf-8')   
tsvin2 = csv.reader(tsvin2, delimiter='\t')
candidatelist = list()

for row in tsvin:
    sentencelist.append(row)

for row in tsvin2:
    candidatelist.append(row)

def rankingmetric(target, candidate, context):

    # word length
    # type of characters
    # number of words in candidate
    # frequency in copora

    # number of meanings

    numberofmeanings = 0;
    dictionaryentry = requests.get(dictionaryapi + candidate)
    for i in range(len(dictionaryentry.json()[0]['meanings'])):
        numberofmeanings += len(dictionaryentry.json()[0]['meanings'][i]['definitions'])

    # number of synnonyms (thesaurus), anytonyms
    
    
    # POS tag

    # CONTEXT

    return 0

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

    # SORT RANKING
    # PROPER FORMATING

    return "{}"



answer = ""
for i in range(1):
    answer += "Sentence " + str(i + 1) + " rankings: "
    answer += algorithm(sentencelist[i], candidatelist[i])
    if i + 1 != len(sentencelist):
        answer += "\n"

answerfile = open("answer.txt", "w")
answerfile.write(answer)
answerfile.close()