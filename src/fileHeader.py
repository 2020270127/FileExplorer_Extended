# 파일 시그니처와 파일 확장자를 쌍으로 미리 저장
# 텍스트 파일의 형식은 별도의 처리를 위해 따로 저장
fileSignatureList = [(".exe", "4D 5A"), (".msi", "23 20"), (".png", "89 50 4E 47 0D 0A 1A 0A"), (".zip", "50 4B 03 04")]
fileSignatureListIndex = [fileSignatureList[i][0] for i in range(len(fileSignatureList))]
textfile = [".py", ".txt"]
