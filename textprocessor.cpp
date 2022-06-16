// TODO:: program description

// To be added: mapping characters' occurences to word length 
// e.g., does 'x'/'X' appear more frequently in longer words?
// 'z'/'Z' appeared in words with an average length of 7.2
//
// To be added: counting of frequency of characters in words
// e.g., when 'y'/'Y' was present, it appeared an average of 1.2 times


#include <iostream>
#include <map>
using std::map;

void print_data(map<char, unsigned> char_frequencies_complex, map<unsigned, unsigned> length_frequencies_complex);

// N.B.: When executing the program, give it text through cin
// e.g., './a.out < mytext.txt'
int main() {
	
	std::string input_buffer;
	bool simple_sentence = false;
	map<char, unsigned> char_frequencies_complex;
	map<unsigned, unsigned> length_frequencies_complex;
	map<char, unsigned> char_frequencies_simple;
	map<unsigned, unsigned> length_frequencies_simple;

	// TODO::
	//map<char, map<unsigned, unsigned>> char_to_length_frequencies_complex;
	//map<char, map<unsigned, unsigned>> char_to_numberof_frequencies;
	

	while(std::getline(std::cin, input_buffer)) { // read each line of input text into buffer
		
		for(unsigned i = 0; i < input_buffer.length(); i++ ) {
			
			char c = input_buffer.at(i);
			unsigned word_length = 0;

			// TODO:: handle edge cases for words such as 'one-to-one,' 'let's,' 'dec. (??)'
			while((c >= 65 && c <= 90) || (c >= 97 && c <= 122)) { // ascii range for 'a-z' and 'A-Z'
				
				if (simple_sentence) {
					(char_frequencies_simple[c])++;
				} else {
					(char_frequencies_complex[c])++;
				}
				
				word_length++;
				i++;
				if (i < input_buffer.length()) {
					c = input_buffer.at(i);
				} else {
					break;
				}
				
				// check for words in the form 'one-to-one' etc.
				if (c == '-') {
					if (i + 1 < input_buffer.length() && 
						((input_buffer.at(i + 1) >= 65 && input_buffer.at(i + 1) <= 90) || 
						(input_buffer.at(i + 1) >= 97 && input_buffer.at(i + 1) <= 122))) {

						if (simple_sentence) { // it's a word --> increment hyphen count
							(char_frequencies_simple[c])++;
						} else {
							(char_frequencies_complex[c])++;
						} 

						word_length++;
						c = input_buffer.at(i + 1);
					}
				}

				// N.B.: words such as 'don't' are defined to be length 4
				if (c == 39) { 
					if (i + 1 < input_buffer.length() &&
                        ((input_buffer.at(i + 1) >= 65 && input_buffer.at(i + 1) <= 90) ||
                        (input_buffer.at(i + 1) >= 97 && input_buffer.at(i + 1) <= 122))) {
                                        
						if (simple_sentence) { // it's a word --> increment apostrophe count
							(char_frequencies_simple[c])++;
						} else {
							(char_frequencies_complex[c])++;
						} 

                        c = input_buffer.at(i + 1);
                    } 
				}

				if (word_length != 0) {
				(length_frequencies_complex[word_length])++;
				}
			}
		}

		if (simple_sentence == false) { // just processed a complex sentence --> indicates we are now simple
			simple_sentence = true;
		}

		if (input_buffer == "") {
			simple_sentence = false; // complex sentence for given data file begin after a newline has been reached
		}
	}

	printf("----------------COMPLEX DATA-----------------\n");
	print_data(char_frequencies_complex, length_frequencies_complex);
	printf("----------------SIMPLE DATA------------------\n");
	print_data(char_frequencies_simple, length_frequencies_simple);
	return 0;
}

void print_data(map<char, unsigned> char_frequencies_complex, map<unsigned, unsigned> length_frequencies_complex) {
	for (map<char, unsigned>::iterator it = char_frequencies_complex.begin(); it != char_frequencies_complex.end(); it++) {
		std::cout << it->first << " " << it->second << std::endl;
	}
	for (map<unsigned, unsigned>::iterator it = length_frequencies_complex.begin(); it != length_frequencies_complex.end(); it++) {
		std::cout << it->first << " " << it->second << std::endl;
	}
}
