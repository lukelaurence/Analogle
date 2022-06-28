from gensim.models import KeyedVectors
import random

model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin',binary=True)

wordlist = []
with open('words.txt','r') as words:
	for word in words:
		wordlist.append(word[:-1])

def chooseword(lst,model,minlength,forbidden=[]):
	"chooses a word from a list if it's at least minlength and not forbidden"
	word = random.choice(wordlist)
	if len(word) >= minlength and word not in forbidden and word in model:
		forbidden.append(word)
		return word
	else:
		return chooseword(lst,model,minlength,forbidden)

forbidden = []

word1 = chooseword(wordlist,model,3,forbidden)
word2 = chooseword(wordlist,model,3,forbidden)
word3 = chooseword(wordlist,model,3,forbidden)

def xisto(wrdlst,model,word1,word2,word3,forbidlst=[]):
	"Given two words, finds the word most like a third word in the same way"
	difference = model.similarity(word1,word2)
	bestsimilarity = (0,'N/A')
	for x in wrdlst:
		if x not in forbidlst and x in model:
			similarity = model.similarity(word3,x)
			if abs(difference - similarity) < abs(difference - bestsimilarity[0]):
				bestsimilarity = (similarity,x)
	return bestsimilarity

difference,word4 = xisto(wordlist,model,word1,word2,word3,forbidden)

print("'{}' is to '{}' as '{}' is to what?".format(word1.capitalize(),word2,word3))
num_guesses = 0
lastdifference = 0
attemptdifference = 0
while True:
	guess = input("Enter guess: ")
	if guess not in model:
		print("Input not recognized as word")
		continue
	num_guesses += 1
	if guess == word4:
		print("You win! '{}' is to '{}' as '{}' is to '{}'.".format(word1,word2,word3,word4))
		break
	badguess = xisto(wordlist,model,word3,guess,word1)[1]
	direction = "Wrong"
	if num_guesses > 1:
		attemptdifference = model.similarity(word3,guess)
		direction = "Warmer" if abs(difference - attemptdifference) < abs(difference - lastdifference) else "Colder"
	lastdifference = attemptdifference
	# add best guess
	print("{}, '{}' is to '{}' as '{}' is to '{}'.".format(direction,word1,badguess,word3,guess))
	print("Guesses:",num_guesses)