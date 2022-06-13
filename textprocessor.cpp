// This program takes a text file (written in the English alphabet)
// and outputs the frequency of each 26 letters in the text as well
// as hyphens, if they are used to form a word (e.g., one-year-old).
// Additionally, it outputs the frequency of the words' lengths,
// as well as the average word length. 
// This program assumes that the words in the text are spelled correctly. 

// To be added: mapping characters' occurences to word length 
// e.g., does 'x'/'X' appear more frequently in longer words?
// 'z'/'Z' appeared in words with an average length of 7.2
//
// To be added: counting of frequency of characters in words
// e.g., when 'y'/'Y' was present, it appeared an average of 1.2 times


#include <iostream>
#include <map>
using std::map;

void print_data(map<char, unsigned> char_frequencies, map<unsigned, unsigned> length_frequencies);

// N.B.: When executing the program, give it text through cin
// e.g., './a.out < mytext.txt'
int main() {
	
	std::string input_buffer;
	map<char, unsigned> char_frequencies;
	map<unsigned, unsigned> length_frequencies;
	
	// TODO::
	//map<char, map<unsigned, unsigned>> char_to_length_frequencies;
	//map<char, map<unsigned, unsigned>> char_to_numberof_frequencies;

	while(std::getline(std::cin, input_buffer)) { // read each line of input text into buffer
		for(unsigned i = 0; i < input_buffer.length(); i++) {
			
			char c = input_buffer.at(i);
			unsigned word_length = 0;

			// TODO:: handle edge cases for words such as 'one-to-one,' 'let's,' 'dec. (??)'
			while((c >= 65 && c <= 90) || (c >= 97 && c <= 122)) { // ascii range for 'a-z' and 'A-Z'
				
				(char_frequencies[c])++;
				word_length++;
				i++;
				if (i < input_buffer.length()) {
					c = input_buffer.at(i);
				} else {
					break;
				}
				
				// check for words in the form 'one-to-one' etc.
				// N.B.: hyphens are counted in the char frequency if they constitute a word
				if (c == '-') {
					if (i + 1 < input_buffer.length() && 
						(input_buffer.at(i + 1) >= 65 && input_buffer.at(i + 1) <= 90) || 
						(input_buffer.at(i + 1) >= 97 && input_buffer.at(i + 1) <= 122)) {

						(char_frequencies[c])++; // it's a word --> increment hyphen count
						word_length++;
						c = input_buffer.at(i + 1);

					}
				}

				// N.B.: words such as 'don't' are defined to be length 4
				if (c == 39) { // TODO:: other types of potential apostrophes
					if (i + 1 < input_buffer.length() &&
                                                (input_buffer.at(i + 1) >= 65 && input_buffer.at(i + 1) <= 90) ||
                                                (input_buffer.at(i + 1) >= 97 && input_buffer.at(i + 1) <= 122)) {
                                        
                                                c = input_buffer.at(i + 1);

                                        } 

				}

			if (word_length != 0) {
				(length_frequencies[word_length])++;
			}
			}

		}

	}

	print_data(char_frequencies, length_frequencies);
	return 0;
}

void print_data(map<char, unsigned> char_frequencies, map<unsigned, unsigned> length_frequencies) {
	for (map<char, unsigned>::iterator it = char_frequencies.begin(); it != char_frequencies.end(); it++) {
		std::cout << it->first << " " << it->second << std::endl;
	}
	for (map<unsigned, unsigned>::iterator it = length_frequencies.begin(); it != length_frequencies.end(); it++) {
		std::cout << it->first << " " << it->second << std::endl;
	}

}
