from datasets import load_dataset
import csv

word_frequencies = {"" : 0}

def write_to_csv(dict):
    # sort frequencies from highest to lowest
    dict = {k: v for k, v in sorted(dict.items(), key=lambda item: item[1], reverse=True)}

    with open('wikifrequencies.csv', 'w') as file:
        for key in dict.keys():
            file.write("%s, %s\n" % (key, dict[key]))

def process_article(article):
    current_word = ""
    currently_processing_paragraph = True # text file starts out immediatley on paragraph 1
    reached_end = False
    i = 0
    # TODO:: a few edge cases, like 'PTSD' and '1', ought to be handled ********************************
    while i < len(article) and not reached_end:
        if not currently_processing_paragraph: 
            while article[i] == '\n':
                i += 1
            j = i # temp var to check if loop is currently in a header, and if so, skip over the header's words
            on_sentence = False
            while not article[j] == '\n' and j + 1 < len(article):
                if article[j] == '.': # headers don't contain periods --> if we find one, go back to original index i
                    on_sentence = True
                    break
                j += 1
            if not on_sentence:
                i = j # skip over header

        if (article[i] == ' ' or article[i] == '.' or article[i] == ',' or article[i] == '"' or article[i] == ';' or article[i] == ':' or article[i] == '—' or 
            article[i] == '\t' or article[i] == '(' or article[i] == ')' or article[i] == '[' or article[i] == ']'): # indicates loop is no longer processing a word
            
            if not current_word == "" or not len(current_word) == 0:
                if current_word.lower() in word_frequencies:
                    word_frequencies[current_word.lower()] += 1
                else:
                    word_frequencies[current_word.lower()] = 1
            current_word = ""

        elif article[i] == '\n':
            currently_processing_paragraph = False

        elif article[i] == '\'':
            if i + 1 < len(article) and ord(article[i + 1]) >= 65 and ord(article[i + 1]) <= 90: # indicates that we are now in a quote and must reset the current word, i.e., the word is not in the form such as don't
                current_word = ""
        else:
            current_word += article[i]
            if  (current_word == "See also" or current_word == "Notes" or current_word == "External links" or current_word == "Bibliography" or
                    current_word == "References" or current_word == "citations"  or current_word == "Sources" or current_word == "Primary sources" or
                        current_word == "Secondary sources" or current_word == "Tertiary sources" or current_word == "Further reading"): # indicates end of the article
                            reached_end = True
        i += 1
    return 0

wiki_articles = load_dataset("wikipedia", "20220301.en", split="train")
for i in range(6458670): # number of EN articles in the provided dataset
    process_article(wiki_articles[i]['text'])

write_to_csv(word_frequencies)
    