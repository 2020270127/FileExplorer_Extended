import os
import tkinter as tk
from tkinter import Toplevel, Label, messagebox, simpledialog
from datetime import datetime
from functools import partial
from sys import platform
import shutil
import threading
from PIL import Image, ImageTk
import ttkbootstrap as ttk
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap.dialogs.dialogs import Querybox
import psutil
import hashlib
import requests
import time

# import custom functions
import ext
import util
from Sort import *
from binwalk import *
from config import *

# globals
fileNames = []
file_path = ""  # path of main.py
lastDirectory = ""
selectedItem = ""  # focused item on Treeview
src = ""  # temp path for copying
theme = ""  # current theme
photo_ref = []  # keeps references of photos
currDrive = ""
available_drives = []
font_size = "10"  # default is 10
folderIcon = 0
fileIcon = 0
items = 0  # holds treeview items
cwdLabel = 0
footer = 0
src_list = []  # 전역 변수: 붙여넣기할 항목 경로를 저장하는 리스트

format_scan_info = [] # 선택한 파일의 포맷/확장자 스캔 결과를 저장하는 리스트
files = ['1', '2', '3']  # binwalk를 사용할 파일 목록들, 절대경로/상대경로/파일명 모두 가능.



script_path = os.path.abspath(__file__) # virusScan apiKey.txt 생성 위치 지정을 위한 변수
script_folder = os.path.dirname(script_path) #virusScan apiKey.txt 생성 위치 지정을 위한 변수

class Theme:
    # available themes
    # Dark
    solarD = "solar"
    superheroD = "superhero"
    Darkly = "darkly"
    CyborgD = "cyborg"
    VaporD = "vapor"
    # Light
    literaL = "litera"  # default theme
    mintyL = "minty"
    morphL = "morph"
    yetiL = "yeti"

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

def checkPlatform():
    global currDrive, available_drives
    if platform == "win32":
        available_drives = [
            chr(x) + ":" for x in range(65, 91) if os.path.exists(chr(x) + ":")
        ]  # 65-91 -> search for drives A-Z
        currDrive = available_drives[0]  # current selected drive
    elif platform == "linux":
        available_drives = "/"
        currDrive = available_drives

def hashExtract(window):
    global items
    hash_result = []

    if selectedItem_list:
        if len(selectedItem_list) > 2:
            Messagebox.show_info(
                message="Only 1 or 2 items are permitted. Sorry!", title="Error!"
            )
            return

        for file in selectedItem_list:
            # 디렉토리인 경우 (해싱 불가능)
            if os.path.isdir(file):
                Messagebox.show_info(
                    message="Hashing files are only possible."+file+"is a file", title="Info"
                )
                break
            # 파일인 경우
            elif os.path.isfile(file):
                try:
                    with open(file, mode='rb') as f:
                        md5_hash = hashlib.md5()
                        sha256_hash = hashlib.sha256()
                        sha1_hash = hashlib.sha1()

                        while True:
                            data = f.read(65536)  # 파일을 64KB 블록으로 읽음
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
                        hash_result.append([file, hashes])
                    
                except Exception as e:
                    print('Error Message:', e)

        
        # 최종 결과 출력
        result_window = Toplevel(window)
        result_window.title = "Hash Extract Result"

        Label(result_window, text="Hash Type", font=("TkDefaultFont", "10", "bold")).grid(row=0, column=0)
        Label(result_window, text="MD5").grid(row=1, column=0)
        Label(result_window, text="SHA256").grid(row=2, column=0)
        Label(result_window, text="SHA1").grid(row=3, column=0)


        # 검사 대상이 된 모든 파일/폴더 이름 출력
        for col, hr in enumerate(hash_result):
            i, hashes = hr
            i = i.split('/')[-1]
            Label(result_window, wraplength=400, text=f"Result of: {i}", font=("TkDefaultFont", "10", "bold")).grid(row=0, column=col+1)
            Label(result_window, wraplength=400, text=hashes['md5']).grid(row=1, column=col+1)
            Label(result_window, wraplength=400, text=hashes['sha256']).grid(row=2, column=col+1)
            Label(result_window, wraplength=400, text=hashes['sha1']).grid(row=3, column=col+1)        

        # 2개 선택한 경우 같은지, 다른지 확인
        if len(selectedItem_list) == 2:
            if hash_result[0][1]['sha256'] == hash_result[1][1]['sha256']:
                Label(result_window,text="Two files are the same", font=("TkDefaultFont", "10", "bold")).grid(row=4, column=1, columnspan=2)
            else:
                Label(result_window,text="Two files are different", font=("TkDefaultFont", "10", "bold")).grid(row=4, column=1, columnspan=2)

    # 파일이나 폴더가 선택되지 않은 경우
    else:
        Messagebox.show_info(
            message="There is no selected file.", title="Error!"
        )

def createWindow():
    root = ttk.Window(themename=theme)
    root.title("CyberHawk")
    root.geometry("1280x720")
    root.resizable(True, True)
    root.iconphoto(False, tk.PhotoImage(file=file_path + "icon.png"))

    

    return root

def refresh(queryNames):
    global fileNames, folderIcon, fileIcon, items, cwdLabel, footer
    # Refresh Header
    cwdLabel.config(text=" " + os.getcwd())
    # --Refresh Header

    # Refresh Browse
    fileSizesSum = 0
    if queryNames:  # if user gave query and pressed enter
        fileNames = queryNames
    else:
        fileNames = os.listdir(os.getcwd())
    fileTypes = [None] * len(fileNames)
    fileSizes = [None] * len(fileNames)
    fileDateModified = []
    for i in items.get_children():  # delete data from previous directory
        items.delete(i)
    for i in range(len(fileNames)):
        try:
            # modification time of file
            fileDateModified.append(
                datetime.fromtimestamp(os.path.getmtime(fileNames[i])).strftime(
                    "%Y-%m-%d %I:%M"
                )
            )
            # size of file
            fileSizes[i] = str(
                round(os.stat(fileNames[i]).st_size / 1024)
            )  # str->round->size of file in KB
            fileSizesSum += int(fileSizes[i])
            fileSizes[i] = str(fileSizes[i]) + " KB"
            #fileSizes[i] = get_size(int(fileSizes[i]))
            # check file type
            ext.extensions(fileTypes, fileNames, i)

            # insert
            if fileTypes[i] == "Directory":
                items.insert(
                    parent="",
                    index=i,
                    values=(fileNames[i], fileDateModified[i], fileTypes[i], ""),
                    image=folderIcon,
                )
            else:
                items.insert(
                    parent="",
                    index=i,
                    values=(
                        fileNames[i],
                        fileDateModified[i],
                        fileTypes[i],
                        fileSizes[i],
                    ),
                    image=fileIcon,
                )
        except:
            pass
    # --Refresh Browse

    # Draw browse
    items.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    # --Draw browse

    # Refresh Footer
    footer.config(
        text=" "
             + str(len(fileNames))
             + " items | "
             + str(round(fileSizesSum / 1024, 1))
             + " MB Total"
    )
    footer.pack(fill=tk.BOTH)
    # --Refresh Footer


def wrap_refresh(event):  # wrapper for F5 bind
    refresh([])


def previous():
    global lastDirectory
    lastDirectory = os.getcwd()
    os.chdir("../")
    refresh([])


def next():
    try:
        os.chdir(lastDirectory)
        refresh([])
    except:
        return


# open file
def onDoubleClick(event=None):
    global items
    iid = items.focus()
    # iid = items.identify_row(event.y) # old
    if iid == "":  # if double click on blank, don't do anything
        return
    for item in items.selection():
        tempDictionary = items.item(item)
        tempName = tempDictionary["values"][0]  # get first value of dictionary
    try:
        newPath = os.getcwd() + "/" + tempName
        if os.path.isdir(
                newPath
        ):  # if file is directory, open directory else open file
            os.chdir(newPath)
        else:
            os.startfile(newPath)
        refresh([])
    except:
        newPath = newPath.replace(tempName, "")
        os.chdir("../")


def onRightClick(m, event):
    selectItem(event)
    if not items.identify_row(event.y):
        m.tk_popup(event.x_root, event.y_root)
    else:
        m.tk_popup(event.x_root, event.y_root)


def search(searchEntry, event):
    fileNames = os.listdir()
    query = searchEntry.get()  # get query from text box
    query = query.lower()
    queryNames = []

    for name in fileNames:
        if name.lower().find(query) != -1:  # if query in name
            queryNames.append(name)
    refresh(queryNames)


def create_widgets(window):
    global folderIcon, fileIcon, items, cwdLabel, footer
    s = ttk.Style()
    # Browse Frame
    browseFrame = ttk.Frame(window)
    scroll = ttk.Scrollbar(browseFrame, orient="vertical")
    items = ttk.Treeview(
        browseFrame,
        columns=("Name", "Date modified", "Type", "Size"),
        yscrollcommand=scroll.set,
        height=15,
        style="Custom.Treeview",
    )
    scroll.config(command=items.yview)  # scroll with mouse drag
    # --Browse Frame

    # Footer Frame
    footerFrame = ttk.Frame(window)
    footer = ttk.Label(footerFrame)
    grip = ttk.Sizegrip(footerFrame, bootstyle="default")
    # --Footer Frame

    folderIcon = tk.PhotoImage(file=file_path + "Folder-icon.png", width=20, height=16)
    fileIcon = tk.PhotoImage(file=file_path + "File-icon.png", width=20, height=16)

    # Header Frame
    refreshIcon = tk.PhotoImage(file=file_path + "Very-Basic-Reload-icon.png")
    backArrowIcon = tk.PhotoImage(file=file_path + "Arrows-Back-icon.png")
    frontArrowIcon = tk.PhotoImage(file=file_path + "Arrows-Front-icon.png")
    headerFrame = ttk.Frame()
    cwdLabel = ttk.Label(
        headerFrame,
        text=" " + os.getcwd(),
        relief="flat",
        # width=110,
    )
    searchEntry = ttk.Entry(headerFrame, width=30, font=("TkDefaultFont", font_size))
    searchEntry.insert(0, "Search files..")
    searchEntry.bind("<Button-1>", partial(click, searchEntry))
    searchEntry.bind("<FocusOut>", partial(FocusOut, searchEntry, window))
    backButton = ttk.Button(
        headerFrame,
        image=backArrowIcon,
        command=previous,
        bootstyle="light",
    )
    forwardButton = ttk.Button(
        headerFrame,
        image=frontArrowIcon,
        command=next,
        bootstyle="light",
    )
    refreshButton = ttk.Button(
        headerFrame,
        command=partial(refresh, []),
        image=refreshIcon,
        bootstyle="light",
    )

    # tooltips for buttons
    ToolTip(backButton, text="Back", bootstyle=("default", "inverse"))
    ToolTip(forwardButton, text="Forward", bootstyle=("default", "inverse"))
    ToolTip(refreshButton, text="Refresh", bootstyle=("default", "inverse"))
    # --Header Frame

    # imgs
    open_img = Image.open(file_path + "icon.png")
    open_photo = ImageTk.PhotoImage(open_img)

    refresh_img = Image.open(file_path + "Very-Basic-Reload-icon.png")
    refresh_photo = ImageTk.PhotoImage(refresh_img)

    rename_img = Image.open(file_path + "rename.png")
    rename_photo = ImageTk.PhotoImage(rename_img)

    drive_img = Image.open(file_path + "drive.png")
    drive_photo = ImageTk.PhotoImage(drive_img)

    info_img = Image.open(file_path + "info.png")
    info_photo = ImageTk.PhotoImage(info_img)

    pie_img = Image.open(file_path + "pie.png")
    pie_photo = ImageTk.PhotoImage(pie_img)

    cpu_img = Image.open(file_path + "cpu.png")
    cpu_photo = ImageTk.PhotoImage(cpu_img)

    memory_img = Image.open(file_path + "memory.png")
    memory_photo = ImageTk.PhotoImage(memory_img)

    network_img = Image.open(file_path + "network.png")
    network_photo = ImageTk.PhotoImage(network_img)

    process_img = Image.open(file_path + "process.png")
    process_photo = ImageTk.PhotoImage(process_img)

    file_img = Image.open(file_path + "File-icon.png")
    file_photo = ImageTk.PhotoImage(file_img)

    dir_img = Image.open(file_path + "Folder-icon.png")
    dir_photo = ImageTk.PhotoImage(dir_img)

    themes_img = Image.open(file_path + "themes.png")
    themes_photo = ImageTk.PhotoImage(themes_img)

    scale_img = Image.open(file_path + "scale.png")
    scale_photo = ImageTk.PhotoImage(scale_img)

    font_img = Image.open(file_path + "font.png")
    font_photo = ImageTk.PhotoImage(font_img)

    copy_img = Image.open(file_path + "copy.png")
    copy_photo = ImageTk.PhotoImage(copy_img)

    paste_img = Image.open(file_path + "paste.png")
    paste_photo = ImageTk.PhotoImage(paste_img)

    delete_img = Image.open(file_path + "delete.png")
    delete_photo = ImageTk.PhotoImage(delete_img)

    m = ttk.Menu(window, tearoff=False, font=("TkDefaultFont", font_size))
    m.add_command(
        label="Open",
        image=open_photo,
        compound="left",
        command=onDoubleClick,
    )
    m.add_separator()

    m.add_command(
        label="Copy Selected",
        image=copy_photo,
        compound="left",
        command=copy,
    )
    m.add_command(
        label="Paste Selected", image=paste_photo, compound="left", command=paste
    )
    m.add_command(
        label="Delete selected",
        image=delete_photo,
        compound="left",
        command=del_file_popup,
    )
    m.add_command(
        label="Rename selected",
        image=rename_photo,
        compound="left",
        command=rename_popup,
    )
    m.add_separator()
    m.add_command(
        label="Refresh",
        image=refresh_photo,
        compound="left",
        command=partial(refresh, []),
    )
    # --Right click menu

    s.configure(".", font=("TkDefaultFont", font_size))  # set font size
    s.configure("Treeview", rowheight=28)  # customize treeview
    s.configure(
        "Treeview.Heading", font=("TkDefaultFont", str(int(font_size) + 1), "bold")
    )
    s.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])  # remove borders

    items.column("#0", width=40, stretch=tk.NO)
    items.column("Name", anchor=tk.W, width=150, minwidth=120)
    items.column("Date modified", anchor=tk.CENTER, width=200, minwidth=120)
    items.column("Size", anchor=tk.CENTER, width=80, minwidth=60)
    items.column("Type", anchor=tk.CENTER, width=120, minwidth=60)

    items.heading(
        "Name",
        text="Name",
        anchor=tk.W,
        command=partial(sort_col, "Name", False),
    )
    items.heading(
        "Date modified",
        text="Date modified",
        anchor=tk.CENTER,
        command=partial(sort_col, "Date modified", False),
    )
    items.heading(
        "Type",
        text="Type",
        anchor=tk.CENTER,
        command=partial(sort_col, "Type", False),
    )
    items.heading(
        "Size",
        text="Size",
        anchor=tk.CENTER,
        command=partial(sort_col, "Size", False),
    )
    items.bind(
        "<Double-1>",
        onDoubleClick,
    )  # command on double click
    items.bind("<ButtonRelease-1>", selectItem)
    items.bind("<Button-3>", partial(onRightClick, m))  # command on right click
    items.bind("<Up>", up_key)  # bind up arrow key
    items.bind("<Down>", down_key)  # bind down arrow key
    # --Browse Frame

    # Menu bar
    bar = ttk.Menu(window, font=("TkDefaultFont", font_size))
    window.config(menu=bar)

    file_menu = ttk.Menu(bar, tearoff=False, font=("TkDefaultFont", font_size))
    file_menu.add_command(
        label="Open",
        image=open_photo,
        compound="left",
        command=onDoubleClick,
    )
    file_menu.add_command(
        label="New file",
        image=file_photo,
        compound="left",
        command=new_file_popup,
    )
    file_menu.add_command(
        label="New directory", image=dir_photo, compound="left", command=new_dir_popup
    )
    file_menu.add_separator()
    file_menu.add_command(
        label="Copy Selected",
        image=copy_photo,
        compound="left",
        command=copy,
    )
    file_menu.add_command(
        label="Paste Selected", image=paste_photo, compound="left", command=paste
    )
    file_menu.add_command(
        label="Delete selected",
        image=delete_photo,
        compound="left",
        command=del_file_popup,
    )
    file_menu.add_command(
        label="Rename selected",
        image=rename_photo,
        compound="left",
        command=rename_popup,
    )
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=window.destroy)

    drives_menu = ttk.Menu(bar, tearoff=False, font=("TkDefaultFont", font_size))
    for drive in available_drives:
        drives_menu.add_command(
            label=drive,
            image=drive_photo,
            compound="left",
            command=partial(cd_drive, drive, []),
        )

    system_menu = ttk.Menu(bar, tearoff=False, font=("TkDefaultFont", font_size))
    system_menu.add_command(
        label="Drives",
        image=pie_photo,
        compound="left",
        command=partial(drive_stats, window),
    )
    system_menu.add_command(
        label="CPU", image=cpu_photo, compound="left", command=cpu_stats
    )
    system_menu.add_command(
        label="Memory", image=memory_photo, compound="left", command=memory_stats
    )
    system_menu.add_command(
        label="Network", image=network_photo, compound="left", command=network_stats
    )
    system_menu.add_command(
        label="Processes",
        image=process_photo,
        compound="left",
        command=partial(processes_win, window),
    )
    ## binwalk 메뉴 생성 ##
    binwalk_menu = ttk.Menu(bar, tearoff=False, font=("TkDefaultFont", font_size))
    binwalk_menu.add_command(
        label="Signature Scanner", image=cpu_photo, compound="left", command=binwalk_signiture_scan
    )
    binwalk_menu.add_command(
        label="Extractor", image=memory_photo, compound="left", command=binwalk_extract_file
    )
    binwalk_menu.add_command(
        label="Entropy Calculator", image=network_photo, compound="left", command=binwalk_entropy_calculate
    )
    # binwalk_menu.add_command(
    #     label="Configuration",
    #     image=process_photo,
    #     compound="left",
    #     command=partial(binwalk_config, window),  # 설정 창은 partial로 window 부모 전달
    # )

    ## 포맷 스캔 메뉴 생성 ##
    format_menu = ttk.Menu(bar, tearoff=False, font=("TkDefaultFont", font_size))
    format_menu.add_command(
        label="Format Scan", image=cpu_photo, compound="left", command=partial(checkFileSignature, window)
    )

    ## 해시 값 추출 메뉴 생성 ##
    hash_extract_menu = ttk.Menu(bar, tearoff=False, font=("TkDefaultFont", font_size))
    hash_extract_menu.add_command(
        label="HashExtract", image=info_photo, compound="left", command=partial(hashExtract, window)
    )
#####################################################################################
    virusScan_menu = ttk.Menu(bar, tearoff=False, font=("Virus_scan", font_size)) #virusScan
    virusScan_menu.add_command(
        label="VirusScan",
        compound="left",
        command=virus_scan,
    )    
    virusScan_menu.add_command(
        label="ApiKey",
        compound="left",
        command=apiKeySetting,
    )    
#####################################################################################

    sub_themes = ttk.Menu(bar, tearoff=False, font=("TkDefaultFont", font_size))
    sub_themes.add_command(label="Darkly", command=partial(write_theme, Theme.Darkly))
    sub_themes.add_command(label="Solar Dark", command=partial(write_theme, Theme.solarD))
    sub_themes.add_command(
        label="Superhero Dark", command=partial(write_theme, Theme.superheroD)
    )
    sub_themes.add_command(label="Cyborg Dark", command=partial(write_theme, Theme.CyborgD))
    sub_themes.add_command(label="Vapor Dark", command=partial(write_theme, Theme.VaporD))
    sub_themes.add_separator()
    sub_themes.add_command(label="Litera Light", command=partial(write_theme, Theme.literaL))
    sub_themes.add_command(label="Minty Light", command=partial(write_theme, Theme.mintyL))
    sub_themes.add_command(label="Morph Light", command=partial(write_theme, Theme.morphL))
    sub_themes.add_command(label="Yeti Light", command=partial(write_theme, Theme.yetiL))

    sub_font_size = ttk.Menu(bar, tearoff=False, font=("TkDefaultFont", font_size))
    sub_font_size.add_command(label="14", command=partial(change_font_popup, 14))
    sub_font_size.add_command(label="12", command=partial(change_font_popup, 12))
    sub_font_size.add_command(label="11", command=partial(change_font_popup, 11))
    sub_font_size.add_command(
        label="10 - default", command=partial(change_font_popup, 10)
    )
    sub_font_size.add_command(label="9", command=partial(change_font_popup, 9))
    sub_font_size.add_command(label="8", command=partial(change_font_popup, 8))
    sub_font_size.add_command(label="7", command=partial(change_font_popup, 7))

    sub_scale = ttk.Menu(bar, tearoff=False, font=("TkDefaultFont", font_size))
    sub_scale.add_command(label="150%", command=partial(change_scale, 1.5, s))
    sub_scale.add_command(label="125%", command=partial(change_scale, 1.25, s))
    sub_scale.add_command(label="100%", command=partial(change_scale, 1.0, s))
    sub_scale.add_command(label="75%", command=partial(change_scale, 0.75, s))
    sub_scale.add_command(label="50%", command=partial(change_scale, 0.5, s))

    preferences_menu = ttk.Menu(bar, tearoff=False, font=("TkDefaultFont", font_size))
    preferences_menu.add_cascade(
        label="Themes", image=themes_photo, compound="left", menu=sub_themes
    )
    preferences_menu.add_cascade(
        label="Scale", image=scale_photo, compound="left", menu=sub_scale
    )
    preferences_menu.add_cascade(
        label="Font size", image=font_photo, compound="left", menu=sub_font_size
    )

    help_menu = ttk.Menu(bar, tearoff=False, font=("TkDefaultFont", font_size))
    help_menu.add_command(
        label="Keybinds", image=info_photo, compound="left", command=keybinds
    )

    about_menu = ttk.Menu(bar, tearoff=False, font=("TkDefaultFont", font_size))
    about_menu.add_command(
        label="About the app", command=about_popup, image=info_photo, compound="left"
    )

    bar.add_cascade(label="File", menu=file_menu, underline=0)
    bar.add_cascade(label="Drives", menu=drives_menu, underline=0)
    bar.add_cascade(label="System", menu=system_menu, underline=0)
    bar.add_cascade(label="Binwalk", menu=binwalk_menu, underline=0)  # binwalk 상단바
    bar.add_cascade(label="Format", menu=format_menu, underline=0)  # format scan 상단바
    bar.add_cascade(label="HashExtract", menu=hash_extract_menu, underline=0)  # format scan 상단바
    bar.add_cascade(label="Preferences", menu=preferences_menu, underline=0)
    bar.add_cascade(label="Help", menu=help_menu, underline=0)
    bar.add_cascade(label="About", menu=about_menu, underline=0)
    bar.add_cascade(label="VirusScan", menu=virusScan_menu,underline=0) #virusScan

    # --Menu bar

    # packs
    scroll.pack(side=tk.RIGHT, fill=tk.BOTH)
    backButton.pack(side=tk.LEFT, padx=5, pady=10, fill=tk.BOTH)
    forwardButton.pack(side=tk.LEFT, padx=5, pady=10, fill=tk.BOTH)
    cwdLabel.pack(side=tk.LEFT, padx=5, pady=10, fill=tk.BOTH, expand=True)
    refreshButton.pack(side=tk.LEFT, padx=1, pady=10, fill=tk.BOTH)
    searchEntry.pack(side=tk.LEFT, padx=5, pady=10, fill=tk.BOTH)
    grip.pack(side=tk.RIGHT, fill=tk.BOTH, padx=2, pady=2)

    headerFrame.pack(fill=tk.X)
    browseFrame.pack(fill=tk.BOTH, expand=True)
    footerFrame.pack(side=tk.BOTTOM, fill=tk.BOTH)

    searchEntry.bind(
        "<Return>",
        partial(search, searchEntry),
    )  # on enter press, run search1

    # img references
    photo_ref.append(backArrowIcon)
    photo_ref.append(frontArrowIcon)
    photo_ref.append(refreshIcon)
    photo_ref.append(open_photo)
    photo_ref.append(refresh_photo)
    photo_ref.append(rename_photo)
    photo_ref.append(drive_photo)
    photo_ref.append(info_photo)
    photo_ref.append(pie_photo)
    photo_ref.append(cpu_photo)
    photo_ref.append(memory_photo)
    photo_ref.append(network_photo)
    photo_ref.append(process_photo)
    photo_ref.append(file_photo)
    photo_ref.append(dir_photo)
    photo_ref.append(themes_photo)
    photo_ref.append(scale_photo)
    photo_ref.append(font_photo)
    photo_ref.append(copy_photo)
    photo_ref.append(paste_photo)
    photo_ref.append(delete_photo)

    # wrappers for keybinds
    window.bind("<F5>", wrap_refresh)
    window.bind("<Delete>", wrap_del)
    window.bind("<Control-c>", wrap_copy)
    window.bind("<Control-v>", wrap_paste)
    window.bind("<Control-Shift-N>", wrap_new_dir)


def sort_col(col, reverse):
    global items
    l = [(items.set(k, col), k) for k in items.get_children("")]
    if col == "Name":
        l.sort(reverse=reverse)
    elif col == "Date modified":
        l = time_heap_sort(l, reverse=reverse)
    elif col == "Size":
        l = size_heap_sort(l, reverse=reverse)
    elif col == "Type":
        l = heap_sort(l, reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        items.move(k, "", index)

    # reverse sort next time
    items.heading(col, command=partial(sort_col, col, not reverse))


def sort_key_dates(item):
    return datetime.strptime(item[0], "%Y-%m-%d %I:%M")


def sort_key_size(item):
    num_size = item[0].split(" ")[0]
    if num_size != "":
        return int(num_size)
    else:
        return -1  # if it's a directory, give it negative size value, for sorting


def write_theme(theme):
    with open(file_path + "../res/theme.txt", "w") as f:  # closes file automatically
        f.write(theme)
    warning_popup()


def warning_popup():
    Messagebox.show_info(
        message="Please restart the application to apply changes.", title="Info"
    )


def change_font_popup(size):
    warning_popup()
    change_font_size(size)


def change_font_size(size):
    with open(file_path + "../res/font.txt", "w") as f:  # closes file automatically
        f.write(str(size))


def change_scale(multiplier, s):
    scale = round(multiplier * 28)  # 28 is default
    s.configure("Treeview", rowheight=scale)


def drive_stats(window):
    top = ttk.Toplevel(window)
    top.resizable(False, False)
    top.iconphoto(False, tk.PhotoImage(file=file_path + "info.png"))
    top.title("Drives")

    meters = []
    for drive in available_drives:
        meters.append(
            ttk.Meter(
                top,
                bootstyle="default",
                metersize=180,
                padding=5,
                metertype="semi",
                subtext="GB Used",
                textright="/ "
                          + str(
                    round(psutil.disk_usage(drive).total / (1024 * 1024 * 1024))
                ),  # converts bytes to GB
                textleft=drive,
                interactive=False,
                amounttotal=round(
                    psutil.disk_usage(drive).total / (1024 * 1024 * 1024)
                ),  # converts bytes to GB
                amountused=round(
                    psutil.disk_usage(drive).used / (1024 * 1024 * 1024)
                ),  # converts bytes to GB
            )
        )
    top.geometry(str(len(meters) * 200) + "x200")  # Add 200px width for every drive
    for meter in meters:
        meter.pack(side=tk.LEFT, expand=True, fill=tk.X)


def cpu_stats():
    cpu_count_log = psutil.cpu_count()
    cpu_count = psutil.cpu_count(logical=False)
    cpu_per = psutil.cpu_percent()
    cpu_freq = round(psutil.cpu_freq().current / 1000, 2)
    Messagebox.ok(
        message="Usage: "
                + str(cpu_per)
                + "%"
                + "\nLogical Processors: "
                + str(cpu_count)
                + "\nCores: "
                + str(cpu_count_log)
                + "\nFrequency: "
                + str(cpu_freq)
                + " GHz",
        title="CPU",
    )

def memory_stats():
    memory_per = psutil.virtual_memory().percent
    memory_total = round(psutil.virtual_memory().total / (1024 * 1024 * 1024), 2)
    memory_used = round(psutil.virtual_memory().used / (1024 * 1024 * 1024), 2)
    memory_avail = round(psutil.virtual_memory().available / (1024 * 1024 * 1024), 2)
    Messagebox.ok(
        message="Usage: "
                + str(memory_per)
                + "%"
                + "\nTotal: "
                + str(memory_total)
                + " GB"
                + "\nUsed: "
                + str(memory_used)
                + " GB"
                + "\nAvailable: "
                + str(memory_avail)
                + " GB",
        title="Memory",
    )


def network_stats():
    net = psutil.net_io_counters(pernic=True)
    mes = ""
    for key, value in net.items():
        mes += (
                str(key)
                + ":\n"
                + "Sent: "
                + str(round(value.bytes_sent / (1024 * 1024 * 1024), 2))
                + " GB\n"
                + "Received: "
                + str(round(value.bytes_recv / (1024 * 1024 * 1024), 2))
                + " GB\n\n"
        )
    Messagebox.ok(message=mes, title="Network")


def processes_win(window):
    top = ttk.Toplevel(window)
    top.geometry("1024x600")
    top.resizable(True, True)
    top.iconphoto(False, tk.PhotoImage(file=file_path + "process.png"))
    top.title("Processes")
    scroll = ttk.Scrollbar(top, orient="vertical")

    processes_list = []
    for i in psutil.pids():
        p = psutil.Process(i)
        processes_list.append(
            (p.name(), p.pid, p.status(), str(round(p.memory_info().rss / 1024)) + "KB")
        )

    processes = ttk.Treeview(
        top,
        columns=("Name", "PID", "Status", "Memory"),
        yscrollcommand=scroll.set,
        style="Custom.Treeview",
    )
    for p in processes_list:
        processes.insert(parent="", index=0, values=p)
    processes.heading("Name", text="Name", anchor="w")
    processes.heading("PID", text="PID", anchor="w")
    processes.heading("Status", text="Status", anchor="w")
    processes.heading("Memory", text="Memory", anchor="w")
    scroll.config(command=processes.yview)
    scroll.pack(side=tk.RIGHT, fill=tk.BOTH)
    processes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


def cd_drive(drive, queryNames):
    global fileNames, currDrive, cwdLabel
    cwdLabel.config(text=" " + drive)
    currDrive = drive
    fileNames = os.listdir(currDrive)
    os.chdir(currDrive + "/")
    refresh(queryNames)


def up_key(event):
    global selectedItem, items
    iid = items.focus()
    iid = items.prev(iid)
    if iid:
        items.selection_set(iid)
        selectedItem = items.item(iid)["values"][0]
        print(selectedItem)
    else:
        pass



def down_key(event):
    global selectedItem, items
    iid = items.focus()
    iid = items.next(iid)
    if iid:
        items.selection_set(iid)
        selectedItem = items.item(iid)["values"][0]
        print(selectedItem)
    else:
        pass


def click(searchEntry, event):
    if searchEntry.get() == "Search files..":
        searchEntry.delete(0, "end")


def FocusOut(searchEntry, window, event):
    searchEntry.delete(0, "end")
    searchEntry.insert(0, "Search files..")
    window.focus()


def rename_popup():
    global items
    if items.focus() != "":
        try:
            name = Querybox.get_string(prompt="Name: ", title="Rename")
            old = os.getcwd() + "/" + selectedItem
            os.rename(old, name)
            refresh([])
        except:
            pass
    else:
        Messagebox.show_info(
            message="There is no selected file or directory.", title="Info"
        )


def selectItem(event):
    global selectedItem, items, selectedItem_list
    iid = items.identify_row(event.y)

    if not iid:
        items.selection_remove(items.selection())
        items.focus('')
        selectedItem_list.clear()
        selectedItem = None
        return
    if event.state & 0x4:  # Ctrl 키가 눌려 있는지 확인합니다.
        # Ctrl 키가 눌려 있으면 선택 목록에 추가합니다.
        if iid:
            items.selection_add(iid)
            selectedItem = items.item(iid)["values"][0]
            items.focus(iid)  # iid에 포커스를 줍니다.
            selectedItem = str(selectedItem)

            #중복시 제거
            if os.path.join(os.getcwd(), selectedItem) in selectedItem_list:
                selectedItem_list.remove(os.path.join(os.getcwd(), selectedItem))
                items.selection_remove(iid)
            else:
                selectedItem_list.append(os.path.join(os.getcwd(), selectedItem))
        else:
            items.selection_clear()
            selectedItem_list.clear()
            pass
    elif event.state & 0x1:  # Shift 키가 눌려 있는지 확인합니다.
        # Shift 키가 눌려 있으면 정렬된 순서대로 항목 범위를 선택합니다.
        current_selection = items.selection()
        if current_selection:
            # 첫 번째와 마지막으로 선택된 항목을 가져옵니다.
            first_selected = current_selection[0]
            last_selected = current_selection[-1]

            # 첫 번째와 마지막으로 선택된 항목의 인덱스를 가져옵니다.
            first_index = items.index(first_selected)
            last_index = items.index(last_selected)
            # 첫 번째와 마지막으로 선택된 항목 사이의 항목 범위를 선택합니다.
            selected_range = items.get_children()[first_index:last_index + 1]
            items.selection_add(selected_range)
            for item in selected_range:
                selectedItem = items.item(item)["values"][0]
                selectedItem_list.append(os.path.join(os.getcwd(), selectedItem))
    else:
        # Ctrl 키가 눌려 있지 않으면 이전 선택을 지우고 현재 항목을 선택합니다.
        if iid:
            items.selection_set(iid)
            selectedItem = items.item(iid)["values"][0]
            items.focus(iid)  # Give focus to iid
            selectedItem_list.clear()
            selectedItem = str(selectedItem)
            selectedItem_list.append(os.path.join(os.getcwd(), selectedItem))
        else:
            pass

def keybinds():
    Messagebox.ok(
        message="Copy - <Control + C>\nPaste - <Control + V>\nDelete - <Del>\n"
                + "New Directory - <Control + Shift + N>\nRefresh - <F5>\n"
                + "Select up - <Arrow key up>\nSelect down - <Arrow key down>",
        title="Info",
    )


def about_popup():  # popup window
    Messagebox.ok(
        message="My File Explorer\nMade by: Chris Tsouchlakis\nVersion 0.5.1",
        title="About",
    )


def new_file_popup():
    name = Querybox.get_string(prompt="Name: ", title="New file")
    if name != "":
        try:
            f = open(os.getcwd() + "/" + name, "x")
            f.close()
            refresh([])
        except:
            pass


def new_dir_popup():
    name = Querybox.get_string(prompt="Name: ", title="New directory")
    if name != "":
        try:
            os.mkdir(os.getcwd() + "/" + name)
            refresh([])
        except:
            pass


def wrap_new_dir(event):
    new_dir_popup()


def copy():
    global src, items
    global selectedItem_list, src_list
    if selectedItem_list:  # 복사할 항목이 있는지 확인합니다.
        for selected_item in selectedItem_list:
            print(f"{selected_item}을(를) 대상지로 복사하는 중...")

        src_list = selectedItem_list
        # 복사 후 복사한 항목 리스트를 비웁니다.
        selected_item = []
        selectedItem_list = []

    else:
        print("복사할 항목이 선택되지 않았습니다.")


def wrap_copy(event):  # wrapper for ctrl+c keybinds
    copy()


def wrap_paste(event):  # wrapper for ctrl+v keybinds
    paste()


def paste():
    global src
    global src_list
    dest = os.getcwd() + "/"
    print(src_list)
    if src_list:  # 붙여넣을 항목이 있는지 확인합니다.
        for src in src_list:
            if not os.path.isdir(src) and src != "":
                try:
                    t1 = threading.Thread(
                        target=shutil.copy2, args=(src, dest)
                    )  # use threads so gui does not hang on large file copy
                    t1.start()
                    refresh([])
                except:
                    pass
            elif os.path.isdir(src) and src != "":
                try:
                    new_dest_dir = os.path.join(dest, os.path.basename(src))
                    os.makedirs(new_dest_dir)
                    t1 = threading.Thread(  # use threads so gui does not hang on large directory copy
                        target=shutil.copytree,
                        args=(src, new_dest_dir, False, None, shutil.copy2, False, True),
                    )
                    t1.start()
                    refresh([])
                except:
                    pass

        # 붙여넣기 후 소스 항목 리스트를 비웁니다.
        src_list = []
        refresh([])
    else:
        print("붙여넣을 항목이 없습니다.")
    refresh([])


def del_file_popup():
    global items, selectedItem_list
    print(selectedItem_list)

    if selectedItem_list:  # if there is a focused item
        answer = Messagebox.yesno(
            message="선택된 파일/폴더를 삭제하시겠습니까?",
            alert=True,
        )
        if answer == "Yes":
            for selected_item in selectedItem_list:
                del_file(selected_item)
                refresh([])
            refresh([])
        else:
            return
    else:
        Messagebox.show_info(
            message="삭제할 항목이 선택되지 않았습니다.", title="Info"
        )


def wrap_del(event):  # wrapper for delete keybind
    del_file_popup()


def del_file(selected_item):
    if os.path.isfile(selected_item):
        os.remove(selected_item)
    elif os.path.isdir(selected_item):
        shutil.rmtree(selected_item)


def read_theme():
    global theme, file_path
    with open(file_path + "../res/theme.txt") as f:  # closes file automatically
        theme = f.readline()
    if theme == "":  # if theme.txt is empty, set default theme
        theme = Theme.literaL


def read_font():
    global font_size
    with open(file_path + "../res/font.txt") as f:  # closes file automatically
        font_size = f.readline()
    if font_size == "":  # if font.txt is empty, set default font
        font_size = 10

#virusScan
def apiKeySetting():
    apiKeyResult = simpledialog.askstring("Input", "Please enter your VirusTotal API key:")
    if apiKeyResult!=None:
        f=open(script_folder+"/"+'apiKey.txt',mode='w')
        f.write(apiKeyResult)
        f.close()
def get_api_key():
    apiKeyFile='apiKey.txt'
    if os.path.exists(script_folder+"/"+'apiKey.txt'):
        f=open(script_folder+"/"+'apiKey.txt',mode='r')
        apiKeyResult=f.read()
        f.close()
        return apiKeyResult
    else:
        apiKeyResult = simpledialog.askstring("Input", "Please enter your VirusTotal API key:")
        if apiKeyResult!=None:
            f=open(script_folder+"/"+'apiKey.txt',mode='w')
            f.write(apiKeyResult)
            f.close()
            return apiKeyResult
        else:
            return apiKeyResult
def virus_scan():
    global selectedItem_list
    if len(selectedItem_list)==1:
        upload_url = 'https://www.virustotal.com/vtapi/v2/file/scan'
        api_key = get_api_key()
        if api_key !=None:    
            file_path = os.path.join(os.getcwd(), selectedItem_list[0])
            report_url = 'https://www.virustotal.com/vtapi/v2/file/report'
            upload_files = {'file': (file_path, open(file_path, 'rb'))}
            upload_params = {'apikey': api_key}

            try:
                upload_response = requests.post(upload_url, files=upload_files, params=upload_params)

                if upload_response.status_code == 200:
                    upload_result = upload_response.json()
                    scan_id = upload_result.get('scan_id')

                    if scan_id:
                        messagebox.showinfo("Success", f"File uploaded successfully.")
                        time.sleep(10)

                        report_params = {'apikey': api_key, 'resource': scan_id}
                        report_response = requests.get(report_url, params=report_params)

                        if report_response.status_code == 200:
                            report_result = report_response.json()

                            if 'scans' in report_result:
                                count = 0
                                str_msg=""
                                for antivirus, scan_result in report_result['scans'].items():
                                    if scan_result['detected']:
                                        str_msg+=f"{antivirus}: Detected\n Result: {scan_result['result']}\n"
                                        count += 1
                                tk.messagebox.showinfo("Scan Result", str_msg)

                                if count == 0:
                                    tk.messagebox.showinfo("Scan Result", "Not detected")
                            else:
                                tk.messagebox.showinfo("Scan Result", "No scan results found.")
                        else:
                            tk.messagebox.showerror("Error", f"Error getting scan results: {report_response.status_code} - {report_response.text}")
                    else:
                        tk.messagebox.showinfo("Error", "No scan ID found in the upload response.")
                else:
                    tk.messagebox.showerror("Error", f"Error uploading file: {upload_response.status_code} - {upload_response.text}")

            except Exception as e:
                tk.messagebox.showerror("Error", f"An error occurred: {str(e)}")
        else:
            tk.messagebox.showerror("Error","ApiKey를 입력 해주세요")
    else:
        tk.messagebox.showerror("Error","virusScan은 한개의 파일만 선택가능합니다")

def main():
    global file_path
    file_path = os.path.join(os.path.dirname(__file__), "../icons/")
   
    checkPlatform()
    read_theme()
    read_font()
    root = createWindow()
    create_widgets(root)
    refresh([])
    root.mainloop()

if __name__ == "__main__":
    main()
