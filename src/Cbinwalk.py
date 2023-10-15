import sys
import os
import subprocess

# if len(sys.argv) >= 3:
#     function = sys.argv[1] #function : 작동 함수 문자
#     arg = sys.argv[2]     #arg     : 함수 인자 
#     file = sys.argv[3]     #file     : 파일명
#     files = sys.argv[3:]     #file     : 파일명 (file_binDiff에서 사용)
# else:
#     print("최소 3개의 인자가 필요합니다.")

def file_sig(function, file, arg=None): #파일 시그니쳐 스캔 함수 
    if function == '-B': #Scan target file(s) for common file signatures
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk', '--signature', file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-R': #Scan target file(s) for the specified sequence of bytes, 인자 하나 필요 (스캔할 raw string)
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk', '--raw={}'.format(arg), file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")
    
    elif function == '-A': #Scan target file(s) for common executable opcode signatures
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk', '--opcodes', file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")
    
    elif function == '-m': #Specify a custom magic file to use, 인자 하나 필요(설정할 매직 파일)
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk','--magic={}'.format(arg), file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")
    
    elif function == '-b': #Disable smart signature keywords
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk','--dumb', file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-l': #Show results marked as invalid
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk','--invalid',file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-x': #Exclude results that match <str>
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk','--exclude={}'.format(arg), file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-y': #Only show results that match <str>
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk','--include={}'.format(arg), file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

def file_ext(function, file, arg=None): #파일 추출 함수 
    if function == '-e': #Automatically extract known file types
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk', '--extract', file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")
    
    elif function == '-M': #Recursively scan extracted files
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk', '--matryoshka', file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")
    
    elif function == '-d': #Limit matryoshka recursion depth (default: 8 levels deep), 인자 하나 사용(깊이)
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk','--depth={}'.format(arg), file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")
    
    elif function == '-C': #Extract files/foldersto a custom directory (default: current working directory), 경로 인자 하나 사용. 주의필요
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk','--directory={}'.format(arg), file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-j': #Limit the size of each extracted file, 인자 하나 사용(파일 최대 크기)
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk','--size={}'.format(arg), file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-n': #Limit the number of extracted files, 인자 하나 사용(파일 최대 개수)
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk','--count={}'.format(arg), file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-0': #Execute external extraction utilities with the specified user's privileges, 인자 하나 사용(wsl 기준 어떤 권한으로 사용할껀지)
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk','--run-as={}'.format(arg), file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-1': #Do not sanitize extracted symlinks that point outside the extraction directory (dangerous)
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk','--preserve-symlinks', file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-r': #Delete carved files after extraction
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk','--rm', file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-z': #Carve data from files, but don't execute extraction utilities
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk','--carve', file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-v': #Extract into sub-directories named by the offset
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk','--subdirs', file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

def file_ent(function, file, arg=None): #파일 엔트로피 스캔 함수
    if function == '-E': #Calculate file entropy
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk', '--entropy', file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-F': #Use faster, but less detailed, entropy analysis
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk', '--fast', file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")
    
    elif function == '-J': #Save plot as a PNG
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk', '--save', file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")
    
    elif function == '-Q': #Omit the legend from the entropy plot graph
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk','--nlegend', file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")
    
    elif function == '-N': #Do not generate an entropy plot graph
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk','--nplot', file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-H': #Set the rising edge entropy trigger threshold (default: 0.95), 인자 하나 필요(rising threshold)
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk','--high={}'.format(arg), file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-L': #Set the falling edge entropy trigger threshold (default: 0.85), 인자 하나 필요(falling threshold)
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk','--low={}'.format(arg), file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

def file_binDiff(function, files, arg=None): #파일끼리 차이를 보여주는 함수, files는 리스트가 와야함
    if function == '-W': #Perform a hexdump / diff of a file or files
        try:
            for file in files:
                if(os.path.isfile(file)):
                    pass
                else:
                    raise Exception("파일이 아닙니다.")
            subprocess.run(['wsl', 'binwalk', '--hexdump'] + files)
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-G': #Scan target file(s) for the specified sequence of bytes, 인자 하나 필요 (스캔할 raw string)
        try:
            for file in files:
                if(os.path.isfile(file)):
                    pass
                else:
                    raise Exception("파일이 아닙니다.")
                subprocess.run(['wsl', 'binwalk', '--raw={}'.format(arg)] + files)
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")
    
    elif function == '-i': #Scan target file(s) for common executable opcode signatures
        try:
            for file in files:
                if(os.path.isfile(file)):
                    pass
                else:
                    raise Exception("파일이 아닙니다.")
            subprocess.run(['wsl', 'binwalk', '--opcodes'] + files)    
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")
    
    elif function == '-U': #Specify a custom magic file to use, 인자 하나 필요(설정할 매직 파일)
        try:
            for file in files:
                if(os.path.isfile(file)):
                    pass
                else:
                    raise Exception("파일이 아닙니다.")
            subprocess.run(['wsl', 'binwalk','--magic={}'.format(arg)] + files)
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")
    
    elif function == '-u': #Disable smart signature keywords
        try:
            for file in files:
                if(os.path.isfile(file)):
                    pass
                else:
                    raise Exception("파일이 아닙니다.")
            subprocess.run(['wsl', 'binwalk','--dumb'] + files)
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-w': #Show results marked as invalid
        try:
            for file in files:
                if(os.path.isfile(file)):
                    pass
                else:
                    raise Exception("파일이 아닙니다.")
            subprocess.run(['wsl', 'binwalk','--invalid'] + files)
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

def file_rawComp(function, file, arg=None): #압축 식별 함수
    if function == '-X': #Scan for raw deflate compression streams
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk', '--deflate', file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-Z': #Scan for raw LZMA compression streams
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk', '--lzma', file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")
    
    elif function == '-P': #Perform a superficial, but faster, scan
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk', '--partial', file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")
    
    elif function == '-S': #Stop after the first result
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk','--stop', file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")
    
def file_general(function, file, arg=None): #binwalk 기본 함수
    if function == '-l': #Number of bytes to scan
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk', '--length={}'.format(arg), file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-o': #Start scan at this file offset
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk', '--offset={}'.format(arg), file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")
    
    elif function == '-O': #Add a base address to all printed offsets
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk', '--base={}'.format(arg), file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")
    
    elif function == '-K': #Set file block size
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk','--block={}'.format(arg), file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")
    
    elif function == '-g': #Reverse every n bytes before scanning
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk','--swap={}'.format(arg), file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-f': #Log results to file
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk','--log={}'.format(arg), file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-c': #Log results to file in CSV format
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk','--csv', file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-t': #Format output to fit the terminal window
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk','--term', file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")
    
    elif function == '-q': #Suppress output to stdout
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk','--quiet', file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-v': #Enable verbose output
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk','--verbose', file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-a': #Only scan files whose names match this regex
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk','--finclude={}'.format(arg), file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-p': #Do not scan files whose names match this regex
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk','--fexclude={}'.format(arg), file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")

    elif function == '-s': #Enable the status server on the specified port
        try:
            if(os.path.isfile(file)):
                subprocess.run(['wsl', 'binwalk','--status={}'.format(arg), file])
            else:
                raise Exception("파일이 아닙니다.")
        except Exception as e:
            print(f"binwalk 오류 발생: {e}")
