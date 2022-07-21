import csv
import sys
csv.field_size_limit(sys.maxsize)

from curses.ascii import isalnum

sentencefile = 'assets/targetwordtest.tsv'
candidatefile = 'assets/candidatestest.csv'
frequencyfile = 'assets/FrencuenciasEN.csv'
wikifrequencyfile = 'assets/wikifrequencies.csv'
PPBDfile = 'assets/PPDBlarge.csv'

frequencylist = {}
wiki_frequency_list = {}
PPDBdictionary = {} # maps a target word to a list of possible replacements and their associated PPDB2.0 score

def rankingmetric(target, candidates, context):
    orderedlist = {}

    if not target in PPDBdictionary:
        for candidate in candidates:
            orderedlist[candidate] = 0
        print(target)
    else:
        for candidate in candidates:
            candidateinPPDB = False
            for element in PPDBdictionary[target]:
                if element[0] == candidate:
                    orderedlist[candidate] = element[1]
                    candidateinPPDB = True
                    break
            if not candidateinPPDB:
                # TODO: handle this case
                orderedlist[candidate] = 100 # guarentees it will be ranked most complext

    # sort by complexity scores determined in loop above (i.e., those with the lowest scores are the least complex)
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

def algorithm(sentence, candidates):
    rankings = {}
    context = sentence[0]
    target = sentence[1].strip().lower()
    candidates = tokenizecandidates(candidates)

    rankings = rankingmetric(target, candidates, context)

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

def processPPDBrow(row):
    PPDBdictionary[row[0]] = list()
    substitute = ""
    PPDBscore = ""
    onsub = True
    i = 0
    try:
        while i < len(row[1]) - 1:
            if row[1][i] == " " and not onsub: # advance to next substitute in list, reset trackers
                try:
                    PPDBdictionary[row[0]].append((substitute, float((PPDBscore))))
                except:
                    print('caught error')
                substitute = ""
                PPDBscore = ""
                onsub = True
            elif row[1][i] == ":" and row[1][i + 1] != "/": # check for link edge case, e.g., http://
                onsub = False
            elif onsub:
                substitute += row[1][i]
            else:
                PPDBscore += row[1][i]
            i += 1
    except:
        print('caught error')

def retrieve_data_from_files(sentence_list, candidate_list):
    tsvin = open(sentencefile, "rt", encoding='utf-8')
    tsvin = csv.reader(tsvin, delimiter='\t')
    tsvin2 = open(candidatefile, "rt", encoding='utf-8')
    tsvin2 = csv.reader(tsvin2, delimiter='\t')
    tsvin3 = open(frequencyfile, "rt", encoding='utf-8')
    tsvin3 = csv.reader(tsvin3, delimiter=';')
    tsvin4 = open(wikifrequencyfile, "rt", encoding='utf-8')
    tsvin4 = csv.reader(tsvin4, delimiter=',')
    tsvin5 = open(PPBDfile, "rt", encoding='utf-8')
    tsvin5 = csv.reader(tsvin5, delimiter=',')

    for row in tsvin:
        sentence_list.append(row)
    for row in tsvin2:
        candidate_list.append(row)
    for row in tsvin3:
        frequencylist[row[1]] = (row[0], row[2]) # relative rank, raw frequency pair
    for row in tsvin4:
        wiki_frequency_list[row[0]] = (int)(row[1])
    for row in tsvin5:
        processPPDBrow(row)


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
