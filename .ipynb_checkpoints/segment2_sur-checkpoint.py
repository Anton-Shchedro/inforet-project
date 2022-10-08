import functools, math
from IPython.display import clear_output
import re

class OneGramDist(dict):
   def __init__(self, filename):
      self.gramCount = 0

      for line in open(filename):
         (word, count) = line[:-1].split('\t\t')
         self[word] = int(count)
         self.gramCount += self[word]

   def __call__(self, key):
      if key in self:
         return float(self[key]) / self.gramCount
      else:
         if len(key) > 120: #20 words * 6 mean letters in word
            return 1.0 / (self.gramCount * 10**(120-2))
         else: return 1.0 / (self.gramCount * 10**(len(key)-2))

singleWordProb = OneGramDist('surname2-one-grams.txt')
def wordSeqFitness(words):
   return sum(math.log10(singleWordProb(w)) for w in words)

def memoize(f):
   cache = {}

   def memoizedFunction(*args):
      if args not in cache:
         cache[args] = f(*args)
      return cache[args]

   memoizedFunction.cache = cache
   return memoizedFunction

@memoize
def segment(word):
    if not word: return []
    word = word.lower().replace('.','').replace('  ',' ')  # change to lower case
    regex = re.compile("[^a-zA-Z -']")
    regex.sub('', word)
    while(len(word) > 0 and word[0] == ' '):
        word = word[1:]
        
    clear_output(wait=True)
    print(word)
    
    allSegmentations = [[first] + segment(rest) for (first,rest) in splitPairs(word)]
    return max(allSegmentations, key = wordSeqFitness)

def splitPairs(word, maxLen=20):
   return [(word[:i+1], word[i+1:]) for i in range(max(len(word), maxLen))]

@memoize
def segmentWithProb(word):
   segmented = segment(word)
   return (wordSeqFitness(segmented), segmented)