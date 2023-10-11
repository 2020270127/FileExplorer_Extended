import os
import sys
import binwalk

arg1= sys.argv[1] #함수 이름
arg2= sys.argv[2] #파일 이름


def file_sig(arg2): #파일 시그니쳐 출력 함수   ex) file_sig("filename") 
    try:
        if(os.path.isfile(arg2)):
            binwalk.scan(arg2,signature=True)
        else:
            raise Exception("파일이 아닙니다.")
    except Exception as e:
        print(f"binwalk 오류 발생: {e}")

def file_ext(arg2): #파일 시그니쳐 출력 함수   ex) file_sig("filename") 
    try:
        if(os.path.isfile(arg2)):
            binwalk.scan(arg2,signature=True, extract=True)
        else:
            raise Exception("파일이 아닙니다.")
    except Exception as e:
        print(f"binwalk 오류 발생: {e}")


if(arg1 == 'file_sig'):
    file_sig(arg2)
if(arg1 == 'file_ext'):
    file_ext(arg2)