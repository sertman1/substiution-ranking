import csv

candidate_file = 'assets/candidatestest.csv'
two_gram_file = 'assets/two-grams/drive-download-20220721T082654Z-001/data12'
ngram_dict = 'assets/ngramgooglecandidates.csv'

hashmap_of_candidates = {}

def retrieve_data_from_files(candidate_list):
    tsvin = open(candidate_file, "rt", encoding='utf-8')   
    tsvin = csv.reader(tsvin, delimiter='\t')
    tsvin2 = open(ngram_dict, "rt", encoding='utf-8')
    tsvin2 = csv.reader(tsvin2, delimiter=',')

    for row in tsvin:
      candidate_list.append(row)

    for row in tsvin2:
      hashmap_of_candidates[row[0]] = (int)(row[1])

def tokenize_candidates(candidates):
    list_of_candidates = list()
    candidate = ""
    for c in candidates[0]:
        if c != ';' and c != '\n':
            candidate += c
        else:
            list_of_candidates.append(candidate.strip())
            candidate = ""
    list_of_candidates.append(candidate.strip())
    return list_of_candidates

def process_two_gram_file(hashmap_of_candidates):
  with open(two_gram_file) as fp:
        line = fp.readline()
        # process the lines of text in the one-gram file:
        while line:
          i = 0
          two_gram = ""
          frequency = ""
          num_spaces = 0 # used to determine when the 2-gram has been found in full
          while num_spaces != 2: # ascii values for '\t' and ' '
            if ord(line[i]) == 9 or ord(line[i]) == 32:
              num_spaces += 1
              if num_spaces == 2:
                break
            two_gram += line[i]
            i += 1
          two_gram = two_gram.lower()
          # only continue if the one_gram is one of the candidates
          if two_gram in hashmap_of_candidates:
            print(two_gram)
            # skip through the white spaces
            while ord(line[i]) == 9 or ord(line[i]) == 32:
              i += 1
            # extract frequency value
            while i < len(line):
              frequency += line[i]
              i += 1    

            hashmap_of_candidates[two_gram] += int(frequency) # combine the upper case and lower case variations

          line = fp.readline() # advance to loop to next line

def write_to_csv(dict):
    # sort frequencies from highest to lowest
    dict = {k: v for k, v in sorted(dict.items(), key=lambda item: item[1], reverse=True)}

    with open('assets/ngramgooglecandidates.csv', 'w') as file:
        for key in dict.keys():
            file.write("%s, %s\n" % (key, dict[key]))

def main():
    candidate_list = list()
    retrieve_data_from_files(candidate_list)

    # for i in range(len(candidate_list)):
    #   candidates = tokenize_candidates(candidate_list[i])
    #   for candidate in candidates:
    #     if not candidate in hashmap_of_candidates:
    #       hashmap_of_candidates[candidate] = 0
    
    process_two_gram_file(hashmap_of_candidates)
    write_to_csv(hashmap_of_candidates)

if __name__ == '__main__':
    main()
