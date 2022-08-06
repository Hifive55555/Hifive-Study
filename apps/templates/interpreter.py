# -*- coding:utf-8 -*-

# URL_FOR INTERPRETER 是用于将标准html文件转义为路径为url_for的html文件, 方便flask开发者快速添加url_for重定向
# 开发者: Hifive; GitHub: Hifive55555
# Version: 2.0.1 Beta 注释版
# 此版本包括由Tk编写的UI程序、cmd程序、以及API接口 (Python库)

# 更新日志
# 1.0.0 Beta 2022/1 UFI横空出世，推出核心功能
# 1.1.0 Beta 2022/1 增加UI界面
# 2.0.1 Beta 2022/8/5 重修代码，增加注释，逻辑业务分离

import re
import os
import tkinter as tk
from tkinter import filedialog


def main(origin_text: str) -> str:
    """ 主逻辑函数，每次只进行一次操作 """

    # 添加 url_for 的函数
    def add(match) -> str:
        address = match.group()
        addition = r"{{ url_for('static', filename='" + address + r"') }}"
        return addition

    # 替换目录字符
    x = re.sub(r"/?(\w[\u4E00-\u9FA5\w_-]+/)+([\u4E00-\u9FA5\w_-]+\.)+\w+\b", add, origin_text)
    return x


def file_catcher(file_name, prefix, *paths):
    # 解析路径（获取路径origin 及 生成路径to）
    origin_path = paths[0]
    if paths[1]:
        to_path = paths[1]
    else:
        to_path = origin_path
    del paths

    # 获取文件
    with open(os.path.join(origin_path, file_name), mode="r", encoding="utf-8") as f:
        origin_text = f.read()

    if not os.path.exists(to_path):
        os.makedirs(to_path)
        print("创建新的文件夹")

    x = main(origin_text)

    with open(os.path.join(to_path, prefix + file_name), mode="w", encoding="utf-8") as f:
        f.write(x)
        return True


def cmd():
    while True:
        path = input("Path: ")
        state = main(path)
        if state:
            print("SUCCESS!")


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.files, self.folders = None, None
        self.paths = []
        self.title("Html url_for Interpreter")
        # self.geometry("600x300")

        tk.Button(self, text='打开文件', width=20, command=self.select_file).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(self, text='打开文件夹', width=20, command=self.select_folder).grid(row=1, column=1, padx=5, pady=5)

        self.listbox = tk.Listbox(self, setgrid=True, width=60, selectmode=tk.EXTENDED)
        self.listbox.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
        # 删除选项
        delete_button = tk.Button(self, text='删除', width=10, command=self.delete)
        delete_button.grid(row=1, column=2, padx=5, pady=5)

        tk.Label(self, text="\t\t前缀").grid(row=3, column=0, pady=10)
        self.entry_text = tk.StringVar(self, value="inter_")
        tk.Entry(self, textvariable=self.entry_text).grid(row=3, column=1, pady=10)

        self.check_path = tk.IntVar(self, value=1)
        c1 = tk.Checkbutton(self, text="使用原文件路径", variable=self.check_path, onvalue=1, offvalue=0)
        c1.grid(row=4, column=0, pady=10)
        tk.Button(self, text="--> 转义", command=self.trans, width=20, height=2).grid(
            row=4, column=1, columnspan=1, pady=10)

    def delete(self):
        delete_tuple = self.listbox.curselection()
        delete_list = list(delete_tuple)
        delete_list.reverse()
        # print(delete_tuple, len(self.paths))
        for item in delete_list:
            del self.paths[item]
        self.listbox.delete(first=delete_tuple[0], last=delete_tuple[-1])

    def select_file(self):
        self.files = filedialog.askopenfilenames()  # 选择打开什么文件，返回文件名
        self.inter()

    def select_folder(self):
        self.folders = filedialog.askdirectory()  # 选择打开什么文件，返回文件名
        self.inter()

    def inter(self):
        def add_path(path):
            path = os.path.abspath(path)
            if path not in self.paths:
                self.paths.append(path)
            else:
                self.listbox.delete(self.paths.index(path))

        if self.files:
            for path in self.files:
                add_path(path)
        if self.folders:
            for filepath, dirnames, filenames in os.walk(self.folders):
                for filename in filenames:
                    add_path(os.path.join(filepath, filename))
        for i in self.paths:
            self.listbox.insert(tk.END, i)

    def trans(self):
        state = None

        def decompose(content: str):
            """ p_file为加上前一个文件目录的str """
            file, path = "", ""
            content = content.split("\\")
            file = content[-1]
            p_file = content[-2]
            del content[-1]
            content[0] += "\\"
            for i in content:
                path = os.path.join(path, i)
            return file, path, p_file

        if self.check_path.get() == 1:
            for ori in self.paths:
                file_name, origin_path, _ = decompose(ori)
                state = file_catcher(origin_path, origin_path, file_name, self.entry_text.get())
        else:
            save_path = filedialog.askdirectory(title="选择保存的文件夹")
            print(save_path)
            for ori in self.paths:
                file_name, origin_path, p_file = decompose(ori)
                to_path = os.path.join(save_path, "/_inter/", p_file)
                state = file_catcher(origin_path, to_path, file_name, self.entry_text.get())
        if state:
            tk.Message(self, text="转义成功").grid()


if __name__ == "__main__":
    try:
        root = GUI()
        root.mainloop()
    except ImportError:
        cmd()
