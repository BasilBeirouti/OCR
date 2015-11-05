__author__ = 'basilbeirouti'

import pytesseract as pt
from PIL import Image
import csv
import string

### Utility Functions ###

def img2txt(imgpath):
    if type(imgpath) == type(""):
        return pt.image_to_string(Image.open(imgpath))
    elif type(imgpath) == type([]):
        return "\n".join([img2txt(el) for el in imgpath])

def readdataset(csvfileobj):
    reader = csv.reader(csvfileobj)
    return list(enumerate(list(reader)))

def most_common(lst):
    #could make it max(set(lst)...) to make it faster, but dicts are not hashable
    return max(lst, key=lst.count)

def itemdict2csvrow(itemdict):
    return [itemdict["UID"], itemdict["itemnumber"], itemdict["itemname"], itemdict["itemprice"]]

#make sure that the groceriesdataset csv file is ordered from most common purchase to least common purchase
def makedicts(dataset):
    for el in dataset:
        tempdict = dict()
        tempdict["UID"] = el[0]
        tempdict["itemnumber"] = int(el[1][0])
        tempdict["itemname"] = el[1][1]
        tempdict["itemprice"] = float(el[1][2])
        yield tempdict

def matchlines(bmobj, rawlines):
    return [(line, el) for line, el in [(line, bmobj.coerce_line(line)) for line in rawlines] if el is not None]

class TokenizerMixin:

    numbers = lambda x: (x in "1234567890.") or False
    letters = lambda x: (x in string.ascii_uppercase) or False

    @classmethod
    def _tokenize(cls, token):
        asnum = "".join(filter(cls.numbers, token))
        asword = "".join(filter(cls.letters, token))
        if len(asword) <= 2:
            asword = ""
        if len(asnum) + len(asword) == 0:
            return None
        elif len(asnum) == 0 and len(asword)!= 0:
            return asword
        elif len(asnum) > 4 and "." not in asnum:
            return int(asnum)

    @classmethod
    def _num_or_word(cls, rawline):
        rawtokens = rawline.split()
        return [cls._tokenize(rawtoken) for rawtoken in rawtokens]


class Matcher:

    def __init__(self, dataset):
        self.knownitems = list(makedicts(dataset))

    def _perfect_match_item_num(self, token):
        for itemdict in self.knownitems:
            if itemdict["itemnumber"] == token:
                return itemdict

    def _perfect_match_item_name(self, token):
        results = []
        for itemdict in self.knownitems:
            for partialname in itemdict["itemname"].split():
                if partialname == token:
                    results.append(itemdict)
        return results

    def _most_likely_name(self, wordtokens):
        #the wordtokens here should all be derived from one rawline
        acc = []
        for token in wordtokens:
            acc = acc + [el for el in self._match_token(token) if el]
        if acc:
            return most_common(acc)

    def _match_token(self, token):
        #perfect number matches take precendence over perfect word matches
        match = self._perfect_match_item_num(token) or self._perfect_match_item_name(token)
        return match


class BestMatch(Matcher, TokenizerMixin):

    def coerce_line(self, rawline):
        tokens = self._num_or_word(rawline)
        numtokens = [token for token in tokens if type(token) == type(0)]
        for numtoken in numtokens:
            matchonnumber = self._match_token(numtoken)
            if matchonnumber:
                return matchonnumber
        wordtokens = [token for token in tokens if type(token) == type("")]
        matchonname = self._most_likely_name(wordtokens)
        if matchonname:
            return matchonname





















