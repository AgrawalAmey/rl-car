from env import *

rl_bot = RlBot()

for i in range(10000):
    observations = rl_bot.step([0.1, 0.1])
    print(observations['proxy_sensor_vals'])
    print(observations['light_sensor_vals'])

rl_bot.distroy()
