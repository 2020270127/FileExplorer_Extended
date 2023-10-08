#[TITLE] Utility
#[DESC] CyberHawk에서 사용하는 기능들 구현
#       현재 기능: ls, mkdir, rm, touch, cp, mv, file_sig
#[Writer] 

import enum
import os
import shutil
import binwalk

# 파일 시그니처와 파일 확장자를 쌍으로 미리 저장
# 텍스트 파일의 형식은 별도의 처리를 위해 따로 저장
fileSignatureList = [(".exe", "4D 5A"), (".msi", "23 20"), (".png", "89 50 4E 47 0D 0A 1A 0A"), (".zip", "50 4B 03 04")]
fileSignatureListIndex = [fileSignatureList[i][0] for i in range(len(fileSignatureList))]
textfile = [".py", ".txt"]

# 출력문자 색상 변경
formatters = {
    'Red': '\033[91m',
    'Green': '\033[92m',
    'Blue': '\033[94m',
    'END': '\033[0m'
}

# 색을 입혀 출력하는 함수
def printlog(content, color):
    if color == 'Green':
        print('{Green}'.format(**formatters) + str(content) + '{END}'.format(**formatters))
    elif color == 'Blue':
        print('{Blue}'.format(**formatters) + str(content) + '{END}'.format(**formatters))
    else:
        print('{Red}'.format(**formatters) + str(content) + '{END}'.format(**formatters))

def checkFileSignature(fileExt, file):
    if fileExt == '':
        print(file, end='')
        printlog("[UnknownType]", "Blue")
        return
    if fileExt in textfile:
        print(file)
        return

    with open(file, mode='rb') as f:
        binaryData = f.read(20)
        binaryDataString = ["{:02x}".format(x) for x in binaryData]

    if fileExt in fileSignatureListIndex:
        index = fileSignatureListIndex.index(fileExt)
        datastream = binaryDataString[0:len(fileSignatureList[index][1].split(' '))]
        fileSignature = fileSignatureList[index][1].lower().split(' ')
        if datastream == fileSignature:
            print(file)
        else:
            print(file, end='')
            printlog("[InproperFileExtension]", "Red")
    else:
        print(file, end='')
        printlog("[InproperFileExtension]", "Red")

def ls():
    current_directory = os.getcwd()
    files = os.listdir(current_directory)
    print("현재 디렉토리 내의 파일 목록:")
    for file in files:
    if os.path.isdir(file):
        print(file)
    elif os.path.isfile(file):
        fileExt = os.path.splitext(file)[1]
        checkFileSignature(fileExt, file)

def mkdir(args):
    try:
        os.mkdir(args)
        print(f"새 디렉토리 '{args}'가 생성되었습니다.")
    except FileExistsError:
        print(f"오류: '{args}' 디렉토리가 이미 존재합니다.")

def rm(args):
    if os.path.exists(args):
        if os.path.isdir(args):
            shutil.rmtree(args)
            print(f"디렉토리 '{args}'가 삭제되었습니다.")
        else:
            os.remove(args)
            print(f"파일 '{args}'가 삭제되었습니다.")
    else:
        print(f"경로 '{args}'를 찾을 수 없습니다.")

def touch(args):
    try:
        open(args, 'w').close()
        print(f"빈 파일 '{args}'가 생성되었습니다.")
    except Exception as e:
        print(f"파일 생성 중 오류 발생: {e}")

def cp(args):
    source, destination = args
    try:
        if os.path.isdir(source):
            shutil.copytree(source, destination)
            print(f"'{source}' 디렉토리가 '{destination}'로 복사되었습니다.")
        else:
            shutil.copy(source, destination)
            print(f"'{source}' 파일이 '{destination}'로 복사되었습니다.")
    except Exception as e:
        print(f"복사 중 오류 발생: {e}")

def mv(args):
    source, destination = args
    try:
        shutil.move(source, destination)
        print(f"'{source}'가 '{destination}'로 이동되었습니다.")
    except Exception as e:
        print(f"이동 중 오류 발생: {e}")


def file_sig(args): #파일 시그니쳐 출력 함수   ex) file_sig("filename") 
    try:
        if(os.path.isfile(args)):
            binwalk.scan(args,signature=True)
        else:
            raise Exception("파일이 아닙니다.")
    except Exception as e:
        print(f"binwalk 오류 발생: {e}")

