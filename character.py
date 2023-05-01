import tkinter as tk

# 画按钮
root = tk.Tk()
root.title("交大")
button1 = tk.Button(root, text="交", width=10, command=lambda: draw("jiao.txt"))
button1.grid(row=0, column=0, sticky=tk.E)
button2 = tk.Button(root, text="大", width=10, command=lambda: draw("da.txt"))
button2.grid(row=0, column=1, sticky=tk.W)

# 画字符, 显示在按钮下方
board = tk.Canvas(root, width=160, height=160)
board.grid(row=1, column=0, columnspan=2)


def draw(filename):
    if filename is None:
        ch = [False] * 256
    else:
        # 打开文件
        with open(filename, 'r') as f:
            # 读取文件中的所有行并去除空白字符
            lines = f.read().replace('\n', '').replace(' ', '').replace('\t', '').replace('\r', '')
        # 将读取的行转换为 True 或 False
        ch = [True if line == '1' else False for line in lines if line in ('0', '1')]
    for i in range(0, 16):
        for j in range(0, 16):
            if ch[j * 16 + i]:
                board.create_rectangle(i * 10, j * 10, i * 10 + 10, j * 10 + 10, fill="black")
            else:
                board.create_rectangle(i * 10, j * 10, i * 10 + 10, j * 10 + 10, fill="white")


draw(None)
root.mainloop()
