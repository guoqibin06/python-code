from PIL import Image as i
import easygui
import os
im=easygui.enterbox(msg="请打开",title="包含要转换文件的文件夹")
print(im)
print(type(im))
#获取文件地址
imlist=os.listdir(im)
try:
    savefolder = easygui.enterbox(msg="请选择", title="保存转换后图像的文件夹")
    for img_Path in imlist:
        img=i.open(os.path.join(im,img_Path))
        new_img=img.convert("RGBA")
        #下面还需修改
        new_img.save(os.path.join(savefolder,os.path.splitext(img_Path)[0]+".png"))
        #还要试试出现空格中文行不行
except IOError:
    print("转换失败！")
