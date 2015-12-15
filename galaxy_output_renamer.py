#!/usr/bin/python3
# galaxy_output_renamer.py by josh and dave

########################################################
# Usage: python3 galaxy_output_renamer.py galaxyfilenames.csv midplatedetails.csv fastadir/
########################################################

import sys
import re
import os
import shutil

del sys.argv[0]

if not len(sys.argv) == 3:
    sys.exit("""Please specify three inputs in this order:
1) Original galaxy file names CSV file
2) MID plate details CSV file
3) Directory containing galaxy output fastas""")

galaxyLinePattern = re.compile("^\d+,(\w+),(\w+),\w+,\d+,\d+,\d+,\d+,(\d+),([ \w]*)$")

galaxyFileNamesCSV = sys.argv[0]
MIDplateDetailsCSV = sys.argv[1]
fastaDirectory = sys.argv[2]

fastaOutDir = "all_renamed_fastas"

if not os.path.isdir(fastaOutDir):
    os.makedirs(fastaOutDir)

fastaFileList = [fasta for fasta in os.listdir(fastaDirectory) if os.path.isfile(os.path.join(fastaDirectory, fasta))]

for fastaFile in fastaFileList:
    newFileName = fastaFile.replace("-","_")
    newFileName = newFileName.replace("[","")
    newFileName = newFileName.replace("]","")
    fastaFile = os.path.join(fastaDirectory, fastaFile)
    newFastaFile = os.path.join(fastaDirectory, newFileName)
    os.rename(fastaFile, newFastaFile)

primerDict = {}
sampleRefDict = {}

galaxyNames = open(galaxyFileNamesCSV, "r")

galaxyNames.readline()

for line in galaxyNames:
    line = line.rstrip()
    if not galaxyLinePattern.match(line):
        print(line)
        sys.exit("Error line in unexpected format")
    else:
        forwardPrimer = galaxyLinePattern.match(line).group(1)
        reversePrimer = galaxyLinePattern.match(line).group(2)
        downloadName = galaxyLinePattern.match(line).group(3)
        isEmpty = galaxyLinePattern.match(line).group(4)
        if downloadName in primerDict:
            sys.exit("Error download name already in dictionary")
        else:
            primerDict[downloadName] = [forwardPrimer,reversePrimer,isEmpty]

galaxyNames.close()

MIDplateDetails = open(MIDplateDetailsCSV, "r")

MIDmatrix = []
forwardPrimerList = []
revPrimerList = []

for indx, line in enumerate(MIDplateDetails):
    line = line.rstrip()
    if indx == 0:
        revPrimerList = line.split(",")
        forwardPrimerList.append(revPrimerList[0])
        MIDmatrix.append(revPrimerList)
    else:
        lineList = line.split(",")
        MIDmatrix.append(lineList)
        forwardPrimerList.append(lineList[0])

MIDplateDetails.close()

GalaxyToSampleDict = {}

for key, value in primerDict.items():
    forwardPrimer = value[0]
    reversePrimer = value[1]
    isEmpty = value[2]
    if isEmpty:
        continue
    else:
        row = forwardPrimerList.index(forwardPrimer)
        col = revPrimerList.index(reversePrimer)
        if row == 0 or col == 0:
            sys.exit("Error bad index returned")
        sampleID = MIDmatrix[row][col]
        GalaxyToSampleDict[key] = sampleID

fastaFileList = [fasta for fasta in os.listdir(fastaDirectory) if os.path.isfile(os.path.join(fastaDirectory, fasta))]

for key, value in GalaxyToSampleDict.items():
    galaxySubstring = "Galaxy" + key + "_"
    fastaMatches = [fasta for fasta in fastaFileList if galaxySubstring in fasta]
    if len(fastaMatches) != 1:
        print(key)
        print(fastaMatches)
        sys.exit("Error, zero or more than one file found")
    fastaFileName = fastaMatches[0]
    fastaFileList.remove(fastaFileName)
    fastaFile = os.path.join(fastaDirectory, fastaFileName)
    outFileName = "poo" + value + ".fasta"
    outFile = os.path.join(fastaOutDir, outFileName)
    try:
        shutil.copy(fastaFile, outFile)
    except:
        sys.exit("Error copying failed")

if len(fastaFileList) != 0:
    print(fastaFileList)
    print("""!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
CAREFUL. Some fastas have not been parsed. Check carefully
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!""")

quit()
