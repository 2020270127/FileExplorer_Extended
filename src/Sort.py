import enum
import os
import shutil
import requests
from datetime import datetime

'''
* Lib name : Sort

* Description : sort 함수를 동작하기 위해 필요한 함수들의 집합

* Change Date : 2023. 10. 08

* Version : 0.2                

'''

class size_sort:
    
    def size_list_files_in_current_dir(self, current_dir):
        files = []
        for entry in os.scandir(current_dir):
            if entry.is_file():
                file_name = entry.name
                file_size = entry.stat().st_size
                files.append((file_name, file_size))
        
        return files

    def ascending_heapify(self, arr, n, i):
        largest = i
        left_child = 2 * i + 1
        right_child = 2 * i + 2

        if left_child < n and arr[i][1] < arr[left_child][1]:
            largest = left_child

        if right_child < n and arr[largest][1] < arr[right_child][1]:
            largest = right_child

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            self.ascending_heapify(arr, n, largest)

    def heap_sort_by_size(self,files):
        n = len(files)

        for i in range(n // 2 - 1, -1, -1):
            self.ascending_heapify(files, n, i)

        for i in range(n - 1, 0, -1):
            files[i], files[0] = files[0], files[i]
            self.ascending_heapify(files, i, 0)

        return files
    
    def get_size(self, filesize):
        # Not Using SI Standard (1kb = 1024byte)
        if(0< filesize < 1024):
            print(f'{filesize}bytes')
        elif (1024<= filesize<1024**2):
            print(f'{round(filesize/1024,2)}KB')
        elif (1024**2<= filesize<1024**3):
            print(f'{round(filesize/(1024**2),2)}MB')
        elif (1024**3<= filesize<1024**4):
            print(f'{round(filesize/(1024**3),2)}GB')
        else:
            print(f'{filesize}byte')

class time_sort:

    def descending_heapify(self,arr, n, i):
        largest = i
        left_child = 2 * i + 1
        right_child = 2 * i + 2

        if left_child < n and arr[i][1] > arr[left_child][1]:
            largest = left_child

        if right_child < n and arr[largest][1] > arr[right_child][1]:
            largest = right_child

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            self.descending_heapify(arr, n, largest)

    def time_list_files_in_current_dir(self, current_dir):
        files = []
        for entry in os.scandir(current_dir):
            if entry.is_file():
                file_name = entry.name
                file_created_time = entry.stat().st_ctime
                created_time_str = datetime.utcfromtimestamp(file_created_time).strftime('%Y-%m-%d %H:%M:%S')
                files.append((file_name, created_time_str))
        
        return files

    def heap_sort_by_created_time(self,files):
        n = len(files)

        for i in range(n // 2 - 1, -1, -1):
            self.descending_heapify(files, n, i)

        for i in range(n - 1, 0, -1):
            files[i], files[0] = files[0], files[i]
            self.descending_heapify(files, i, 0)

        return files
    
class name_sort:

    def sort_files_by_name(slef, directory):
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

        sorted_files = sorted(files)

        return sorted_files

def upload_and_get_scan_results(file_name):
    upload_url = f'https://www.virustotal.com/vtapi/v2/file/scan'
    api_key = 'api 키 입력'
    file_path=os.getcwd()
    file_path+="/"+file_name
    report_url = f'https://www.virustotal.com/vtapi/v2/file/report'

    upload_files = {'file': (file_path, open(file_path, 'rb'))}
    upload_params = {'apikey': api_key}

    try:
        upload_response = requests.post(upload_url, files=upload_files, params=upload_params)

        if upload_response.status_code == 200:
            upload_result = upload_response.json()
            scan_id = upload_result.get('scan_id')
            if scan_id:
                print(f"File uploaded successfully. Scan ID: {scan_id}")

                report_params = {'apikey': api_key, 'resource': scan_id}
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
