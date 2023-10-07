import enum
import os
import shutil


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

def main():
    user_input = input("어떤 명령을 수행하시겠습니까? (LS, MKDIR, RM, TOUCH, CP, MV): ").lower()

    try: #인자가 있는 함수
        function_name, *args = user_input.split() #공백 기준
    except ValueError: #인자가 없는 함수
        function_name = user_input
        args = [] 

    try:
        command = globals()[function_name]
        command(*args)
    except KeyError:
        print("잘못된 명령어입니다.")

    

    
    

if __name__ == "__main__":
    main()
