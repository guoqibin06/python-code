import cv2
import numpy as np

def read_video_and_show_frame(video_path="你的视频.mp4"):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("视频打开失败")
        return
    else:
        #获取视频属性并输出
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print("视频信息：")
    print(f"视频帧率：{fps}")
    print(f"分辨率：{width}x{height}")
    print(f"总帧数：{total_frame}")
    print(f"视频时长：{total_frame/fps:.2f}秒")
    ret,frame = cap.read()
    if not ret:
        print("视频第一帧读取失败")
        cap.release()
        return
    cv2.namedWindow("视频第一帧",cv2.WINDOW_NORMAL)
    cv2.resizeWindow("视频第一帧",800,600)
    cv2.imshow("视频第一帧",frame)
    print("请按任意键关闭")
    cv2.waitKey(0)
    cap.release()
    cv2.destroyAllWindows()
# 全局变量
start_x,start_y = -1,-1
end_x,end_y = -1,-1
drawing = False
frame_copy = None
WINDOW_NAME = "Select watermark"
def mouse_draw(event,x,y,flags,param):
    global start_x,start_y,end_x,end_y,drawing,frame_copy
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_x,start_y = x,y
    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        frame_copy = param.copy()
        cv2.rectangle(frame_copy,(start_x,start_y),(x,y),(0,255,0),2)
        cv2.imshow(WINDOW_NAME,frame_copy)
    elif event == cv2.EVENT_LBUTTONUP:
        end_x,end_y = x,y
        drawing = False
        global roi_x,roi_y,roi_w,roi_h
        roi_x = min(start_x,end_x)
        roi_y = min(start_y,end_y)
        roi_w = abs(start_x - end_x)
        roi_h = abs(start_y - end_y)
        # 画出选定的矩形
        cv2.rectangle(frame_copy,(roi_x,roi_y),(roi_x+roi_w,roi_y+roi_h),(0,0,255),2)
        cv2.imshow(WINDOW_NAME,frame_copy)
        # 输出参数
        print("="*50)
        print(f"水印区域参数（直接用）：roi=({roi_x}, {roi_y}, {roi_w}, {roi_h})")
        print("="*50)
def select_watermark_roi(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("视频打开失败")
        return
    ret,frame = cap.read()
    if not ret:
        print("读取失败")
        cap.release()
        return
    cap.release()  # 只需要第一帧，提前释放视频资源

    global frame_copy
    frame_copy = frame.copy()
    # 创建窗口
    cv2.namedWindow(WINDOW_NAME,cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW_NAME,1280,700)
    cv2.imshow(WINDOW_NAME,frame_copy) # 这里先显示窗口保证窗口句柄有效
    cv2.setMouseCallback(WINDOW_NAME,mouse_draw,frame)
    #等待操作
    print("鼠标拖动框选")
    print("按ESC关闭")
    while True:
        if cv2.waitKey(1) & 0xFF == 27:  # 27是ESC键的ASCII码
            break
    cv2.destroyAllWindows()
    if roi_x == -1 or roi_y == -1 or roi_w == 0 or roi_h == 0:
        print("无效的选取范围")
        return None,None,None,None
    return roi_x,roi_y,roi_w,roi_h

def remove_watermark(video_path,out_put_path,roi=None):
    if roi is None or len(roi) != 4:
        print("无效roi")
        return
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("无效文件路径")
        return
    roi_x,roi_y,roi_w,roi_h = roi
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # 创建视频写入器
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(out_put_path,fourcc,fps,(width,height))
    if not out.isOpened():
        print("视频写入器创建失败，请检查输出路径是否合法！")
        return
    # 创建水印遮罩
    mask = np.zeros((height,width),dtype = np.uint8)
    mask[roi_y:roi_y+roi_h,roi_x:roi_x+roi_w] = 255

    # 去水印核心操作
    print(f"开始去水印。。。共{total_frame}帧")
    proceed = 0
    while cap.isOpened():
        ret,frame = cap.read()
        if not ret:
            break
        frame_fixed = cv2.inpaint(frame,mask,3,cv2.INPAINT_TELEA)
        out.write(frame_fixed)
        proceed += 1
        # 进度提示
        if proceed % 100 == 0:
            print(f"进度完成：{proceed}/{total_frame}帧")
        
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"本次任务已完成，文件已保存至{out_put_path}")
    print("按下任意键以退出")
    cv2.waitKey(0)

if __name__ == "__main__":
    video_path = "2026-03-07 22-06-11.mp4"
    out_put_path = "test.mp4"
    roi_x,roi_y,roi_w,roi_h = select_watermark_roi(video_path)
    if roi_x is None:
        print("无效roi")
        exit()
    remove_watermark(video_path,out_put_path,(roi_x,roi_y,roi_w,roi_h))

    