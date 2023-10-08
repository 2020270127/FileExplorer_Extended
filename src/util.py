#[TITLE] Utility
#[DESC] CyberHawk에서 사용하는 기능들 구현
#       현재 기능: ls, mkdir, rm, touch, cp, mv, file_sig
#[Writer] 

import enum
import os
import shutil
import binwalk

def ls():
    current_directory = os.getcwd()
    files = os.listdir(current_directory)
    print("현재 디렉토리 내의 파일 목록:")
    for file in files:
        print(file)

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

