from tkinter import *

from max30102 import MAX30102
import hrcalc

# 初始化 sensor
sensor = MAX30102()

window = Tk()

window.title("MAX30102 Demo")

def on_closing():
    # 退出程序前先关闭传感器
    sensor.shutdown()
    window.destroy()

# 上方空隙
frame1 = Frame(master=window, width=600, height=50)
frame1.pack(fill=BOTH, side=TOP, expand=True)

frame2 = Frame(master=window, width=600, height=600)

# 脉搏和你的血氧饱和度
upperText = Label(frame2, text="BPM: 0, SpO2: 0", font=("Arial", 30))
downText = Label(frame2, text="Put your hand on the sensor.", font=("Arial", 20))
upperText.grid(column=0, row=0)
downText.grid(column=0, row=1)

frame2.pack(anchor='center')

# 下方空隙
frame3 = Frame(master=window, width=600, height=50)
frame3.pack(fill=BOTH, side=TOP, expand=True)

# 更新Label的函数
def update_label():
    # 读取传感器的数据
    ir, red = sensor.read_sequential()
    # 解析数据，计算心率和血氧饱和度
    hr, hr_valid, spo2, spo2_valid = hrcalc.calc_hr_and_spo2(ir, red)
    # 判断数据是否有效
    if not hr_valid or not spo2_valid:
        text = "BPM: 0, SpO2: 0"
    else:
        # 格式化心率和血氧饱和度
        text = "BPM: {}, SpO2: {}".format(int(hr), int(spo2))
    # 更新Label
    upperText.config(text=text)
    # 通过after函数实现定时刷新
    window.after(1000, update_label)

# 启动定时刷新
update_label()

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
