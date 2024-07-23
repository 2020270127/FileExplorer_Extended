import os
from extensions.config import *
from tkinter import Toplevel, Label
from ttkbootstrap.dialogs.dialogs import Messagebox

format_scan_info = [] # 선택한 파일의 포맷/확장자 스캔 결과를 저장하는 리스트

# 파일 시그니처와 파일 확장자를 쌍으로 미리 저장
# 텍스트 파일의 형식은 별도의 처리를 위해 따로 저장
textfile = [".txt", ".py", ".c", ".h", ".cpp"]
fileSignatureGroup = [
    (".exe", "4D 5A"), (".msi", "23 20"), (".png", "89 50 4E 47 0D 0A 1A 0A"), (".zip", "50 4B 03 04"),
    (".jpg", "FF D8 FF E0"), (".jpeg", "FF D8 FF E0"), (".mp4", "00 00 00 18 66 74 79 70"),
    (".docx", "50 4B 03 04 14 00 06 00"), (".pptx", "50 4B 03 04 14 00 06 00"), (".xlsx", "50 4B 03 04 14 00 06 00"),
    (".hwp", "D0 CF 11 E0 A1 B1 1A E1"), (".msi", "D0 CF 11 E0 A1 B1 1A E1")
]
signatureList = [fileSignatureGroup[i][0] for i in range(len(fileSignatureGroup))]

def checkFileSignature(window):
    # 프로그램이 실행된 이후 포맷 탐색이 여러번 진행될 수 있음
    # 이전 스캔 결과와 중첩되는 것을 막기위해 리스트 정리
    format_scan_info.clear()

    # 파일 또는 폴더가 선택된 경우
    if selectedItem_list:
        # 다중 선택이 될 수 있어 리스트에 있는 모든 선택된 파일/폴더에 대해 검사를 진행
        for file in selectedItem_list:
            # 폴더가 선택된 경우 단순 폴더임을 알림
            if os.path.isdir(file):
                format_scan_info.append("Directory")
            # 파일인 경우 몇 가지 존재할 수 있는 경우의 수를 모두 다룸
            # 1. 텍스트 형식의 파일인 경우(메모장, 코드/헤더 등)
            # 2. 파일에 확장자가 없는 경우
            # 3. 그 외에 파일 확장자가 존재하는 경우
            # 4. 검사하고자 하는 파일의 확장자가 미리 저장되어 있지 않은 경우
            elif os.path.isfile(file):
                fileExt = os.path.splitext(file)[1] # 파일 확장자명만 변수로 저장
                if fileExt in textfile: # 텍스트 형식의 파일은 텍스트 파일임을 알려줌
                    format_scan_info.append("Text file")
                elif fileExt == '': # 파일 확장자가 없으면 알 수 없음
                    format_scan_info.append("Unknown Type")
                elif fileExt in signatureList: # 파일 확장자가 있으면 파일 시그니처와 일치하는지 검사
                    with open(file, mode='rb') as f:
                        # 바이너리 형태로 읽어 16진수의 파일 시그니처를 가져옴
                        binaryData = f.read(20)
                        binaryDataString = ["{:02x}".format(x) for x in binaryData]

                        # 파일 시그니처가 파일 확장자가 올바르게 매칭되는지 확인
                        index = signatureList.index(fileExt)
                        datastream = binaryDataString[0:len(fileSignatureGroup[index][1].split(' '))]
                        fileSignature = fileSignatureGroup[index][1].lower().split(' ')

                        # 시그니처와 확장자가 올바르게 매칭되는지 최종 확인
                        if datastream == fileSignature:
                            format_scan_info.append("Proper")
                        else:
                            format_scan_info.append("Improper File Extension")
                # 예외처리 : 검사 대상이 되는 파일의 확장자가 미리 저장되어 있지 않으면 에러 출력
                else:
                    format_scan_info.append("Error")
        # 최종 결과 출력
        result_window = Toplevel(window)
        result_window.title = "Format Scanning Result"

        # 검사 대상이 된 모든 파일/폴더 이름 출력
        Label(result_window, text="Name", font=("TkDefaultFont", "10", "bold")).grid(row=0, column=0)
        for i in range(len(selectedItem_list)):
            Label(result_window, text=selectedItem_list[i].split('\\')[-1]).grid(row=(i + 1), column=0)

        # 검사 대상이 된 모든 파일/폴더의 검사 결과 출력
        Label(result_window, text="Scan Info", font=("TkDefaultFont", "10", "bold")).grid(row=0, column=1)
        for j in range(len(format_scan_info)):
            Label(result_window, text=format_scan_info[j]).grid(row=(j + 1), column=1)

    # 파일이나 폴더가 선택되지 않은 경우
    else:
        Messagebox.show_info(
            message="There is no selected file or directory.", title="Info"
        )
        