
#!/usr/bin/python3
#pip install PyMuPDF

#找到 fitz 的安装目录
#vscode setting 中搜索 python.analysis.extraPaths
#fitz 的安装目录 添加到   python.analysis.extraPaths
#导入库：
import fitz
#1. 导入库，查看版本
print(fitz.__doc__)

doc= fitz.open("C:\\eagle-data\\eagle-sight\\git\\NewEnergy\\doc\\03设计\\0302详细设计\\tbox-vcu 协议\\华宝-鹰明\\鹰明汽车远程服务终端与云平台通信协议V1.4.pdf")

print("doc:",doc)

print("doc.page_count:",doc.page_count)

print("doc.metadata:",doc.metadata)

print("doc.get_toc():",doc.get_toc())


#页面输出

for index in range(0,doc.page_count):    
    print("index:",index)
    page = doc.load_page(index)
    print(page)
    for link in page.links():
        print("index-link:",link)
    for annot in page.annots():
        print("index-annot:",annot)
    for field in page.widgets():
        print("index-field:",field)

    """
    text = page.get_text(opt)
对opt使用以下字符串之一以获取不同的格式：

"text"：（默认）带换行符的纯文本。无格式、无文字位置详细信息、无图像

"blocks"：生成文本块（段落）的列表

"words"：生成单词列表（不包含空格的字符串）

"html"：创建页面的完整视觉版本，包括任何图像。这可以通过internet浏览器显示

"dict"/"json"：与HTML相同的信息级别，但作为Python字典或resp.JSON字符串。

"rawdict"/"rawjson"："dict"/"json"的超级集合。它还提供诸如XML之类的字符详细信息。

"xhtml"：文本信息级别与文本版本相同，但包含图像。

"xml"：不包含图像，但包含每个文本字符的完整位置和字体信息。使用XML模块进行解释。
    """
    text = page.get_text("text")
    print ("text",text)

    
    blocks = page.get_text("blocks")
    print ("blocks",blocks)
    
    dict = page.get_text("dict")
    print ("dict",dict)
    xml = page.get_text("xml")
    print ("xml",xml)