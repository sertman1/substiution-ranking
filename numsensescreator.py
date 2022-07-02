import csv
import requests
import time

API = "https://api.dictionaryapi.dev/api/v2/entries/en/"
trial_candidate_file = './assets/candidates.csv'
test_candidate_file = './assets/candidatestest.csv'
num_senses_file = './assets/numberofsenses.csv'


trial_candidate_list = list()
test_candidate_list = list()
num_senses_list = {}

def retrieve_data_from_files():
    tsvin = open(trial_candidate_file, "rt", encoding='utf-8')   
    tsvin = csv.reader(tsvin, delimiter='\t')
    tsvin2 = open(test_candidate_file, "rt", encoding='utf-8')   
    tsvin2 = csv.reader(tsvin2, delimiter='\t')
    tsvin3 = open(num_senses_file, "rt", encoding='utf-8')   
    tsvin3 = csv.reader(tsvin3, delimiter=',')
    
    for row in tsvin:
        trial_candidate_list.append(row)
    for row in tsvin2:
        test_candidate_list.append(row)
    for row in tsvin3:
        num_senses_list[row[0]] = (int)(row[1])

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

def get_num_senses(candidate):
    if candidate in num_senses_list:
        return # save time by not calling API unnecessarily
    else:
        numberofmeanings = 0 # a candidate not found in the API gets assigned 0c
        dictionaryentry = requests.get(API + candidate)
        if dictionaryentry.status_code == 200:
            for i in range(len(dictionaryentry.json()[0]['meanings'])):
                numberofmeanings += len(dictionaryentry.json()[0]['meanings'][i]['definitions'])

        num_senses_list[candidate] = numberofmeanings # store retireved data to be written to csv
        write_to_csv(num_senses_list)
        time.sleep(0.33) # to prevent overwhelming the public API
        
def write_to_csv(dict):
    # sort numberofsenses from highest to lowest
    dict = {k: v for k, v in sorted(dict.items(), key=lambda item: item[1], reverse=True)}
    print('writing to csv')

    with open('./assets/numberofsenses.csv', 'w') as file:
        for key in dict.keys():
            file.write("%s, %s\n" % (key, dict[key]))
    
def main():
    retrieve_data_from_files()
    for i in range(len(trial_candidate_list)):
        for candidate in tokenizecandidates(trial_candidate_list[i]):
            get_num_senses(candidate)
            

    for i in range(len(test_candidate_list)):
        for candidate in tokenizecandidates(test_candidate_list[i]):
            get_num_senses(candidate)
    
if __name__ == '__main__':
    main()
