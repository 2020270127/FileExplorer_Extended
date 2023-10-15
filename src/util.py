#[TITLE] Utility
#[DESC] CyberHawk에서 사용하는 기능들 구현
#       현재 기능: ls, mkdir, rm, touch, cp, mv, file_sig, sort
#[Writer] 
import subprocess
import enum
import os
import shutil
import hashlib
import requests
import Sort # sort 함수 동작을 위한 자체 제작 라이브러리
import Cbinwalk as cbin# binwalk 함수 동작을 위한 메크로
import time
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
            subprocess.run(['wsl', 'python3','bin.py','file_sig' ,args])
        else:
            raise Exception("파일이 아닙니다.")
    except Exception as e:
        print(f"binwalk 오류 발생: {e}")
def file_ext(args): #파일 시그니쳐 출력 함수   ex) file_sig("filename") 
    try:
        if(os.path.isfile(args)):
            subprocess.run(['wsl', 'python3','bin.py','file_ext' ,args])
        else:
            raise Exception("파일이 아닙니다.")
    except Exception as e:
        print(f"binwalk 오류 발생: {e}")
        

'''
* Name : sort

* Description : format, size, time, name 4가지 기능별 정렬 함수
    - format : 포맷 타입을 입력 받은 후 현재 디렉토리에서 해당 포맷 타입을 가진 파일을 출력
    - size : 현재 디렉토리에 있는 파일들 중 '파일 크기가 가장 작은 것' 부터 순차적으로 출력 (디렉토리는 출력 안함)
    - time : 가장 최근에 변경한 적이 있는 파일부터 순차적으로 출력하며 연도-월-일-시-분 도 같이 출력
    - name : 이름 순으로 정렬('영어 기준' 영어가 먼저 출력된 후 한글 파일들이 나오며 한글 자음 기준 정렬은 아직 구현 x)

* Arguments :   -args : 문자열 값으로 'format', 'size', 'time', 'name' 중 하나가 입력됨

* Change Date : 2023. 10. 08

* Version : 0.2                

'''
def sort(args): 
    mode = ['format', 'size', 'time', 'name']
    current_directory = os.getcwd()
    files = os.listdir(current_directory)
    #try:
    if (args == mode[0]):
        uformat = input('input format type : ')
        format_dict = {}

        for file in files:
            format = file.split('.')[-1]
            if format not in format_dict:
                format_dict[format] = [file]
            else:
                format_dict[format].append(file)

        if (uformat in list(format_dict.keys())):        
            f = format_dict.get(uformat, [])
            print('\n')
            for file in f:
                print(file)
        else :
            print(f'Can not find format {uformat}')

    elif (args == mode[1]):   # size sort (파일 크기 기준 정렬)      
        current_dir = os.getcwd() 
        files_in_current_dir = Sort.size_sort().size_list_files_in_current_dir(current_dir)
        sorted_files = Sort.size_sort().heap_sort_by_size(files_in_current_dir)
        for file_name, file_size in sorted_files:
            print(file_name, end = '  ')
            Sort.size_sort().get_size(file_size)

    elif (args == mode[2]): # time sort (최종 변경 시간 기준 정렬)
        current_dir = os.getcwd()
        files_in_current_dir = Sort.time_sort().time_list_files_in_current_dir(current_dir)
        sorted_files = Sort.time_sort().heap_sort_by_created_time(files_in_current_dir)
        for file_name, file_modified_time in sorted_files:
            print('%-50s%20s' %(str(file_name), str(file_modified_time)))

    elif (args == mode[3]): # name sort(영어 기준)
        current_directory = os.getcwd()
        sorted_file_list = Sort.name_sort().sort_files_by_name(current_directory)
        for file_name in sorted_file_list:
            print(file_name)                        
    else :
        print('잘못된 명령어입니다.')
    #except :
        #print('에러 발생.')

'''
* Name : filehash

* Description : 파일의 MD5, SHA256, SHA1 해시를 계산하는 함수
                ex) filehash('CyberHawk.py')

* Arguments : 해시를 계산할 파일의 경로가 전달됨 (param file_path)

* Change Date : 2023. 10. 09

'''
def filehash(file_path):
    try:
        with open(file_path, 'rb') as file:
            md5_hash = hashlib.md5()
            sha256_hash = hashlib.sha256()
            sha1_hash = hashlib.sha1()

            while True:
                data = file.read(65536)  # 파일을 64KB 블록으로 읽음
                if not data:
                    break

                md5_hash.update(data)
                sha256_hash.update(data)
                sha1_hash.update(data)

            # 해시 값을 16진수로 반환
            hashes = {
                'md5': md5_hash.hexdigest(),
                'sha256': sha256_hash.hexdigest(),
                'sha1': sha1_hash.hexdigest()
            }

            print(hashes)
            #return hashes
        
    except FileNotFoundError:
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")

def virus_scan(file_name):
    upload_url = f'https://www.virustotal.com/vtapi/v2/file/scan'
    api_key = 'api 키 입력'
    file_path=os.getcwd()
    file_path+="/"+file_name
    report_url = f'https://www.virustotal.com/vtapi/v2/file/report'
    upload_files = {'file': (file_path, open(file_path, 'rb'))}
    upload_params = {'apikey': api_key}

    try:
        upload_response = requests.post(upload_url, files=upload_files, params=upload_params)
        upload_response = requests.post(upload_url, files=upload_files, params=upload_params)
        if upload_response.status_code == 200:
            upload_result = upload_response.json()
            scan_id = upload_result.get('scan_id')
            if scan_id:
                print(f"File uploaded successfully. Scan ID: {scan_id}")
                time.sleep(10)
                report_params = {'apikey': api_key, 'resource': scan_id}
                report_response = requests.get(report_url, params=report_params)
                report_response = requests.get(report_url, params=report_params)
                if report_response.status_code == 200:
                    report_result = report_response.json()
                    if 'scans' in report_result:
                        for antivirus, scan_result in report_result['scans'].items():
                            print(f"{antivirus}: Detected: {scan_result['detected']}, Result: {scan_result['result']}")
                    else:
                        print("No scan results found.")
                else:
                    print(f"Error getting scan results: {report_response.status_code} - {report_response.text}")
            else:
                print("No scan ID found in upload response.")
        else:
            print(f"Error uploading file: {upload_response.status_code} - {upload_response.text}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

