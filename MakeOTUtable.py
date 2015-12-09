#!/usr/bin/python3
# MakeOTUtable.py by josh and dave

import string
import sys
import re

seqPattern = re.compile("^[AGTC*-]+$")
IDPattern = re.compile("^>(\S+)")
batList = []
OTUList = []
OTUDict = {}
seqDict = {}

del sys.argv[0]

if len(sys.argv != !):
    sys.exit("Please specify a single input file.")

inFileName = sys.argv[0]
inFile = open(inFileName, "r")

for index, line in enumerate(inFile):
    line = line.rstrip()
    if index == 0 and not IDPattern.match(line):
        print(index)
        print(line)
        sys.exit("Error, first line of fasta file not in expected format (not an ID line)")
    if IDPattern.match(line):
        lineParts = line.split()
        currentOTU = lineParts.pop(0)
        if IDPattern.match(currentOTU):
            currentOTU = IDPattern.match(currentOTU).group(1)
        else:
            print(currentOTU)
            sys.exit("Error, OTU name not in expected format")
        sequence = inFile.readline().rstrip()
        if not seqPattern.match(sequence):
            print(sequence)
            sys.exit("Error, sequence not in expected format")
        seqDict[currentOTU] = sequence
        if currentOTU not in OTUDict:
            OTUDict[currentOTU] = {}
        if currentOTU not in OTUList:
            OTUList.append(currentOTU)
        copyInfo = lineParts.pop(0)
        copyInfoParts = copyInfo.split("-")
        copyInfo = copyInfoParts[0]
        copyInfoParts = copyInfo.split("_")
        copyNumber = copyInfoParts.pop()
        batName = "_".join(copyInfoParts)
        OTUDict[currentOTU][batName] = copyNumber
        if batName not in batList:
            batList.append(batName)
    if seqPattern.match(line):
        sys.exit("Error, sequence shouldn't match here")

inFile.close()

batList.sort()
OTUList.sort()

outFile1 = open(inFileName + ".table.out", "w")
outFile1.write("MOTU\t" + "\t".join(batList) + "\n")
outFile2 = open(inFileName + ".table_binary.out", "w")
outFile2.write("MOTU\t" + "\t".join(batList) + "\n")
outFile3 = open(inFileName + ".sequenceData", "w")
outFile3.write("MOTU\tSequence\n")

for OTU in OTUList:
    binaryList = [OTU]
    copyNumList = [OTU]
    for bat in batList:
        if bat in OTUDict[OTU]:
            copyNumList.append(OTUDict[OTU][bat])
            binaryList.append("1")
        else:
            copyNumList.append("0")
            binaryList.append("0")
    outFile1.write("\t".join(copyNumList) + "\n")
    outFile2.write("\t".join(binaryList) + "\n")
    outFile3.write(OTU + "\t" + seqDict[OTU] + "\n")


outFile1.close()
outFile2.close()
outFile3.close()

exit()
