from pymycobot.mycobot import MyCobot
import time

class MyArm:
    def __init__(self, port="COM5", baurd=115200) :
        
        self.port = port
        self.baurd = baurd
        
        
    def connect(self) :
        return MyCobot(self.port, self.baurd)
    
    def pick(self, mc) :
        mc.set_gripper_value(40, 40)
        time.sleep(2)
        mc.send_angles([95.8, 33.48, -44.47, -47.72, 84.11, 0.35], 40)
        time.sleep(5)
        mc.send_angles([89.64, 3.42, -70.57, -23.63, 89.82, 3.42], 40)
        time.sleep(2)
        mc.set_gripper_value(13, 40)
        time.sleep(2)
        mc.send_angles([95.8, 33.48, -44.47, -47.72, 84.11, 0.35], 40)
        time.sleep(2)
        mc.send_angles([60.55, 6.24, -27.5, -31.11, 26.36, 0.17], 40)
        time.sleep(2)
        
    def angleReset(self, mc) :
        mc.send_angles([0, 0, 0, 0, 0, 0], 20)
        time.sleep(2)
        
    def yellow_one(self, mc) :
        mc.send_angles([2.9, 24.87, -73.91, -27.5, 90.43, 1.14], 40)
        time.sleep(2)
        mc.set_gripper_value(40, 40)
        time.sleep(2)
        mc.send_angles([8.61, 43.68, -80.41, -12.39, 83.23, 5.09], 40)
        time.sleep(2)
        
    def orange_one(self, mc) :
        mc.send_angles([0.96, -16.52, -30.76, -33.75, 90, 2.1], 40)
        time.sleep(2)
        mc.set_gripper_value(60, 40)
        time.sleep(2)
        mc.send_angles([6.76, -6.15, -35.06, -19.42, 85.86, 10.19], 40)
        time.sleep(2)
        
    def red_one(self, mc) :
        mc.send_angles([1.4, -42.89, 10.45, -39.11, 90.08, -0.08], 40)
        time.sleep(2)
        mc.set_gripper_value(60, 40)
        time.sleep(2)
        mc.send_angles([1.58, -35.85, -7.73, 6.5, 91.05, -4.04], 40)
        time.sleep(2)
        
    def green(self, mc) :
        mc.send_angles([40.25, -24.69, -59.76, -3.16, 92.98, 5.62], 40)
        time.sleep(2)
        mc.set_gripper_value(60, 40)
        time.sleep(2)
        mc.send_angles([40.86, -3.33, -27.68, -37.44, 90.61, -4.04], 40)
        time.sleep(2)
        
        
def main() :
    myArm = MyArm("COM10", 115200)
    mc = myArm.connect()
    mc.set_gripper_mode(0)
    myArm.angleReset(mc)
    myArm.pick(mc)
    # myArm.yellow_one(mc)
    # myArm.orange_one(mc)
    # myArm.red_one(mc)
    myArm.green(mc)
    myArm.angleReset(mc)
    mc.set_gripper_value(0, 40)
    
if __name__ == '__main__':
    main()