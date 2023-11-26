import enum
import os
import shutil
import heapq
import random
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

'''
def sort_key_size(item):
    if(item == "..." or ""):
        return -1
    else:
        num_size = item.split(" ")[0]
        unit = item.split(" ")[1]

        if num_size != "":
            if unit == 'KB':
                return int(num_size)
            elif unit == 'MB':
                return int(num_size) * 1024
            elif unit == 'GB':
                return int(num_size) * (1024**2)
            elif unit == 'TB':
                return int(num_size) * (1024**3)
        else:
            return -1

def get_size(filesize): 
        # Not Using SI Standard (1kb = 1024byte)
        if(0< filesize < 1024):
            return str(filesize)+' KB' 
        elif (1024<= filesize<1024**2):
            return str(round(filesize/1024,2))+' MB'
        elif (1024**2<= filesize<1024**3):
            return str(round(filesize/(1024**2),2))+' GB'
        elif (1024**3<= filesize<1024**4):
            return str(round(filesize/(1024**3),2))+' TB'
        else:
            return ''

'''
def sort_key_size(item):
    num_size = item[0].split(" ")[0]
    if num_size != "":
        return int(num_size)
    else:
        return -1 
          
def max_heapify(unsorted, index, heap_size):
    largest = index
    left_index = 2 * index + 1
    right_index = 2 * index + 2
    if left_index < heap_size and unsorted[left_index] < unsorted[largest]:
        largest = left_index

    if right_index < heap_size and unsorted[right_index] < unsorted[largest]:
        largest = right_index

    if largest != index:
        unsorted[largest], unsorted[index] = unsorted[index], unsorted[largest]
        max_heapify(unsorted, largest, heap_size)

def min_heapify(unsorted, index, heap_size):
    largest = index
    left_index = 2 * index + 1
    right_index = 2 * index + 2
    if left_index < heap_size and unsorted[left_index] > unsorted[largest]:
        largest = left_index

    if right_index < heap_size and unsorted[right_index] > unsorted[largest]:
        largest = right_index

    if largest != index:
        unsorted[largest], unsorted[index] = unsorted[index], unsorted[largest]
        min_heapify(unsorted, largest, heap_size)

def heap_sort(unsorted,reverse:bool = False):
    if(not reverse):
        n = len(unsorted)
        for i in range(n // 2 - 1, -1, -1):
            max_heapify(unsorted, i, n)
        for i in range(n - 1, 0, -1):
            unsorted[0], unsorted[i] = unsorted[i], unsorted[0]
            max_heapify(unsorted, 0, i)
        return unsorted
    else:
        n = len(unsorted)
        for i in range(n // 2 - 1, -1, -1):
            min_heapify(unsorted, i, n)
        for i in range(n - 1, 0, -1):
            unsorted[0], unsorted[i] = unsorted[i], unsorted[0]
            min_heapify(unsorted, 0, i)
        return unsorted

def time_heap_sort(lis, reverse: bool = False):

    for i in range(len(lis)):
        tmp = int((datetime.strptime(lis[i][0],"%Y-%m-%d %I:%M")).timestamp())
        lis[i] = (tmp,lis[i][1])

    lis = heap_sort(lis,reverse)

    for i in range(len(lis)):
        tmp = datetime.fromtimestamp(lis[i][0]).strftime("%Y-%m-%d %I:%M")
        lis[i] = (tmp,lis[i][1])

    return lis

def size_heap_sort(lis, reverse: bool = False):

    for i in range(len(lis)):
        tmp = sort_key_size(lis[i])
        lis[i] = (tmp,lis[i][1])

    lis = heap_sort(lis,reverse)

    for i in range(len(lis)):
        tmp = str(lis[i][0]) + " KB"
        lis[i] = (tmp,lis[i][1])
    
    return lis
