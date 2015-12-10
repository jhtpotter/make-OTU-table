#!/usr/bin/python3
# extractblastdetails.py by dave
#Requires two input files, the first is your BLAST output from blasting the fasta file output in the last step, the second is the OTUs/sequences table output by the last step

#Imports things for python to use 
import string
import sys
import re

OTUPattern = re.compile("^Query=\s(\S+)$") #This should match any line that begins with 'Query= ', followed by any string of characters
accessionPattern =  re.compile("^gb\|([A-Z0-9.]+)\|.+\s+(\d+)\s+([0-9]+e-[0-9]+)$") #This matches the beginning of an accession number. WARNING= this will match way more lines than I want, I'll need to skip to the next instance of OTUPattern after selecting the first instance of this
seqPattern = re.compile("^[AGTC*-]+$")
OTUList = []
seqDict = {}
accessionDict = {}

del sys.argv[0]

if len(sys.argv) != 2:
    sys.exit("Please specify two input files, the first being a blast output, the second being your output table.")

blastFileName = sys.argv[0]
blastFile = open(blastFileName, "r")

seqDataFileName = sys.argv[1]
seqDataFile = open(seqDataFileName, "r")

for line in seqDataFile:
    line = line.rstrip()
    lineParts = line.split("\t")
    OTUname = lineParts[0]
    sequence = lineParts[1]
    if OTUname == "MOTU" and sequence == "Sequence":
        continue
    elif not seqPattern.match(sequence):
        print(line)
        sys.exit("Error, sequence not in expected format")
    elif OTUname in seqDict:
        sys.exit("Error, OTU already found in dictionary")
    else:
        OTUList.append(OTUname)
        seqDict[OTUname] = sequence

seqDataFile.close()

OTUList.sort()

for line in blastFile:
    line = line.rstrip()
    if OTUPattern.match(line):
        currentOTU = OTUPattern.match(line).group(1)
        if currentOTU not in seqDict:
            sys.exit("Error, OTU not found in sequence dictionary")
    if accessionPattern.match(line) and currentOTU not in accessionDict:
        accession = accessionPattern.match(line).group(1)
        score = accessionPattern.match(line).group(2)
        eValue = accessionPattern.match(line).group(3)
        accessionDict[currentOTU] = [accession, score, eValue]
        nextLine = blastFile.readline()
        while accessionPattern.match(nextLine):
            nextLine = blastFile.readline()
        line = nextLine

blastFile.close()

outFileName = seqDataFileName
outFile = open(outFileName, "w")
outFile.write("MOTU\tSequence\tAccession\tScore\tEValue\n")

for OTU in OTUList:
    sequence = seqDict[OTU]
    accession = accessionDict[OTU][0]
    score = accessionDict[OTU][1]
    eValue = accessionDict[OTU][2]
    outFile.write(OTU + "\t" + sequence + "\t" + accession + "\t" + score + "\t" + eValue + "\n")

outFile.close()


quit()
