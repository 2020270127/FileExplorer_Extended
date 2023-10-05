import argparse
import os
import shutil

# 1. ArgumentParser 만들기
parser = argparse.ArgumentParser(description="Custom command line utility")

# 2. 명령행 옵션 정의
parser.add_argument("-ls", action="store_true", help="현재 디렉토리 내의 파일 목록 표시")
parser.add_argument("-mkdir", type=str, help="새 디렉토리 만들기")
parser.add_argument("-rm", type=str, help="파일 또는 디렉토리 삭제")
parser.add_argument("-touch", type=str, help="빈 파일 생성")
parser.add_argument("-cp", nargs=2, help="파일 또는 디렉토리 복사")
parser.add_argument("-mv", nargs=2, help="파일 또는 디렉토리 이동")

# 3. 명령행 인수 파싱
args = parser.parse_args()

# 4. 선택된 옵션을 기반으로 작업 수행
if args.ls:
    current_directory = os.getcwd()
    files = os.listdir(current_directory)
    print("현재 디렉토리 내의 파일 목록:")
    for file in files:
        print(file)

elif args.mkdir:
    try:
        os.mkdir(args.mkdir)
        print(f"새 디렉토리 '{args.mkdir}'가 생성되었습니다.")
    except FileExistsError:
        print(f"오류: '{args.mkdir}' 디렉토리가 이미 존재합니다.")

elif args.rm:
    if os.path.exists(args.rm):
        if os.path.isdir(args.rm):
            shutil.rmtree(args.rm)
            print(f"디렉토리 '{args.rm}'가 삭제되었습니다.")
        else:
            os.remove(args.rm)
            print(f"파일 '{args.rm}'가 삭제되었습니다.")
    else:
        print(f"경로 '{args.rm}'를 찾을 수 없습니다.")

elif args.touch:
    try:
        open(args.touch, 'w').close()
        print(f"빈 파일 '{args.touch}'가 생성되었습니다.")
    except Exception as e:
        print(f"파일 생성 중 오류 발생: {e}")

elif args.cp:
    source, destination = args.cp
    try:
        if os.path.isdir(source):
            shutil.copytree(source, destination)
            print(f"'{source}' 디렉토리가 '{destination}'로 복사되었습니다.")
        else:
            shutil.copy(source, destination)
            print(f"'{source}' 파일이 '{destination}'로 복사되었습니다.")
    except Exception as e:
        print(f"복사 중 오류 발생: {e}")

elif args.mv:
    source, destination = args.mv
    try:
        shutil.move(source, destination)
        print(f"'{source}'가 '{destination}'로 이동되었습니다.")
    except Exception as e:
        print(f"이동 중 오류 발생: {e}")

else:
    parser.print_help()
