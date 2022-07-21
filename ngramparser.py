import csv

candidate_file = 'assets/candidatestest.csv'
one_gram_file = 'assets/vocab_cs'

def retrieve_data_from_files(candidate_list):
    tsvin = open(candidate_file, "rt", encoding='utf-8')   
    tsvin = csv.reader(tsvin, delimiter='\t')

    for row in tsvin:
      candidate_list.append(row)

def tokenize_candidates(candidates):
    list_of_candidates = list()
    candidate = ""
    for c in candidates[0]:
        if c != ';' and c != '\n':
            candidate += c
        else:
            list_of_candidates.append(candidate)
            candidate = ""
    list_of_candidates.append(candidate.strip())
    return list_of_candidates

def process_one_gram_file(hashmap_of_candidates):
  with open(one_gram_file) as fp:
        line = fp.readline()
        # process the lines of text in the one-gram file:
        while line:
          i = 0
          one_gram = ""
          frequency = ""

          while ord(line[i]) != 9 and ord(line[i]) != 32: # ascii values for '\t' and ' '
            one_gram += line[i]
            i += 1

          # only continue if the one_gram is one of the candidates
          if one_gram in hashmap_of_candidates:
            # skip through the white spaces
            while ord(line[i]) == 9 or ord(line[i]) == 32:
              i += 1
            # extract frequency value
            while i < len(line):
              frequency += line[i]
              i += 1    

            hashmap_of_candidates[one_gram] = int(frequency)
            print(one_gram)        

          line = fp.readline() # advance to loop to next line

def write_to_csv(dict):
    # sort frequencies from highest to lowest
    dict = {k: v for k, v in sorted(dict.items(), key=lambda item: item[1], reverse=True)}

    with open('./assets/onegramcandidates.csv', 'w') as file:
        for key in dict.keys():
            file.write("%s, %s\n" % (key, dict[key]))

def main():
    candidate_list = list()
    retrieve_data_from_files(candidate_list)
    hashmap_of_candidates = {}

    for i in range(len(candidate_list)):
      candidates = tokenize_candidates(candidate_list[i])
      for candidate in candidates:
        if not candidate in hashmap_of_candidates:
          hashmap_of_candidates[candidate] = 0
    
    process_one_gram_file(hashmap_of_candidates)
    write_to_csv(hashmap_of_candidates)

if __name__ == '__main__':
    main()
