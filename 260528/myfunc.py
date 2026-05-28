def myfunc(name,age):
    print(f"姓名: {name}, 年齡: {age}")


def myfunc2(name="請輸入姓名",age = 99):
    print(f"姓名: {name}, 年齡: {age}")

def add(a, b):
    return a + b

# 回傳多個值（以元組形式）
def min_max(numbers):
    return min(numbers), max(numbers)
def add(a, b):
    return a + b

# 回傳多個值（以元組形式）
def min_max(numbers):
    return min(numbers), max(numbers)

def total(*args):
    print(args)

def myfunc5(**kwargs):
    print(kwargs)

low, high = min_max([3, 1, 4, 1, 5, 9])
low, high = min_max([3, 1, 4, 1, 5, 9])

print(add(10, 20))  # 輸出: 5
total(1, 2, 3, 4, 5)
total(10, 20, 30)

myfunc5(arg1=1, arg2=2, mname=3, anything=5)

count = 0    # 全域變數

def increment():
    #count += 1 #區域變數
    count = 100
    print("count inside func:", count)    # 100

def myfunc():
    global count
    count += 300
increment()
print(count)    # 1
myfunc()
print("被函式中的全域乎收變更後的值:", count)    # 301

square = lambda x: x ** 2
add = lambda a, b: a + b

students = [("Alice", 90), ("Bob", 75), ("Charlie", 88)]
sorted_students = sorted(students, key=lambda s: s[1], reverse=True)
sorted_students2 = sorted(students, key=lambda s: s[1], reverse=True)
print(students)
print(sorted_students)

import os
print(os.getcwd()) #取得目前python執行環境當前資料夾
print(os.listdir(".")) #取得當前資料夾的檔案內容(包含一般資料夾,及一般檔案)
os.makedirs("folder", exist_ok=True)#建立資料夾
print(os.path.exists("file.txt"))#目前路徑有沒有在file.txt

# 檢查目前使用者對某個檔案的實際權限
print(os.access("file.txt", os.R_OK))    # True = 可讀
print(os.access("file.txt", os.W_OK))    # True = 可寫
print(os.access("file.txt", os.X_OK))    # True = 可執行

import sys
print(sys.argv)       # 命令列引數串列，sys.argv[0] 為腳本名稱
print(sys.version)
print(sys.platform)

from pathlib import Path

# 建立路徑物件
p = Path("data/output.txt")

print(p.name)       # output.txt
print(p.stem)       # output
print(p.suffix)     # .txt
print(p.parent)     # data

# 組合路徑
base = Path("data")
file = base / "report" / "summary.csv"    # data/report/summary.csv

# 建立目錄
Path("output").mkdir(parents=True, exist_ok=True)

# 確認存在
print(Path("data.txt").exists())

# 判斷是檔案或資料夾
print(Path("data.txt").is_file())    # True = 是檔案
print(Path("output").is_dir())       # True = 是資料夾

# 取得檔案詳細資訊（stat）
p = Path("output/data.txt")
print(p.stat().st_size)              # 檔案大小（位元組）
size_kb = p.stat().st_size / 1024    # 轉換為 KB

# 列出目錄內容
for f in Path(".").iterdir():
    #print(f)
    pass
# 依副檔名篩選
for f in Path(".").glob("*.txt"):
    print(f)
    pass