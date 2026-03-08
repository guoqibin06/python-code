from PIL import Image
import easygui
import os
import Remove_Watermark as RW
choices = ["去水印工具","批量更改格式为png"]
ret = easygui.choicebox("目前包含的功能：","请选择工具",choices)
if ret == "批量更改格式为png":
    img_path=easygui.diropenbox("请打开包含要转换文件的文件夹：")
    if not img_path:
        print("无效文件路径")
        exit(0)        
    #获取文件地址
    imlist=os.listdir(img_path)
    try:
        savefolder = easygui.diropenbox(msg="请打开保存转换后图像的文件夹",title="请选择文件夹")
        if not savefolder:
            print("无效文件路径")
            exit(0)
        for img_converted_path in imlist:
            support_format_list = [".png",".jpg",".jpeg"]
            if not (os.path.splitext(img_converted_path)[1] in support_format_list):
                continue
            img=Image.open(os.path.join(img_path,img_converted_path))
            new_img=img.convert("RGBA")
            #下面还需修改
            new_img.save(os.path.join(savefolder,os.path.splitext(img_converted_path)[0]+".png"))
            #还要试试出现空格中文行不行
    except IOError:
        print("转换失败！")
elif ret == "去水印工具":
    video_path = easygui.fileopenbox(msg="请选择",title="要去水印的单个视频")
    if not video_path:
        print("无效文件路径")
        exit(0)
    out_put_path = easygui.filesavebox(msg="请选择",title="输出路径")
    if not out_put_path:
        print("无效文件路径")
        exit(0)
    roi_x,roi_y,roi_w,roi_h = RW.select_watermark_roi(video_path)
    if roi_x is None:
        print("无效roi")
        exit()
    RW.remove_watermark(video_path,out_put_path,(roi_x,roi_y,roi_w,roi_h))
