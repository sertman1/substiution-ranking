from datasets import load_dataset

def add_word_to_dict(word):

    return 0

def process_article(article):
    current_word = ""
    num_words = 0
    currently_processing_paragraph = True # text file starts out immediatley on paragraph 1
    # TODO:: a few edge cases, like 'PTSD', ought to be handled
    for i in range(len(article)):
        if (article[i] == ' ' or article[i] == '.' or article[i] == ',' or article[i] == '"' or article[i] == ';' or article[i] == ':' or article[i] == '—' or 
            article[i] == '\t' or article[i] == '(' or article[i] == ')' or article[i] == '[' or article[i] == ']'): # indicates loop is no longer processing a word
            
            if not current_word == "":
                add_word_to_dict(current_word)
                num_words += 1

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
                            break
        i += 1
    print(num_words)
    return 0

wiki_articles = load_dataset("wikipedia", "20220301.en", split="train")
process_article(wiki_articles[1]['text'])

# See also, Notes, External links, Bibliography, References, citations, Sources, Primary sources, Secondary sources, Tertiary sources, Further reading 

# for i in range(6458670): # number of EN articles in the provided dataset