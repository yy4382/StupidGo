import tkinter as tk
'''
文件格式应该如下(可以任意增加、删除\n,\r,\t和空格）
jiao.txt: 
0000001000000000
0000000100000000
0000000100000000
1111111111111110
0000000000000000
0001000000010000
0001000000001000
0010000000100100
0100100000100100
0000010001000000
0000001010000000
0000000100000000
0000001010000000
0000110001000000
0011000000110000
1100000000001110
'''

# 打开文件
with open('jiao.txt', 'r') as f:
    # 读取文件中的所有行并去除空白字符
    lines = f.read().replace('\n', '').replace(' ', '').replace('\t', '').replace('\r', '')
# 将读取的行转换为 True 或 False
character = [True if line == '1' else False for line in lines if line in ('0', '1')]

# 画字符
board = tk.Canvas(width=500, height=500)
board.pack()
for i in range(0, 16):
    for j in range(0, 16):
        if character[j * 16 + i]:
            board.create_rectangle(i * 10, j * 10, i * 10 + 10, j * 10 + 10, fill="black")
        else:
            board.create_rectangle(i * 10, j * 10, i * 10 + 10, j * 10 + 10, fill="white")
tk.mainloop()
