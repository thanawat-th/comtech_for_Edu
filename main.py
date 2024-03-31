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
startt = "pres [1] to go"
mkSound = "Make your sound"
presred = "[1]when finish"
now = "listening..."


#ตัวแปรตั่งต่าง
startPin = 1
pressed = 0
soundlevel = 0
correctButton = 0
choice = []
global score
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
def show_quiz_num(q, m):
    strtex = "q: " + str(q) + "/5" + "   mode: " + str(m)
    display.fill(0)
    display.text(strtex, 0, 0, 1)
    display.show()

def show_text_head(tex):
    display.fill(0)
    strtex = str(tex)
    display.text(strtex, 0, 8, 1)
    display.show()
    
def show_text(tex):
    strtex = str(tex)
    display.text(strtex, 0, 8, 1)
    display.show()
    
#ฟังก์ชันแสดงข้อความบนจอ บรรทัด2
def show_text_2(tex):
    strtex = str(tex)
    display.text(strtex, 0, 20, 1)
    display.show()
    
#ฟังก์ชันแสดงข้อความบนจอ บรรทัด3
def show_text_3(tex):
    strtex = str(tex)
    display.text(strtex, 0, 30, 1)
    display.show()
def show_text_31(tex):
    strtex = str(tex)
    display.text(strtex, 0, 32, 1)
    display.show()
    
#ฟังก์ชันแสดงข้อความบนจอ บรรทัด4
def show_text_4(tex):
    strtex = str(tex)
    display.text(strtex, 0, 40, 1)
    display.show()
def show_text_41(tex):
    strtex = str(tex)
    display.text(strtex, 0, 42, 1)
    display.show()
    
#ฟังก์ชันแสดงข้อความบนจอ บรรทัด5
def show_text_5(tex):
    strtex = str(tex)
    display.text(strtex, 0, 50, 1)
    display.show()
    

def show_text_6(tex):
    strtex = str(tex)
    display.text(strtex, 0, 55, 1)
    display.show()
    
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
    

def random_mode():
    global mode
    mode = random.randint(0, 1)

def map_sound_level(input_level):
    ran_tip = random.randint(0, 2)
    tip_20 = ["whisper", "library", "Humming"]
    tip_40 = ["talking", "rain", "outsite"]
    tip_60 = ["hair dryer", "Busy traffic", "vacuum cleaner"]
    tip_90 = ["motorcycle", "concert", "thunderclap"]
    if input_level == 0:
        return "hear Threshold"
    elif 20 <= input_level < 40:
        return tip_20[ran_tip]
    elif 40 <= input_level < 60:
        return tip_40[ran_tip]
    elif 60 <= input_level < 90:
        return tip_60[ran_tip]
    elif 90 <= input_level :
        return tip_90[ran_tip]

#ฟังก์ชันรับเสียง
def get_sound_input(i, mode):
    global soundlevel
    show_quiz_num(i, mode)
    show_text(mkSound)
    show_text_3(now)
    show_text_6(presred)
    adc34 = ADC(Pin(34))
    adc34.atten(ADC.ATTN_11DB)
    adc34.width(ADC.WIDTH_12BIT)
    pressed = 0
    final_diff = 0
    calibration_factor = 20
    ref_value = 1725
    while True:
        voltage = adc34.read()
        diff = abs(voltage - ref_value)
        if diff >= 20:
            if diff > final_diff:
                final_diff = diff
                print(final_diff)
        if not button1.value():
            if final_diff == 0:
                soundlevel = 0
            else:
                soundlevel = round(20 * math.log10(final_diff))
            print(final_diff)
            break
        time.sleep(0.0096)
    return

''''
0 dB: Threshold of hearing (faint rustle of leaves)
10 dB: Very quiet (breathing)
20 dB: Quiet (whisper)
30 dB: Soft (library)
40 dB: Quiet conversation (refrigerator hum)
50 dB: Moderate conversation (moderate rain)
60 dB: Normal conversation (air conditioner)
70 dB: Busy traffic (vacuum cleaner)
80 dB: Loud music (hair dryer)
90 dB: Very loud music (motorcycle)
100 dB: Noisy factory (subway train)
110 dB: Painful (car horn)
120 dB: Extremely loud (thunderclap)
130 dB: Deafening (jet airplane takeoff)
140 dB: Pain threshold (rock concert)
150 dB: Beyond the pain threshold (gunshot)
160 dB: Can cause immediate ear damage (fireworks)'''

    


if __name__ == "__main__":
    #เมนลูปจ้าา
    while True:
        finish = 0
        show_text_head("  SONIC SENSEI") #หน้าแรก
        show_text_3("    [1]play")
        show_text_41("    [2]about")
        show_text_6("    [3]credit")
        time.sleep(1)
        pressed = 0
        check_press()
        if pressed == 1:
            score = 0
            for i in range(5): #5รอบ 5ข้อ
                random_mode()
                if mode == 0:
                    get_sound_input(i + 1, mode+1)
                    print(soundlevel) #เอาไว้ดีบักเฉยๆ เดะค่อยลบ
                    quizz(soundlevel)
                    show_quiz_num(i+1, mode+1)
                    show_text("What Sound Level (dB):") #หน้าคำถาม
                    show_text_2("[1] "+ str(choices[0]))
                    show_text_3("[2] "+ str(choices[1]))
                    show_text_4("[3] "+ str(choices[2]))
                    show_text_5("[4] "+ str(choices[3]))
                    time.sleep(1)
                    pressed = 0
                    check_press()
                    if pressed == correctButton: #ตรวจคำตอบ
                        show_quiz_num(i+1, mode+1)
                        show_text("you Correct :) ") 
                        show_text_2("^^ + 1 Point ^^")
                        show_text_31(str(soundlevel) + "dB is sound of:")
                        show_text_41("->" + map_sound_level(soundlevel))
                        show_text_6("[1]next         ")
                        score = score + 1
                        time.sleep(1)
                        pressed = 0
                        check_press()
                        if pressed == startPin:
                            pass
                    else:
                        show_quiz_num(i+1, mode+1)
                        show_text("try next time :(")
                        show_text_2("correct is "  + str(soundlevel) + "dB")
                        show_text_31(str(soundlevel) + "dB is sound of:")
                        show_text_41("->" + map_sound_level(soundlevel))
                        show_text_6("[1]next         ")
                        time.sleep(1)
                        pressed = 0
                        check_press()
                        if pressed == startPin:
                            pass
                        
                else:
                    db_question = random.randint(25, 70)
                    show_quiz_num(i+1, mode+1)
                    show_text("make sound level:")
                    show_text_3(str(db_question) + " dB")
                    show_text_6("[1]if you ready")
                    pressed = 0
                    check_press()
                    if pressed == startPin:
                        for j in range(2):
                            get_sound_input(i+1, mode+1)
                            diff_ans = abs(db_question - soundlevel)
                            if diff_ans <= 10:
                                show_quiz_num(i+1, mode+1)
                                show_text("your SoundLevel:")
                                show_text_2(str(soundlevel) + " dB")
                                show_text_3("Diff:" + str(diff_ans) + " from:" + str(db_question))
                                show_text_4("^^ + 1 Point ^^")
                                show_text_6("[1]next         ")
                                score = score + 1
                                time.sleep(1)
                                pressed = 0
                                check_press()
                                if pressed == 1:
                                    break
                                
                            else:
                                show_quiz_num(i+1, mode+1)
                                show_text("your SoundLevel:")
                                show_text_2(str(soundlevel) + " dB")
                                show_text_3("Diff:" + str(diff_ans) + " from:" + str(db_question))
                                show_text_4("try next time :(")
                                if j < 1:
                                    show_text_6("[1]next [2]retry")
                                else:
                                    show_text_6("[1]next         ")
                                time.sleep(1)
                                pressed = 0
                                check_press()
                                if pressed == 1:  
                                    break
                                elif pressed == 2: 
                                    pass
            finish = 1
            
        elif pressed == 2:
            show_text_head("Have 2 mode:")
            show_text_3("[1]about mode 1")
            show_text_4("[2]about mode 2")
            show_text_6("     [4]back")
            pressed = 0
            check_press()
            if pressed == 4:
                pressed = 0
                pass
            elif pressed == 1:
                pressed = 0
                show_text_head("    MODE 1:")
                show_text_3("Input your sound")
                show_text_4("And guess level")
                show_text_6("     [4]main")
                check_press()
                pass
            elif pressed == 2:
                pressed = 0
                show_text_head("    MODE 2:")
                show_text_2("Set volume level")
                show_text_3("you make sound")
                show_text_4("closest question")
                show_text_6("     [4]main")
                check_press()
                pass
            
        elif pressed == 3:
            show_text_head("   DEVELOPER:")
            show_text_3("1.Natpicha 155-6")
            show_text_4("2.Thanawat 159-8")
            show_text_6("     [4]back")
            pressed = 0
            check_press()
            pass
            
        if finish == 1:
            display.fill(0)
            show_text("^_^ CONGRATE ^_^") #หน้าสรุปผลล
            show_text_2(" your Score : " + str(score))
            if score == 5:
                show_text_31("    YOU ARE")
                show_text_41(" SOUND MASTER!!")
            show_text_6("  [4]play Agin")
            pressed = 0
            check_press()
            display.fill(0)
            display.show()
            pass
    