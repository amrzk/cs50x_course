import cs50
import string
import re

text = cs50.get_string('Text: ')

# Obtaining letters
letters = list(re.sub("[?.,'! ]", '', text))
letter_count = len(letters)

# Obtaining words
words = text.split(' ')
word_count = len(words)

# Obtaining Sentences
sentences = re.split('[?.!]', text)
if sentences[-1] == '':
    sentences.pop(-1)
sentence_count = len(sentences)

# Average number of letter per 100 word
L = letter_count * (100 / word_count)

# Average number of sentences per 100 words
S = sentence_count * (100 / word_count)

# Coleman-Liau index
index = 0.0588 * L - 0.296 * S - 15.8

if index < 1:
    print('Before Grade 1')
elif index > 16:
    print('Grade 16+')
else:
    print(f'Grade {round(index)}')

