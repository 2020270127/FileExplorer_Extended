# 출력문자 색상 변경
formatters = {
    'Red': '\033[91m',
    'Green': '\033[92m',
    'Blue': '\033[94m',
    'END': '\033[0m'
}

# 색을 입혀 출력하는 함수
def printlog(content, color):
    if color == 'Green':
        print('{Green}'.format(**formatters) + str(content) + '{END}'.format(**formatters))
    elif color == 'Blue':
        print('{Blue}'.format(**formatters) + str(content) + '{END}'.format(**formatters))
    else:
        print('{Red}'.format(**formatters) + str(content) + '{END}'.format(**formatters))
