#อิมพอร์ตแพ็คเกจจ้า
from machine import Pin, ADC, I2C 
import random
import time
import math
import ssd1306 #แพ็คเกจจอเด้อ


# Define GPIO pins for buttons and sound
sound_pin = 34
button1_pin = 25
button2_pin = 26
button3_pin = 27
button4_pin = 18

adc34 = ADC(Pin(sound_pin))
i2c = I2C(sda=Pin(16), scl=Pin(17)) #กำหนดการสื่อสารของจอเป็นแบบ I2C 
display = ssd1306.SSD1306_I2C(128, 64, i2c) #กำหนดขนาดของจอ

# Initialize button pins
button1 = Pin(button1_pin, Pin.IN, Pin.PULL_UP)
button2 = Pin(button2_pin, Pin.IN, Pin.PULL_UP)
button3 = Pin(button3_pin, Pin.IN, Pin.PULL_UP)
button4 = Pin(button4_pin, Pin.IN, Pin.PULL_UP)

#ข้อความตั่งต่าง
question1 = "what is sound level?"
startt = "pres 1 to go"
mkSound = "Make sound and"
presred = "press 1"


#ตัวแปรตั่งต่าง
startPin = 1
pressed = 0
soundlevel = 0
correctButton = 0
choice = []
score = 0
mode = 0
db_question = 0


#ฟังก์ชันกำหนดการกดปุ่ม
def check_buttons():
    global pressed
    if not button1.value():
        pressed = 1
    if not button2.value():
        pressed = 2
    if not button3.value():
        pressed = 3
    if not button4.value():
        pressed = 4
    
#ฟังก์ชันตรวจสอบการกดปุ่ม
def check_press():
    while True:
        check_buttons()
        time.sleep(0.15) # Adjust the sleep time as needed
        if pressed != 0:
            break
    return pressed
    

#ฟังก์ชันแสดงข้อความบนจอ บรรทัดแรก       
def show_text(tex):
    strtex = str(tex)
    display.fill(0)
    display.text(strtex, 0, 0, 1)
    display.show()
    return
#ฟังก์ชันแสดงข้อความบนจอ บรรทัด2
def show_text_2(tex):
    strtex = str(tex)
    display.text(strtex, 0, 20, 1)
    display.show()
    return
#ฟังก์ชันแสดงข้อความบนจอ บรรทัด3
def show_text_3(tex):
    strtex = str(tex)
    display.text(strtex, 0, 30, 1)
    display.show()
    return
#ฟังก์ชันแสดงข้อความบนจอ บรรทัด4
def show_text_4(tex):
    strtex = str(tex)
    display.text(strtex, 0, 40, 1)
    display.show()
    return
#ฟังก์ชันแสดงข้อความบนจอ บรรทัด5
def show_text_5(tex):
    strtex = str(tex)
    display.text(strtex, 0, 50, 1)
    display.show()
    return

def show_text_6(tex):
    strtex = str(tex)
    display.text(strtex, 0, 60, 1)
    display.show()
    return

#ฟังก์ชันรับเสียง
def read_sound():
    adc34.read()
    adc34.atten(ADC.ATTN_11DB)
    adc34.width(ADC.WIDTH_12BIT)
    voltage = adc34.read()
    calibration_factor = 20
    return 20 * math.log10(voltage / 0.1) #+ calibration_factor
    
#ฟังก์ชันสุ่มตัวเลขแบบไม่เอาค่าที่ต้องการ
def random_with_avoid(start, end, avoid):
    rand_num = random.randint(start, end)
    while rand_num < avoid and rand_num > -(avoid):
        rand_num = random.randint(start, end)
    return rand_num

#ฟังก์ชันสุ่มช้อยส์
def quizz(deciB):
    global correctButton
    global choices
    correctButton = random.randint(1, 4)
    choices = [random_with_avoid(-30, 30, 10) for _ in range(4)]
    for i in range (4):
        choices[i-1] = choices[i-1] + deciB
    choices[correctButton - 1] = deciB
    return

def random_mode():
    global mode
    mode = random.randint(1, 2)
    return
    
def mode_1():
    show_text(mkSound)
    show_text_2(presred) #หน้าสอง
    soundlevel = read_sound()
    print(soundlevel) #เอาไว้ดีบักเฉยๆ เดะค่อยลบ
    pressed = 0
    check_press()
    if pressed == startPin:
        quizz(soundlevel)
        show_text("What Sound Level (dB):") #หน้าคำถาม
        show_text_2("1."+ str(choices[0]))
        show_text_3("2."+ str(choices[1]))
        show_text_4("3."+ str(choices[2]))
        show_text_5("4."+ str(choices[3]))
        pressed = 0
        check_press()
        if pressed == correctButton: #ตรวจคำตอบ
            show_text("you Correct :) ") 
            show_text_2("^^ + 1 Point ^^")
            score = score + 1
            time.sleep(2)
            return
        else:
            show_text("try next time :(")
            time.sleep(2)
            return
    else: #เอาไว้ดีบักเฉยๆ เดะค่อยลบ
        return
    

def mode_2():
    global score
    db_question = random.randint(30, 90)
    show_text("make sound level:")
    show_text_2(str(db_question) + " dB")
    show_text_3("press 1 to go next")
    pressed = 0
    check_press()
    if pressed == startPin:
        for i in range(2):
            show_text(mkSound)
            show_text_2(presred)
            soundlevel = read_sound()
            print(soundlevel) #เอาไว้ดีบักเฉยๆ เดะค่อยลบ
            pressed = 0
            check_press()
            if pressed == startPin:
                diff = abs(db_question - soundlevel)
                if diff <= 10:
                    show_text("your Sound Level is:")
                    show_text_2(str(soundlevel) + " dB")
                    show_text_3("Difference: " + str(diff))
                    show_text_4("^^ + 1 Point ^^")
                    if i < 1:
                        show_text_6("1.retry       2.next")
                    else:
                        show_text_6("              2.next")
                    score = score + 1
                    pressed = 0
                    check_press()
                    if pressed == 2:
                        break
                    elif pressed == 1:
                        pass
                else:
                    show_text("your Sound Level is:")
                    show_text_2(str(soundlevel) + " dB")
                    show_text_3("Difference: " + str(diff))
                    show_text_4("try next time :(")
                    if i < 1:
                        show_text_6("1.retry       2.next")
                    else:
                        show_text_6("              2.next")
                    pressed = 0
                    check_press()
                    if pressed == 2:
                        break
                    elif pressed == 1:
                        pass
             
    return
    


if __name__ == "__main__":
    #เมนลูปจ้าา
    for i in range(5): #5รอบ 5ข้อ
        pressed = 0
        show_text(startt) #หน้าแรก
        check_press()
        if pressed == startPin:
                random_mode()
                if mode == 0:
                    mode_1()
                    pass
                else:
                    mode_2()
                    pass
        
        elif pressed != 0: #เอาไว้ดีบักเฉยๆ เดะค่อยลบ
            if pressed == 3:
                display.fill(0)
                display.show()
                break
            display.fill(0)
            display.show()
            print(pressed)
            pass
    show_text("^^ CONGRATE ^^") #หน้าสรุปผลล
    show_text_2("your Score : " + str(score))