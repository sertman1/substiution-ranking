import csv

API = "https://api.dictionaryapi.dev/api/v2/entries/en/"
trial_candidate_file = './assets/candidates.csv'
test_candidate_file = './assets/candidatestest.csv'

def main():
    tsvin = open(trial_candidate_file, "rt", encoding='utf-8')   
    tsvin = csv.reader(tsvin, delimiter='\t')
    trial_candidate_list = list()

    tsvin2 = open(test_candidate_file, "rt", encoding='utf-8')   
    tsvin2 = csv.reader(tsvin2, delimiter='\t')
    test_candidate_list = list()

    for row in tsvin:
        trial_candidate_list.append(row)

    for row in tsvin2:
        test_candidate_list.append(row)

    for i in range(len(trial_candidate_list)):
        get_num_senses(trial_candidate_list[i])

    for i in range(len(test_candidate_list)):
        get_num_senses(test_candidate_list[i])

def get_num_senses(candidates):
    
    return

if __name__ == '__main__':
    main()
