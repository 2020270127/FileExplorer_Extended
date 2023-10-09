import requests
import os
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


file_path = 'test.py'

upload_and_get_scan_results(file_path)