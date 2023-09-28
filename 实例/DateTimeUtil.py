import time
import datetime 

#参数注释：以冒号（:）标记，建议传入的参数类型
#返回值注释：以 ->标记，建议函数返回的类型
def dateTimeToStr(dateTime:"时间",formate:"格式")-> "时间字符串格式化":    
    #转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
    timeArray = time.localtime(dateTime)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime