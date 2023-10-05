from tkinter import *
import os
import os.path

## 전역 변수 선언 부분 ##

window = None
searchDirList = ['C:\\']  # 중요 변수! 검색한 폴더 목록의 스택
currentDir = 'C:\\'
dirLabel, dirListBox, fileListBox = None, None, None # 윈도창에 나올 위젯 변수들

## 함수 선언 부분 ##

def search_button_click():
    #디렉터리 내의 파일 or 폴더 탐색
    global currentDir, searchDirList
    directory_search = entry.get()
    searchDirList.append(currentDir+directory_search+'\\')
    currentDir = directory_search
    fillListBox()
    # 만약 \users\gpdus인 경우 \까지 검색하고 뒤에 꺼 검색 또 해야함.
    


def clickListBox(evt):
    global currentDir, searchDirList
    if (dirListBox.curselection() == ()):  # 다른 리스트 박스를 클릭할 때는 무시함.
        return
    dirName = str(dirListBox.get(dirListBox.curselection()))  # 클릭한 폴더 이름 (문자열)
    if dirName == '상위폴더':
        if len(searchDirList) == 1:  # 상위 폴더를 클릭했는데, 현재 C:\\면 무시함.
            return
        searchDirList.pop()  # 상위 폴더 이동이므로, 마지막 검색 폴더(=현재 폴더) 제거
    else:
        searchDirList.append(currentDir+dirName+'\\')  # 검색 리스트에 클릭한 폴더 추가

    fillListBox()


def fillListBox():
    global currentDir, searchDirList, dirLabel, dirListBox, fileListBox
    dirListBox.delete(0, END)
    fileListBox.delete(0, END)

    dirListBox.insert(END, "상위폴더")
    currentDir = searchDirList[len(searchDirList) - 1]
    dirLabel.configure(text=currentDir)
    folderList = os.listdir(currentDir)

    index = 0  # 파일 목록 위치
    for item in folderList:
        if os.path.isdir(currentDir + item):
            dirListBox.insert(END, item)
        elif os.path.isfile(currentDir + item):
            fileSize = os.path.getsize(
                currentDir + item)    # 파일 사이즈 저장 (Byte 단위)
            fileName, fileExt = os.path.splitext(item)  # 파일 이름과 확장자를 튜플로 분리

            '''
            1MB 미만은 KB 단위로 출력,
            1MB 이상은 MB단위로 출력
            '''
            if fileSize < 1000000:   # 1MB 미만
                fileSize = fileSize // 1000     # KB 단위로 (소수점 x)
                fileListBox.insert(END, item + "   " +
                                   "[" + str(fileSize) + " KB]")
            elif 1000000 <= fileSize:
                fileSize = fileSize // 1000000     # MB 단위로 (소수점 x)
                fileListBox.insert(END, item + "   " +
                                   "[" + str(fileSize) + " MB]")

            '''
            실행 파일인 exe, msi 등은 초록색,
            그림 파일인 jpg, bmp, png, gif 등은 빨간색,
            파이썬 파일인 py는 파란색
            '''
            fileExt = fileExt.lower()  # 대문자 확장자일 경우 소문자로 변환
            if fileExt == '.exe' or fileExt == '.msi':  # 확장자 별로 분류
                fileListBox.itemconfig(index, foreground="green")
            elif fileExt == '.jpg' or fileExt == '.bmp' or fileExt == '.png' or fileExt == '.gif':
                fileListBox.itemconfig(index, foreground="red")
            elif fileExt == '.py':
                fileListBox.itemconfig(index, foreground="blue")

            index += 1

## 메인 코드 부분 ##
if __name__ == "__main__":
    window = Tk()
    window.title("폴더 및 파일 목록 보기")
    window.geometry('300x500')

    dirLabel = Label(window, text=currentDir) # 위쪽 현재 폴더의 전체 경로 출력
    dirLabel.pack()

    # 검색 기능
    entry = Entry(window, width=30)
    entry.pack()

    search_button = Button(window, text="Search Path", command=search_button_click)
    search_button.pack()

     # 왼족. 현재 폴더의 하위 폴더 목록을 보여 주는 리스트 박스
    dirListBox = Listbox(window)
    dirListBox.pack(side=LEFT, fill=BOTH, expand=1)
    dirListBox.bind('<<ListboxSelect>>', clickListBox)

    # 오른쪽. 현재 폴더의 파일 목록을 보여주는 리스트 박스
    fileListBox = Listbox(window) 
    fileListBox.pack(side=RIGHT, fill=BOTH, expand=1)

    fillListBox()   # 초기엔 C:\\의 모든 폴더 목록을 만들기

    window.mainloop()
