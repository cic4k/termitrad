# define a function that takes the file path as input
def frequency_sorted(file_path):
    # open the file and read the content as a string
    with open(file_path, 'r') as f:
        words = f.read()

    # split the string into a list of words and count the frequency of each word
    # using the Counter class from the collections module
    from collections import Counter

    total_words = words.split(";")
    frequencies = Counter(total_words)

    # sort the dictionary by value (i.e., frequency) in descending order
    # and return the result as a list of tuples
    return sorted(frequencies.items(), key=lambda x: x[1], reverse=True), len(total_words)

# test the function
#pprint(frequency_sorted('keywords_articlesSET.txt'))
# the output should be a list of tuples containing the words and their frequencies sorted from max to min


def test_freq():
    freqs, total_words_num = frequency_sorted('keywords_articlesEAT.txt')

    i = _ = 0
    max_words = total_words_num * 0.7
    print(f"Total: {total_words_num}, Max: {max_words}")
    while i <= max_words:
        keyword, freq = freqs[_]
        print(f"{_}\t{freq}\t{keyword}\t{i}")
        i += freq
        _ += 1



