// TODO:: program description

#include <iostream>
#include <map>
using std::map;

void print_raw_data(map<char, unsigned> char_frequencies, map<unsigned, unsigned> length_frequencies, 
										map<char, unsigned> &char_freq_no_capitalization);

// N.B.: When executing the program, give it text through cin
// text should be in the format: <complex sentence\n> <simple sentence\n> <\n>
// e.g., './a.out < mytext.txt'
int main() {
	
	std::string input_buffer;
	bool simple_sentence = false; // keeps track of which sentence computer is on when processing text
	unsigned word_length = 0; // used to store each sentences word lenght
	char c; // used to store the character's present in each sentence

	// N.B. Program attemps to (naively) omit proper nouns from data collection
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
	print_raw_data(char_frequencies_complex, length_frequencies_complex, char_freq_no_capitalization_complex);
	printf("---------------------------------------------\n\n");
	printf("----------------SIMPLE DATA------------------\n");
	printf("RESULTS: \n");
	print_raw_data(char_frequencies_simple, length_frequencies_simple, char_freq_no_capitalization_simple);
	printf("---------------------------------------------\n");

	printf("COMPARING DATA:\n");
	map<char, unsigned>:: iterator it1 = char_freq_no_capitalization_simple.begin();
	for (map<char, unsigned>::iterator it2 = char_freq_no_capitalization_complex.begin();
		 it1 != char_freq_no_capitalization_simple.end() && it2 != char_freq_no_capitalization_complex.end(); it1++, it2++) {

			 std::cout << it1->first << "   " << it2->first << std::endl;

		}
	// TODO:: COMPARE DATA

	return 0;
}

void print_raw_data(map<char, unsigned> char_frequencies, map<unsigned, unsigned> length_frequencies, map<char, unsigned> &char_freq_no_capitalization) {
	unsigned total_chars = 0;
	int counter = 0; // used to space out the character data for an easier view	

	for (map<char, unsigned>::iterator it = char_frequencies.begin(); it != char_frequencies.end(); it++) {
		std::cout << it->first << ": " << it->second << "  ";

		if (it->first >= 97 && it->first <= 122) {
			char_freq_no_capitalization[it->first - 32] += it->second; // decapitalize the char
		} else {
			char_freq_no_capitalization[it->first] += it->second;
		}

		total_chars += it->second;

		counter++;
		if (counter > 6) {
			std::cout << std::endl;
			counter = 0;
			it++;
		} else if (it++ != char_frequencies.end()) {
			std::cout << "|  "; 
		}
		it--;
	
	}
	std::cout << std::endl;
	std::cout << "LENGTH OCCURRENCES:" << std::endl;
	int sum_of_lengths = 0;
	int num_of_lengths = 0;
	counter = 0; // reset spacing
	for (map<unsigned, unsigned>::iterator it = length_frequencies.begin(); it != length_frequencies.end(); it++) {
		std::cout << it->first << ": " << it->second << "  " ;
		sum_of_lengths += it->first * it->second;
		num_of_lengths += it->second;
		counter++;
		if (counter > 4) {
			std::cout << std::endl;
			counter = 0;
			it++;
		} else if (it++ != length_frequencies.end()) {
			std::cout << "|  ";
		} 
		it--;
	}

	std::cout << "\nAVERAGE WORD LENGTH: " << ((double) sum_of_lengths) / ((double) num_of_lengths) << std::endl;
	std::cout << "CHARACTER AVERAGES: " << std::endl;

	for (map<char, unsigned>::iterator it = char_freq_no_capitalization.begin(); it != char_freq_no_capitalization.end(); it++) {
		std::cout << it->first << ": " << (((double)it->second) / ((double)total_chars)) * 100 << "%" << std::endl;
	}

}
