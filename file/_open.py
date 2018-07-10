#!/user/bin/python3
# -*- coding:utf-8 -*-
while True:

    # 打开文件
    myfile = open("myfile1.txt", "r+", -1, "utf-8")

    # 读取文件内容
    content = myfile.read()

    #输出文件内容
    print(content)

    writeContent = input("请输入添加内容：")

    myfile.write(writeContent)

    myfile.close()