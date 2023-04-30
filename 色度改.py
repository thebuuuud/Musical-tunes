#1.引入需要的库函数
import librosa
import matplotlib.pyplot as plt
import librosa.display
import numpy as np
import pandas as pd

#2.载入音乐（需要换成自己电脑上的路径）（这里的采样率和每帧长度采用默认值，我算了一下还算合理，可以讨论需不需要修改）
y,sr=librosa.load("F:\Amedeo Tommasi - Magic Waltz.mp3")

#3.处理cqt下的色度向量
threshold=0.9 #设置绝对能量和相对能量的阈值，其余音置零，可以消除部分静音帧并起到筛选的作用
chroma_cq = librosa.feature.chroma_cqt(y=y, sr=sr,threshold=threshold)
chroma_cq [chroma_cq < threshold] = 0.0
mean = np.mean(chroma_cq, axis=1) # 计算每一行的均值，可以代表每种音高在音乐中出现的相对时长
# print(mean)


# 输出2：色度向量写入excel
data = pd.DataFrame(chroma_cq) #将数组转换为dataframe结构
writer = pd.ExcelWriter('G:\重要作品\作业\大二下\信号系统\音乐讨论\sedu2.xlsx')   # 写入Excel文件
data.to_excel(writer, 'page_2', float_format='%.5f')   ## ‘page_1’是写入excel的sheet名
# writer.save() #这句注释掉
writer.close()


#4. 调式标准向量（强化了主音和属音的寻找）
Mode=[[2,0,1,0,1,1,0,2,0,1,0,1],# C大
[1,0,1,0,2,1,0,1,0,2,0,1],# a小

[1,0,2,0,1,0,1,2,0,1,0,1],# G大
[1,0,1,0,2,0,1,1,0,1,0,2],# e小

[0,1,2,0,1,0,1,1,0,2,0,1],# D大
[0,1,1,0,1,0,2,1,0,1,0,2],# b小

[0,1,1,0,2,0,1,0,1,2,0,1],# A大
[0,2,1,0,1,0,2,0,1,1,0,1],# #f小

[0,1,0,1,2,0,1,0,1,1,0,2],# E大
[0,2,0,1,1,0,1,0,2,1,0,1],# #c小

[0,1,0,1,1,0,2,0,1,0,1,2],# B大
[0,1,0,2,1,0,1,0,2,0,1,1],# #g小

[0,2,0,1,0,1,2,0,1,0,1,1],# #F大
[0,1,0,2,0,1,1,0,1,0,2,1],# #d小

[1,2,0,1,0,1,1,0,2,0,1,0],# #C大
[1,1,0,1,0,2,1,0,1,0,2,0],# #a小


[2,0,1,0,1,2,0,1,0,1,1,0],# F大
[1,0,2,0,1,1,0,1,0,2,1,0],# d小

[1,0,1,1,0,2,0,1,0,1,2,0],# bB大
[1,0,2,1,0,1,0,2,0,1,1,0],# g小

[1,0,1,2,0,1,0,1,1,0,2,0],# bE大
[2,0,1,1,0,1,0,2,1,0,1,0],# c小

[1,1,0,2,0,1,0,1,2,0,1,0],# bA大
[2,1,0,1,0,2,0,1,1,0,1,0]]# f小


Mode_name=["C大调","a小调","G大调","e小调","D大调","b小调","A大调","升f小调","E大调","升c小调",
           "B大调","升g小调","升F大调","升d小调","升C大调","升a小调","F大调","d小调","降B大调",
           "g小调","降E大调","c小调","降A大调","f小调"]

#5.用简单的互相关运算代替了求相关系数
result=[0 for c in range(24)]

for i in range(0,len(Mode)):
    result[i]= np.dot(mean,Mode[i])
    print(result[i])

print("------------------")

#6.排序，选取最大
def list_max(list):
    #假设第一个最大，最大值的下标0
    index = 0
    max = list[0]
    for i in range(1,len(list)):
        if(list[i] > max):
            max = list[i]
            index = i
    index=index+1#不是按数组，按正常算法，从1开始
    return (index,max)#返回多个值，使用元组


res = list_max(result)
print(Mode_name[res[0]-1])
print("第%d个;最大值：%f"%res)


#7.画出置零处理后的cqt色谱图，便于观察
plt.figure(figsize = (15,5))
librosa.display.specshow(chroma_cq, x_axis = 'time',y_axis = 'chroma',cmap = 'coolwarm')