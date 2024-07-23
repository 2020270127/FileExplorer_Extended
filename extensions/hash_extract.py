import os
import hashlib
from extensions.config import *
from tkinter import Toplevel, Label
from ttkbootstrap.dialogs.dialogs import Messagebox

def hashExtract(window):
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
