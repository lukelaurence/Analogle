from gensim.models import KeyedVectors
import random

def createwordlist(is_hard=False):
	"creates list of words from either wiktionary's corpus or 5000 most common"
	file = 'hardwords.txt' if is_hard else 'easywords.txt'
	wordlist = []
	with open(file,'r') as words:
		for word in words:
			wordlist.append(word[:-1])
	return wordlist

def chooseword(lst,model,minlength,forbidden=[]):
	"chooses a word from a list if it's at least minlength and not forbidden"
	word = random.choice(lst)
	if len(word) >= minlength and word not in forbidden and word in model:
		forbidden.append(word)
		return word
	else:
		return chooseword(lst,model,minlength,forbidden)

def xisto(wrdlst,model,word1,word2,word3,forbidlst=[]):
	"given two words, finds the word most like a third word in the same way"
	difference = model.similarity(word1,word2)
	bestsimilarity = (0,'N/A')
	for x in wrdlst:
		if x not in forbidlst and x in model:
			similarity = model.similarity(word3,x)
			if abs(difference - similarity) < abs(difference - bestsimilarity[0]):
				bestsimilarity = (similarity,x)
	return bestsimilarity

def generatewords(wordlist,model,minlength):
	"given a list of words and minlength, gives 2 pairs of unique words with the same relative similarity"
	forbidden = []
	word1 = chooseword(wordlist,model,minlength,forbidden)
	word2 = chooseword(wordlist,model,minlength,forbidden)
	word3 = chooseword(wordlist,model,minlength,forbidden)
	difference,word4 = xisto(wordlist,model,word1,word2,word3,forbidden)
	return word1,word2,word3,word4,difference

def gameloop(model):
	wordlist = createwordlist(input("Play in hardmode: y/n? ") == 'y')
	word1,word2,word3,word4,difference = generatewords(wordlist,model,3)
	print("'{}' is to '{}' as '{}' is to what?".format(word1.capitalize(),word2,word3))
	num_guesses = 0
	bestdifference = 0
	bestguess = ''
	attemptdifference = 0
	print(difference) #flag
	while True:
		guess = input("Enter guess: ")
		if guess == 'I give up':
			print("'{}' is to '{}' as '{}' is to '{}'.".format(word1.capitalize(),word2,word3,word4))
			break
		if guess not in model:
			print("Input not recognized as word")
			continue
		num_guesses += 1
		if guess == word4:
			print("You win! '{}' is to '{}' as '{}' is to '{}'.".format(word1.capitalize(),word2,word3,word4))
			guesses = 'guess' if num_guesses == 1 else "guesses"
			print("You won in {} {}".format(num_guesses,guesses))
			break
		badguess = xisto(wordlist,model,word3,guess,word1)[1]
		print("Incorrect, '{}' is to '{}' as '{}' is to '{}'.".format(word3,guess,word1,badguess))
		print("'{}' is to '{}' as '{}' is to what?".format(word1.capitalize(),word2,word3))
		attemptdifference = model.similarity(word3,guess)
		print(attemptdifference) #flag
		if num_guesses > 1:
			if abs(difference - attemptdifference) < abs(difference - bestdifference):
				print("Warmer. '{}' is your new best guess! Your previous best guess was '{}'.".format(guess.capitalize(),bestguess))
				bestdifference,bestguess = attemptdifference,guess
			else:
				print("Colder. Your best guess is still '{}'.".format(bestguess))
		else:
			bestdifference,bestguess = attemptdifference,guess
		# print("Guesses:",num_guesses)
	return input("Play again: y/n? ") == 'y'

if __name__ == "__main__":
	model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin',binary=True)
	while gameloop(model):
		pass