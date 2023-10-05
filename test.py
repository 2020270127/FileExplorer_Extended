import argparse
import os
import subprocess

def list_files_and_folders(path='.'):
    try:
        with os.scandir(path) as entries:
            for entry in entries:
                entry_type = 'D' if entry.is_dir() else 'F'
                print(f"[{entry_type}] {entry.name}")
    except OSError as e:
        print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Command Line File Explorer")
    parser.add_argument("-d", "--directory", default=os.getcwd(), help="Specify the directory to explore")
    
    args = parser.parse_args()
    current_dir = args.directory

    command_list = ["ls", "-al", current_dir] #목록 출력
    command_mkdir = ["mkdir", "-p", ""] #폴더 생성
    command_mkfile = ["touch", ""] #파일 생성
    command_cp = ["cp","", ""] #파일/폴더 복사
    command_mv = ["mv", "", ""] #파일/폴더 이동
    command_rm = ["rm", "-rf", ""] #파일/폴더 삭제

    while True:
        print("---------------------------------------------")
        print(f"현재 경로: {current_dir}")
        print("Options:")
        print("1. 파일 목록 출력")
        print("2. 경로 수정")
        print("3. 폴더 생성")
        print("4. 파일 생성")
        print("5. 파일/폴더 복사")
        print("6. 파일/폴더 이동")
        print("7. 파일/폴더 삭제")
        
        print("q or Q. Quit")
        print()
        
        choice = input("Enter your choice: ")
        if choice == '1':
            result1 = subprocess.run(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            print(result1.stdout)

        #이거도 cd로 변경해보자
        elif choice == '2':
            """new_path = input("수정할 경로: ")
            if os.path.exists(new_path) and os.path.isdir(new_path):
                current_dir =  os.path.isdir(new_path)
                command_list[2] = os.path.isdir(new_path)

                print(f"{current_dir} 경로로 이동완료 하였습니다.")
            else:
                print("Invalid directory path.")"""


            new_dir = input("Enter the path to change directory: ")
            if os.path.exists(new_dir) and os.path.isdir(new_dir):
                current_dir = new_dir
                command_list[2] = new_dir

            else:
                print("Invalid directory path.")
        elif choice == '3': #mkdir
            new_dir = input("생성할 폴더명: ")
            command_mkdir[2] = new_dir
            result = subprocess.run(command_mkdir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            print(result.stdout)
        elif choice == '4': #touch
            new_file = input("생성할 파일명: ")
            command_mkfile[1] = new_file
            result = subprocess.run(command_mkfile, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            print(result.stdout)
        elif choice == '5': #cp
            what = input("복사할 파일/폴더명: ")
            where = input("붙여놓을 위치: ")
            command_cp[1] = what
            command_cp[2] = where
            result = subprocess.run(command_cp, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            print(result.stdout)
        elif choice == '6': #mv
            what = input("이동할 파일/폴더명: ")
            where = input("붙여놓을 위치: ")
            command_mv[1] = what
            command_mv[2] = where
            result = subprocess.run(command_mv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            print(result.stdout)
        elif choice == '7':
            remove = input("삭제할 파일/폴더명: ")
            command_rm[2] = remove
            result = subprocess.run(command_rm, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            print(result.stdout)
        elif choice == 'q' or choice == 'Q':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()
