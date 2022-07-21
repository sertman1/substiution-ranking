import csv

sentencefile = './assets/targetwordtest.tsv'
candidatefile = './assets/candidatestest.csv'
frequencyfile = './assets/FrencuenciasEN.csv'
wikifrequencyfile = './assets/wikifrequencies.csv'

frequencylist = {}
wiki_frequency_list = {}

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
            listofcandidates.append(candidate.strip())
            candidate = ""
    listofcandidates.append(candidate.strip())
    return listofcandidates

def algorithm(sentence, candidates):
    rankings = {}
    context = sentence[0]
    target = sentence[1]
    candidates = tokenizecandidates(candidates)
    rankings = orderbyfrequency(candidates)

    # format answer properly
    firstentry = True
    lastvalue = 0
    sortedanswers = "{"
    for k, v in rankings.items():
        if firstentry:
            lastvalue = v
            firstentry = False
            sortedanswers += k
        elif v < lastvalue:
            sortedanswers += "} {" + k
        else:
            sortedanswers += ", " + k
        lastvalue = v
    sortedanswers += "}"

    return sortedanswers

def retrieve_data_from_files(sentence_list, candidate_list):
    tsvin = open(sentencefile, "rt", encoding='utf-8')
    tsvin = csv.reader(tsvin, delimiter='\t')
    tsvin2 = open(candidatefile, "rt", encoding='utf-8')   
    tsvin2 = csv.reader(tsvin2, delimiter='\t')
    tsvin3 = open(frequencyfile, "rt", encoding='utf-8')
    tsvin3 = csv.reader(tsvin3, delimiter=';')
    tsvin4 = open(wikifrequencyfile, "rt", encoding='utf-8')
    tsvin4 = csv.reader(tsvin4, delimiter=',')

    for row in tsvin:
        sentence_list.append(row)
    for row in tsvin2:
        candidate_list.append(row)
    for row in tsvin3:
        frequencylist[row[1]] = (row[0], row[2]) # relative rank, raw frequency pair
    for row in tsvin4:
        wiki_frequency_list[row[0]] = (int)(row[1])


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

    answerfile = open("./scorerankings/testanswer.txt", "w")
    answerfile.write(answer)
    answerfile.close()

if __name__ == '__main__':
    main()
