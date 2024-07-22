import util
import queue
import threading
import tkinter as tk
from tkinter import Toplevel, scrolledtext
from config import *



class BinwalkWindow:
    def __init__(self):
        self.binwalk_result = []
        self.binwalk_result_queue = queue.Queue() 

    def __call__(self, func):
        def wrapper():
            self.binwalk_result.clear()

            binwalk_process_window = Toplevel()
            binwalk_process_window.title("Working Status")
            binwalk_process_window.attributes('-topmost', True)
            binwalk_process_area = scrolledtext.ScrolledText(binwalk_process_window, wrap=tk.WORD, width=80, height=20)
            binwalk_process_area.pack(padx=10, pady=10)

            binwalk_result_window = Toplevel()
            binwalk_result_window.title("Result")
            binwalk_result_window.withdraw()
            binwalk_result_area = scrolledtext.ScrolledText(binwalk_result_window, wrap=tk.WORD, width=80, height=20)
            binwalk_result_area.pack(padx=10, pady=10)

            def update_result_window():
                binwalk_result_window.deiconify()
                for result in self.binwalk_result:
                    binwalk_result_area.insert(tk.END, result + '\n')
                binwalk_result_area.configure(state='disabled')

            threading.Thread(target=lambda: func(self.binwalk_result, self.binwalk_result_queue)).start()

            def update_loop():
                while True:
                    try:
                        message = self.binwalk_result_queue.get_nowait()
                    except queue.Empty:
                        break
                    binwalk_process_area.insert(tk.END, message + '\n')
                    binwalk_process_area.yview(tk.END)
                    if message == "job end":
                        update_result_window()
                        binwalk_process_window.destroy()
                        return
                binwalk_result_window.after(100, update_loop)
            update_loop()
        return wrapper

@BinwalkWindow()  
def binwalk_signiture_scan(binwalk_result, q):  
    for file in selectedItem_list:
        print(file)
        q.put("Scanning " + f'{file}' + " ...")
        util.append_binwalk_result('-B', file, binwalk_result)  
    q.put("job end")

@BinwalkWindow()
def binwalk_extract_file(binwalk_result, q):
    for file in selectedItem_list:
        q.put("Extracting " + f'{file}' + " ...")
        util.append_binwalk_result('-e', file, binwalk_result)
    q.put("job end")


@BinwalkWindow()
def binwalk_entropy_calculate(binwalk_result, q):
    for file in selectedItem_list:
        q.put("Analyzing " + f'{file}' + " ...")
        util.append_binwalk_result('-E', file, binwalk_result)
    q.put("job end")
