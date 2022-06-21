import csv

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

answer = ""

def algorithm(sentence, candidates):
    print(sentence)
    print(candidates)

    # word length
    # type of characters
    # number of words in candidate
    # frequency in copora
    # number of meanings
    # number of synnonyms (thesaurus)

    # CONTEXT

    # PROPER FORMATING
    return "{}"

for i in range(3):
    answer += "Sentence " + str(i + 1) + " rankings: "
    answer += algorithm(sentencelist[i], candidatelist[i])
    answer += "\n"

answerfile = open("answer.txt", "w")
answerfile.write(answer)
answerfile.close()