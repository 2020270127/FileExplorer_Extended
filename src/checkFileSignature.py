import printFunc as pf
import fileHeader as fh

def checkFileSignature(fileExt, file):
    if fileExt == '':
        print(file, end='')
        pf.printlog("[UnknownType]", "Blue")
        return
    if fileExt in fh.textfile:
        print(file)
        return

    with open(file, mode='rb') as f:
        binaryData = f.read(20)
        binaryDataString = ["{:02x}".format(x) for x in binaryData]

    if fileExt in fh.fileSignatureListIndex:
        index = fh.fileSignatureListIndex.index(fileExt)
        datastream = binaryDataString[0:len(fh.fileSignatureList[index][1].split(' '))]
        fileSignature = fh.fileSignatureList[index][1].lower().split(' ')
        if datastream == fileSignature:
            print(file)
        else:
            print(file, end='')
            pf.printlog("[InproperFileExtension]", "Red")
    else:
        print(file, end='')
        pf.printlog("[InproperFileExtension]", "Red")
