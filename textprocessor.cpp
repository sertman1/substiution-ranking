// TODO:: program description

// To be added: mapping characters' occurences to word length 
// e.g., does 'x'/'X' appear more frequently in longer words?
// 'z'/'Z' appeared in words with an average length of 7.2
//
// To be added: counting of frequency of characters in words
// e.g., when 'y'/'Y' was present, it appeared an average of 1.2 time


#include <iostream>
#include <map>
using std::map;

void print_data(map<char, unsigned> char_frequencies, map<unsigned, unsigned> length_frequencies, map<char, unsigned> &char_freq_no_capitalization);

// N.B.: When executing the program, give it text through cin
// e.g., './a.out < mytext.txt'
int main() {
	
	std::string input_buffer;
	bool simple_sentence = false;
	unsigned word_length = 0;
	char c;

	// N.B. Program attemps to omit proper nouns from data collection
	map<char, unsigned> char_frequencies_complex;
	map<unsigned, unsigned> length_frequencies_complex;
	map<char, unsigned> char_frequencies_simple;
	map<unsigned, unsigned> length_frequencies_simple;

	// TODO::
	//map<char, map<unsigned, unsigned>> char_to_length_frequencies_complex;
	//map<char, map<unsigned, unsigned>> char_to_numberof_frequencies;
	

	while(std::getline(std::cin, input_buffer)) { // read each line of input text into buffer
		
		for(unsigned i = 0; i < input_buffer.length(); i++ ) {
			
			c = input_buffer.at(i);

			while((c >= 65 && c <= 90) || (c >= 97 && c <= 122) || c == '-' || c == 39) { // ascii range for 'a-z' and 'A-Z', 39 is the apostrophe

				if (simple_sentence) {
					(char_frequencies_simple[c])++;
				} else {
					(char_frequencies_complex[c])++;
				}
				
				if (c != 39) { // N.B., words such as <don't> are defined to be length 4
					word_length++;
				}

				i++;
				if (i < input_buffer.length()) {
					c = input_buffer.at(i);
				} else {
					break;
				}
			}

			if (word_length != 0) {
				if (simple_sentence) {
					(length_frequencies_simple[word_length])++;
				} else {
					(length_frequencies_complex[word_length])++;
				}
			}

			word_length = 0;
		}

		if (simple_sentence == false) { // just processed a complex sentence --> indicates we are now simple
			simple_sentence = true;
		}

		if (input_buffer == "") {
			simple_sentence = false; // complex sentence for given data file begin after a newline has been reached
		}
	}

	map<char, unsigned> char_freq_no_capitalization_complex;
	map<char, unsigned> char_freq_no_capitalization_simple;

	printf("----------------COMPLEX DATA-----------------\n");
	printf("RESULTS: \n");		
	print_data(char_frequencies_complex, length_frequencies_complex, char_freq_no_capitalization_complex);
	printf("---------------------------------------------\n\n");
	printf("----------------SIMPLE DATA------------------\n");
	printf("RESULTS: \n");
	print_data(char_frequencies_simple, length_frequencies_simple, char_freq_no_capitalization_simple);
	printf("---------------------------------------------\n");

	// TODO:: COMPARE DATA

	return 0;
}

void print_data(map<char, unsigned> char_frequencies, map<unsigned, unsigned> length_frequencies, map<char, unsigned> &char_freq_no_capitalization) {
	unsigned total_chars;
	
	for (map<char, unsigned>::iterator it = char_frequencies.begin(); it != char_frequencies.end(); it++) {
		std::cout << it->first << ": " << it->second << std::endl;

		if (it->first >= 97 && it->first <= 122) {
			char_freq_no_capitalization[it->first - 32] += it->second; // decapitalize the char
		} else {
			char_freq_no_capitalization[it->first] += it->second;
		}

		total_chars += it->second;
	}

	int sum_of_lengths = 0;
	int num_of_lengths = 0;
	for (map<unsigned, unsigned>::iterator it = length_frequencies.begin(); it != length_frequencies.end(); it++) {
		std::cout << it->first << ": " << it->second << std::endl;
		sum_of_lengths += it->first * it->second;
		num_of_lengths += it->second;
	}

	std::cout << "\nAVERAGE WORD LENGTH: " << ((double) sum_of_lengths) / ((double) num_of_lengths) << std::endl;
	std::cout << "CHARACTER AVERAGES: " << std::endl;

	for (map<char, unsigned>::iterator it = char_freq_no_capitalization.begin(); it != char_freq_no_capitalization.end(); it++) {
		std::cout << it->first << ": " << ((double)it->second) / ((double)total_chars)  << std::endl;
	}
}
