"""
Author: jeungsin00
"""
import os
import time
import requests
import tkinter as tk
from tkinter import messagebox, simpledialog

script_path = os.path.abspath(__file__) # virusScan apiKey.txt 생성 위치 지정을 위한 변수
script_folder = os.path.dirname(script_path) #virusScan apiKey.txt 생성 위치 지정을 위한 변수

#virusScan
def apiKeySetting():
    apiKeyResult = simpledialog.askstring("Input", "Please enter your VirusTotal API key:")
    if apiKeyResult!=None:
        f=open(script_folder+"/"+'apiKey.txt',mode='w')
        f.write(apiKeyResult)
        f.close()

def get_api_key():
    if os.path.exists(script_folder+"/"+'apiKey.txt'):
        f=open(script_folder+"/"+'apiKey.txt',mode='r')
        apiKeyResult=f.read()
        f.close()
        return apiKeyResult
    else:
        apiKeyResult = simpledialog.askstring("Input", "Please enter your VirusTotal API key:")
        try:
            f=open(script_folder+"/"+'apiKey.txt',mode='w')
            f.write(apiKeyResult)
            f.close()
            return apiKeyResult
        except:
            raise "opening key error"
        
def virus_scan(selectedItem_list):
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
