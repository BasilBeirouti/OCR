__author__ = 'basilbeirouti'

from classes import img2txt, readdataset, BestMatch, itemdict2csvrow, matchlines
import csv

#change these variables
imgpaths = ["FullSizeRender.jpg", "FullSizeRender2.jpg"] #list of image(s) of receipt
csvin = "groceriesdataset.csv" #master data set source
csvout = "reconstructed_grocery_list.csv" #output file to save reconstructed grocery list

dataset = readdataset(open(csvin, 'r'))
bm = BestMatch(dataset)

rawtext = img2txt(imgpaths)
rawlines = rawtext.split("\n")
print([el for el in rawlines])

processed = matchlines(bm, rawlines)
print(processed)
rawlines, items = zip(*processed)
with open(csvout, "w") as file:
    writer = csv.writer(file)
    headers = ["UID", "itemnumber", "itemname", "itemprice"]
    writer.writerow(headers)
    for el in items:
        row = itemdict2csvrow(el)
        print(row)
        writer.writerow(row)