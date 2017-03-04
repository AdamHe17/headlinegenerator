from generateprobabilities import * 
import pickle


f = open("test.pkl",'rb')
shit = pickle.load(f)
f.close()


count_all_occurrences("LEXICON.pkl", False)
