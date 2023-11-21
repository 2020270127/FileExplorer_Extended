import sys
import os
import subprocess
import tkinter.messagebox as ms

# if len(sys.argv) >= 3:
#     function = sys.argv[1] #function : 작동 함수 문자
#     arg = sys.argv[2]     #arg     : 함수 인자 
#     file = sys.argv[3]     #file     : 파일명
#     files = sys.argv[3:]     #file     : 파일명 (file_binDiff에서 사용)
# else:
#     print("최소 3개의 인자가 필요합니다.")

def file_sig(function, file, result, arg=None): #파일 시그니쳐 스캔 함수 
    if function == '-B': #Scan target file(s) for common file signatures
        try:
            if(os.path.isfile(file)):
                result = subprocess.run(['wsl', 'binwalk', '--signature', file], text=True, capture_output=True)
                output = result.stdout
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-R': #Scan target file(s) for the specified sequence of bytes, 인자 하나 필요 (스캔할 raw string)
        try:
            if(os.path.isfile(file)):
                result = subprocess.run(['wsl', 'binwalk', '--raw={}'.format(arg), file], text=True, capture_output=True)
                output = result.stdout
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")
    
    elif function == '-A': #Scan target file(s) for common executable opcode signatures
        try:
            if(os.path.isfile(file)):
                result = result = subprocess.run(['wsl', 'binwalk', '--opcodes', file], text=True, capture_output=True)
                output = result.stdout
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")
    
    elif function == '-m': #Specify a custom magic file to use, 인자 하나 필요(설정할 매직 파일)
        try:
            if(os.path.isfile(file)):
                result = subprocess.run(['wsl', 'binwalk','--magic={}'.format(arg), file], text=True, capture_output=True)
                output = result.stdout
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")
    
    elif function == '-b': #Disable smart signature keywords
        try:
            if(os.path.isfile(file)):
                result = subprocess.run(['wsl', 'binwalk','--dumb', file], text=True, capture_output=True)
                output = result.stdout
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-l': #Show results marked as invalid
        try:
            if(os.path.isfile(file)):
                result = subprocess.run(['wsl', 'binwalk','--invalid',file], text=True, capture_output=True)
                output = result.stdout
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-x': #Exclude results that match <str>
        try:
            if(os.path.isfile(file)):
                result = subprocess.run(['wsl', 'binwalk','--exclude={}'.format(arg), file], text=True, capture_output=True)
                output = result.stdout
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-y': #Only show results that match <str>
        try:
            if(os.path.isfile(file)):
                result = subprocess.run(['wsl', 'binwalk','--include={}'.format(arg), file], text=True, capture_output=True)
                output = result.stdout
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

def file_ext(function, file, result, arg=None): #파일 추출 함수 
    if function == '-e': #Automatically extract known file types
        try:
            if(os.path.isfile(file)):
                result = subprocess.run(['wsl', 'binwalk', '--extract', file], text=True, capture_output=True)
                output = result.stdout
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")
    
    elif function == '-M': #Recursively scan extracted files
        try:
            if(os.path.isfile(file)):
                result = subprocess.run(['wsl', 'binwalk', '--matryoshka', file], text=True, capture_output=True)
                output = result.stdout
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")
    
    elif function == '-d': #Limit matryoshka recursion depth (default: 8 levels deep), 인자 하나 사용(깊이)
        try:
            if(os.path.isfile(file)):
                result = subprocess.run(['wsl', 'binwalk','--depth={}'.format(arg), file], text=True, capture_output=True)
                output = result.stdout
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")
    
    elif function == '-C': #Extract files/foldersto a custom directory (default: current working directory), 경로 인자 하나 사용. 주의필요
        try:
            if(os.path.isfile(file)):
                result = subprocess.run(['wsl', 'binwalk','--directory={}'.format(arg), file], text=True, capture_output=True)
                output = result.stdout
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-j': #Limit the size of each extracted file, 인자 하나 사용(파일 최대 크기)
        try:
            if(os.path.isfile(file)):
                result = subprocess.run(['wsl', 'binwalk','--size={}'.format(arg), file], text=True, capture_output=True)
                output = result.stdout
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-n': #Limit the number of extracted files, 인자 하나 사용(파일 최대 개수)
        try:
            if(os.path.isfile(file)):
                result = subprocess.run(['wsl', 'binwalk','--count={}'.format(arg), file], text=True, capture_output=True)
                output = result.stdout
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-0': #Execute external extraction utilities with the specified user's privileges, 인자 하나 사용(wsl 기준 어떤 권한으로 사용할껀지)
        try:
            if(os.path.isfile(file)):
                result = subprocess.run(['wsl', 'binwalk','--run-as={}'.format(arg), file], text=True, capture_output=True)
                output = result.stdout
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-1': #Do not sanitize extracted symlinks that point outside the extraction directory (dangerous)
        try:
            if(os.path.isfile(file)):
                result = subprocess.run(['wsl', 'binwalk','--preserve-symlinks', file], text=True, capture_output=True)
                output = result.stdout
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-r': #Delete carved files after extraction
        try:
            if(os.path.isfile(file)):
                result = subprocess.run(['wsl', 'binwalk','--rm', file], text=True, capture_output=True)
                output = result.stdout
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-z': #Carve data from files, but don't execute extraction utilities
        try:
            if(os.path.isfile(file)):
                result = subprocess.run(['wsl', 'binwalk','--carve', file], text=True, capture_output=True)
                output = result.stdout
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-v': #Extract into sub-directories named by the offset
        try:
            if(os.path.isfile(file)):
                result = subprocess.run(['wsl', 'binwalk','--subdirs', file], text=True, capture_output=True)
                output = result.stdout
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

def file_ent(function, file, result, arg=None): #파일 엔트로피 스캔 함수
    if function == '-E': #Calculate file entropy
        try:
            if(os.path.isfile(file)):
                result = subprocess.run(['wsl', 'binwalk', '--entropy', file], text=True, capture_output=True)
                output = result.stdout
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-F': #Use faster, but less detailed, entropy analysis
        try:
            if(os.path.isfile(file)):
                result = subprocess.run(['wsl', 'binwalk', '--fast', file], text=True, capture_output=True)
                output = result.stdout
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")
    
    elif function == '-J': #Save plot as a PNG
        try:
            if(os.path.isfile(file)):
                result = subprocess.run(['wsl', 'binwalk', '--save', file], text=True, capture_output=True)
                output = result.stdout
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")
    
    elif function == '-Q': #Omit the legend from the entropy plot graph
        try:
            if(os.path.isfile(file)):
                result = subprocess.run(['wsl', 'binwalk','--nlegend', file], text=True, capture_output=True)
                output = result.stdout
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")
    
    elif function == '-N': #Do not generate an entropy plot graph
        try:
            if(os.path.isfile(file)):
                result = subprocess.run(['wsl', 'binwalk','--nplot', file], text=True, capture_output=True)
                output = result.stdout
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-H': #Set the rising edge entropy trigger threshold (default: 0.95), 인자 하나 필요(rising threshold)
        try:
            if(os.path.isfile(file)):
                result = subprocess.run(['wsl', 'binwalk','--high={}'.format(arg), file], text=True, capture_output=True)
                output = result.stdout
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-L': #Set the falling edge entropy trigger threshold (default: 0.85), 인자 하나 필요(falling threshold)
        try:
            if(os.path.isfile(file)):
                result = subprocess.run(['wsl', 'binwalk','--low={}'.format(arg), file], text=True, capture_output=True)
                output = result.stdout
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

result = ""
file_sig('-B','Sort.py',result)
