from m5stack import *
from m5ui import *
from uiflow import *
import time
import ntptime
import urequests
import unit


setScreenColor(0x222222)
servo_0 = unit.get(unit.SERVO, unit.PORTA)
finger_0 = unit.get(unit.FINGER, unit.PORTC)


variable_speed = None
stop_speed = None
degree_change = None
mode_name = None
dir1 = None
dir2 = None
dir3 = None
angle_and_status_lab = None
angle_and_status_val = None
left_button = None
middle_button = None
right_button = None
login_id = None
lab_login_val = None
scan_stat_color = None
scan_stat_val = None
current_mode = None
current_login_id = None
month = None
finger_read_mode = None
day = None
login_mode = None
hour = None
register_once = None
current_angle_value = None
id_register_count = None
minute = None
strmonth = None
second = None
http_status = None
log_id = None
strday = None
strhour = None
strminute = None
strsecond = None
name_gen_count = None



error_label = M5TextBox(12, 182, "*ERROR*", lcd.FONT_Default, 0xff1414, rotate=0)
error_val = M5TextBox(86, 182, "???", lcd.FONT_Default, 0xff1414, rotate=0)
screen_background_layer = M5Rect(0, 0, 320, 240, 0x222222, 0x222222)
cm_rectangle_left = M5Rect(0, 0, 50, 30, 0x703899, 0x703899)
current_menu_label = M5TextBox(64, 9, "Current menu: ", lcd.FONT_Default, 0xFFFFFF, rotate=0)
cm_rectangle_right = M5Rect(270, 0, 50, 30, 0x703899, 0x703899)
current_menu_val = M5TextBox(172, 9, "???", lcd.FONT_Default, 0xfeaa3f, rotate=0)
a_button_label = M5TextBox(41, 222, "Register", lcd.FONT_Default, 0x31981c, rotate=0)
c_button_label = M5TextBox(214, 222, "Bed adjust", lcd.FONT_Default, 0x9b6638, rotate=0)
b_button_label = M5TextBox(132, 222, "Login", lcd.FONT_Default, 0xd7e847, rotate=0)
cm_rectangle_line_bottom = M5Rect(35, 25, 240, 5, 0x703899, 0x703899)
cm_rectangle_line_top = M5Rect(46, 0, 240, 5, 0x703899, 0x703899)
scan_angle_status_label = M5TextBox(12, 136, "Scan Status:", lcd.FONT_Default, 0xFFFFFF, rotate=0)
directions_line3 = M5TextBox(12, 101, "???", lcd.FONT_Default, 0x0f5dff, rotate=0)
scan_status_val = M5TextBox(112, 136, "???", lcd.FONT_Default, 0x5dd0cf, rotate=0)
dir_rectangle_left = M5Rect(0, 31, 2, 94, 0xfd94f8, 0xfd94f8)
current_login_label = M5TextBox(12, 158, "Current Login ID:", lcd.FONT_Default, 0xFFFFFF, rotate=0)
dir_rectangle_right = M5Rect(318, 33, 2, 94, 0xfd94f8, 0xfd94f8)
current_login_val = M5TextBox(140, 158, "???", lcd.FONT_Default, 0xe265c7, rotate=0)
dir_rectangle_bottom = M5Rect(0, 125, 320, 2, 0xfd94f8, 0xfd94f8)
dir_rectangle_top = M5Rect(1, 31, 320, 2, 0xfd94f8, 0xfd94f8)
directions_label = M5TextBox(12, 40, "Directions:", lcd.FONT_Default, 0xFFFFFF, rotate=0)
directions_line1 = M5TextBox(12, 62, "???", lcd.FONT_Default, 0x0f5dff, rotate=0)
directions_line2 = M5TextBox(12, 81, "???", lcd.FONT_Default, 0x0f5dff, rotate=0)

from numbers import Number


# Describe this function...
def move_motor(variable_speed, stop_speed, degree_change):
  global mode_name, dir1, dir2, dir3, angle_and_status_lab, angle_and_status_val, left_button, middle_button, right_button, login_id, lab_login_val, scan_stat_color, scan_stat_val, current_mode, current_login_id, month, finger_read_mode, day, login_mode, hour, register_once, current_angle_value, id_register_count, minute, strmonth, second, http_status, log_id, strday, strhour, strminute, strsecond, name_gen_count
  servo_0.write_angle(variable_speed)
  wait_ms(188)
  servo_0.write_angle(stop_speed)
  current_angle_value = (current_angle_value if isinstance(current_angle_value, Number) else 0) + degree_change
  try:
    req = urequests.request(method='POST', url='*INSERT YOUR OWN DATABASE CONNECTION LINK HERE*',json={'log_id':log_id,'patient_id':current_login_id,'datatimestamp':oracletimestamp(),'angle_rotation':current_angle_value}, headers={'Content-Type':'application/json'})
    http_status = 'Success'
    gc.collect()
    req.close()
  except:
    http_status = 'Failure'
  log_id = (log_id if isinstance(log_id, Number) else 0) + 1
  scan_status_val.setText(str((str(current_angle_value) + str(' Degrees'))))

# Describe this function...
def change_between_main_and_adjust(mode_name, dir1, dir2, dir3, angle_and_status_lab, angle_and_status_val, left_button, middle_button, right_button):
  global variable_speed, stop_speed, degree_change, login_id, lab_login_val, scan_stat_color, scan_stat_val, current_mode, current_login_id, month, finger_read_mode, day, login_mode, hour, register_once, current_angle_value, id_register_count, minute, strmonth, second, http_status, log_id, strday, strhour, strminute, strsecond, name_gen_count
  current_mode = mode_name
  current_menu_val.setText(str(mode_name))
  directions_line1.setText(str(dir1))
  directions_line2.setText(str(dir2))
  directions_line3.setText(str(dir3))
  scan_angle_status_label.setText(str(angle_and_status_lab))
  scan_status_val.setText(str(angle_and_status_val))
  a_button_label.setText(str(left_button))
  b_button_label.setText(str(middle_button))
  c_button_label.setText(str(right_button))

# Describe this function...
def register_afterscan_default_menu():
  global variable_speed, stop_speed, degree_change, mode_name, dir1, dir2, dir3, angle_and_status_lab, angle_and_status_val, left_button, middle_button, right_button, login_id, lab_login_val, scan_stat_color, scan_stat_val, current_mode, current_login_id, month, finger_read_mode, day, login_mode, hour, register_once, current_angle_value, id_register_count, minute, strmonth, second, http_status, log_id, strday, strhour, strminute, strsecond, name_gen_count
  wait(1.5)
  current_login_label.show()
  current_login_val.show()
  b_button_label.show()
  c_button_label.show()
  scan_status_val.setColor(0x5dd0cf)
  directions_line1.setColor(0x31981c)
  directions_line2.setColor(0xd7e847)
  directions_line3.setColor(0x9b6638)
  directions_line1.setText('Left button --> Add another fingerprint')
  directions_line2.setText('Middle button --> Sign in as a valid user')
  directions_line3.setText('Right button --> Bed adjustment menu')
  scan_status_val.setText('READY FOR NEXT SCAN!')

# Describe this function...
def login_afterscan_default_meny(login_id, lab_login_val, scan_stat_color, scan_stat_val):
  global variable_speed, stop_speed, degree_change, mode_name, dir1, dir2, dir3, angle_and_status_lab, angle_and_status_val, left_button, middle_button, right_button, current_mode, current_login_id, month, finger_read_mode, day, login_mode, hour, register_once, current_angle_value, id_register_count, minute, strmonth, second, http_status, log_id, strday, strhour, strminute, strsecond, name_gen_count
  current_login_id = login_id
  current_login_val.setText(str(lab_login_val))
  scan_status_val.setColor(scan_stat_color)
  scan_status_val.setText(str(scan_stat_val))
  register_afterscan_default_menu()
  a_button_label.show()
  login_mode = False

# Describe this function...
def change_dir_to_blue():
  global variable_speed, stop_speed, degree_change, mode_name, dir1, dir2, dir3, angle_and_status_lab, angle_and_status_val, left_button, middle_button, right_button, login_id, lab_login_val, scan_stat_color, scan_stat_val, current_mode, current_login_id, month, finger_read_mode, day, login_mode, hour, register_once, current_angle_value, id_register_count, minute, strmonth, second, http_status, log_id, strday, strhour, strminute, strsecond, name_gen_count
  directions_line1.setColor(0x0f5dff)
  directions_line2.setColor(0x0f5dff)
  directions_line3.setColor(0x0f5dff)

# Describe this function...
def oracletimestamp():
  global variable_speed, stop_speed, degree_change, mode_name, dir1, dir2, dir3, angle_and_status_lab, angle_and_status_val, left_button, middle_button, right_button, login_id, lab_login_val, scan_stat_color, scan_stat_val, current_mode, current_login_id, month, finger_read_mode, day, login_mode, hour, register_once, current_angle_value, id_register_count, minute, strmonth, second, http_status, log_id, strday, strhour, strminute, strsecond, name_gen_count
  month = ntp.month()
  day = ntp.day()
  hour = ntp.hour()
  minute = ntp.minute()
  second = ntp.second()
  if month < 10:
    strmonth = (str('0') + str(str(month)))
  else:
    strmonth = str(month)
  if day < 10:
    strday = (str('0') + str(str(day)))
  else:
    strday = str(day)
  if hour < 10:
    strhour = (str('0') + str(str(hour)))
  else:
    strhour = str(hour)
  if minute < 10:
    strminute = (str('0') + str(str(minute)))
  else:
    strminute = str(minute)
  if second < 10:
    strsecond = (str('0') + str(str(second)))
  else:
    strsecond = str(second)
  return (str((ntp.year())) + str(((str('-') + str(((str(strmonth) + str(((str('-') + str(((str(strday) + str(((str('T') + str(((str(strhour) + str(((str(':') + str(((str(strminute) + str(((str(':') + str(((str(strsecond) + str('Z'))))))))))))))))))))))))))))))))


def finger_0_unknownCb():
  global current_mode, current_login_id, month, finger_read_mode, variable_speed, mode_name, login_id, day, login_mode, lab_login_val, hour, register_once, current_angle_value, id_register_count, stop_speed, dir1, scan_stat_color, minute, strmonth, degree_change, dir2, scan_stat_val, second, http_status, log_id, dir3, strday, angle_and_status_lab, angle_and_status_val, strhour, left_button, middle_button, strminute, right_button, strsecond, name_gen_count
  if login_mode == True:
    login_afterscan_default_meny(-1, 'UNKNOWN', 0xcc0000, 'LOGIN FAILED. TRY AGAIN!')
  pass
finger_0.getUnknownCb(finger_0_unknownCb)
def finger_0_cb(user_id, access):
  global current_mode, current_login_id, month, finger_read_mode, variable_speed, mode_name, login_id, day, login_mode, lab_login_val, hour, register_once, current_angle_value, id_register_count, stop_speed, dir1, scan_stat_color, minute, strmonth, degree_change, dir2, scan_stat_val, second, http_status, log_id, dir3, strday, angle_and_status_lab, angle_and_status_val, strhour, left_button, middle_button, strminute, right_button, strsecond, name_gen_count
  if login_mode == True:
    login_afterscan_default_meny(user_id, user_id, 0x33cc00, 'LOGIN SUCCESSFUL!')
  pass
finger_0.readFingerCb(callback=finger_0_cb)

def buttonB_wasPressed():
  global current_mode, current_login_id, month, finger_read_mode, variable_speed, mode_name, login_id, day, login_mode, lab_login_val, hour, register_once, current_angle_value, id_register_count, stop_speed, dir1, scan_stat_color, minute, strmonth, degree_change, dir2, scan_stat_val, second, http_status, log_id, dir3, strday, angle_and_status_lab, angle_and_status_val, strhour, left_button, middle_button, strminute, right_button, strsecond, name_gen_count
  if current_mode == 'Main' and finger_read_mode == True and login_mode == False and register_once == True:
    scan_status_val.setText('LOGGING IN...')
    change_dir_to_blue()
    login_mode = True
    directions_line1.setText('Place your finger on the scanner')
    directions_line2.setText('to log into the system.')
    directions_line3.setText(str(''))
    a_button_label.hide()
    c_button_label.hide()
  elif current_mode == 'Bed adjust' and current_angle_value > 0:
    a_button_label.hide()
    c_button_label.hide()
    move_motor(77, 90, -30)
    a_button_label.show()
    c_button_label.show()
  pass
btnB.wasPressed(buttonB_wasPressed)

def buttonC_wasPressed():
  global current_mode, current_login_id, month, finger_read_mode, variable_speed, mode_name, login_id, day, login_mode, lab_login_val, hour, register_once, current_angle_value, id_register_count, stop_speed, dir1, scan_stat_color, minute, strmonth, degree_change, dir2, scan_stat_val, second, http_status, log_id, dir3, strday, angle_and_status_lab, angle_and_status_val, strhour, left_button, middle_button, strminute, right_button, strsecond, name_gen_count
  if current_mode == 'Main' and finger_read_mode == True and login_mode == False and register_once == True:
    if current_login_id != -1:
      change_between_main_and_adjust('Bed adjust', 'Left button --> Move bed upwards', 'Middle button --> Move bed downwards', 'Right button --> Return to main menu', 'Angle Status: ', (str(current_angle_value) + str(' Degrees')), 'Up', 'Down', 'Escape')
    else:
      error_label.show()
      error_val.setText('PLEASE LOGIN WITH VALID ID!')
      error_val.show()
      wait(2)
      error_label.hide()
      error_val.hide()
  elif current_mode == 'Bed adjust':
    change_between_main_and_adjust('Main', 'Left button --> Add another fingerprint', 'Middle button --> Sign in as a valid user', 'Right button --> Bed adjustment menu', 'Scan Status: ', 'READY FOR NEXT SCAN!', 'Register', 'Login', 'Bed adjust')
  pass
btnC.wasPressed(buttonC_wasPressed)

def buttonA_wasPressed():
  global current_mode, current_login_id, month, finger_read_mode, variable_speed, mode_name, login_id, day, login_mode, lab_login_val, hour, register_once, current_angle_value, id_register_count, stop_speed, dir1, scan_stat_color, minute, strmonth, degree_change, dir2, scan_stat_val, second, http_status, log_id, dir3, strday, angle_and_status_lab, angle_and_status_val, strhour, left_button, middle_button, strminute, right_button, strsecond, name_gen_count
  if current_mode == 'Main' and finger_read_mode == True and login_mode == False:
    finger_read_mode = False
    finger_0.addUser(id_register_count, 1)
    scan_status_val.setText('REGISTERING NEW FINGER...')
    change_dir_to_blue()
    if register_once == True:
      directions_line1.setText('Place your finger on the scanner')
      directions_line2.setText('to register another fingerprint ID')
      directions_line3.setText('')
    current_login_label.hide()
    current_login_val.hide()
    b_button_label.hide()
    c_button_label.hide()
  elif current_mode == 'Bed adjust' and current_angle_value < 90:
    b_button_label.hide()
    c_button_label.hide()
    move_motor(100, 90, 30)
    b_button_label.show()
    c_button_label.show()
  pass
btnA.wasPressed(buttonA_wasPressed)


current_menu_val.setText('Main')
directions_line1.setText('Place your finger on the scanner')
directions_line2.setText('to register your first fingerprint ID.')
directions_line3.setText('')
scan_status_val.setText('SYSTEM INITIALIZED!')
current_login_label.hide()
current_login_val.hide()
b_button_label.hide()
c_button_label.hide()
current_mode = 'Main'
http_status = ''
register_once = False
finger_read_mode = True
login_mode = False
log_id = 0
name_gen_count = 0
id_register_count = 0
current_angle_value = 0
current_login_id = -1
wait(2)
finger_0.removeAllUser()
ntp = ntptime.client(host='cn.pool.ntp.org', timezone=8)
while True:
  if current_mode == 'Main' and finger_read_mode == False:
    if (finger_0.state) == 'Add user success':
      scan_status_val.setColor(0x33cc00)
      scan_status_val.setText('REGISTRATION SUCCESSFUL!')
      try:
        req = urequests.request(method='POST', url='*INSERT YOUR OWN DATABASE CONNECTION LINK HERE*',json={'patient_id':id_register_count,'date_entered':oracletimestamp(),'first_name':((str('John') + str(name_gen_count))),'last_name':((str('Doe') + str(name_gen_count)))}, headers={'Content-Type':'application/json'})
        http_status = 'Success'
        gc.collect()
        req.close()
      except:
        http_status = 'Failure'
      register_once = True
      finger_read_mode = True
      id_register_count = (id_register_count if isinstance(id_register_count, Number) else 0) + 1
      name_gen_count = (name_gen_count if isinstance(name_gen_count, Number) else 0) + 1
      register_afterscan_default_menu()
    elif (finger_0.state) == 'Add user fail':
      scan_status_val.setColor(0xcc0000)
      scan_status_val.setText('REGISTRATION FAILED!')
      finger_read_mode = True
      finger_0.removeUser(id_register_count)
      if register_once == True:
        register_afterscan_default_menu()
  wait_ms(2)
