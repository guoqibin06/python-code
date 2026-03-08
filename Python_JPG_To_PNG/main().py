from PIL import Image
import easygui
import os
from pathlib import Path
import sys
import Remove_Watermark as RW
choices = ["去水印工具","批量更改格式为png"]
ret = easygui.choicebox("目前包含的功能：","请选择工具",choices)
if ret == "批量更改格式为png":
    img_path=easygui.diropenbox("请打开包含要转换文件的文件夹：")
    if not img_path:
        print("无效文件路径")
        sys.exit(0)        
    #获取文件地址
    imlist=os.listdir(img_path)
    try:
        savefolder = easygui.diropenbox(msg="请打开保存转换后图像的文件夹",title="请选择文件夹")
        converted_count = 0
        if not savefolder:
            print("无效文件路径")
            sys.exit(0)

        for img_converted_path in imlist:
            support_format_list = [".png",".jpg",".jpeg",".bmp", ".gif"]
            #还要试试出现空格中文行不行,用pathlib下的Path
            img_converted_path = Path(img_converted_path)
            if not img_converted_path.suffix.lower() in support_format_list:
                continue
            with Image.open(str(Path(img_path)/img_converted_path)) as img:
                new_img =img.convert("RGBA")
                new_img.save(str(Path(savefolder)/img_converted_path.stem/".png"))
        easygui.msgbox(msg=f"共转换{converted_count}",title="本次转换已完成")
    except Exception as e:
        print(f"转换失败！错误信息：{str(e)}")
        exit(1)
elif ret == "去水印工具":
    video_path = easygui.fileopenbox(msg="请选择",title="要去水印的单个视频")
    if not video_path:
        print("无效文件路径")
        sys.exit(0)
    out_put_path = easygui.filesavebox(msg="请选择",title="输出路径")
    if not out_put_path:
        print("无效文件路径")
        sys.exit(0)
    roi_x,roi_y,roi_w,roi_h = RW.select_watermark_roi(video_path)
    if roi_x is None:
        print("无效roi")
        sys.exit(0)
    RW.remove_watermark(video_path,out_put_path,(roi_x,roi_y,roi_w,roi_h))
