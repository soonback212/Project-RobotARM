from pymycobot.mycobot import MyCobot
import time

mc = MyCobot("COM5", 115200)

print("gripper test")
mc.set_gripper_mode(0) # 0: 열림, 1: 닫힘
mc.init_eletric_gripper()
mc.set_gripper_calibration()


print("close")
mc.set_gripper_state(1,20)
time.sleep(4)
print(mc.get_gripper_value())


print("open")
mc.set_gripper_state(0,20)
time.sleep(4)
print(mc.get_gripper_value())

print("close")
mc.set_gripper_state(1,20)
time.sleep(4)
print(mc.get_gripper_value())