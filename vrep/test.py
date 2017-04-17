from env import *

rl_bot = RlBot()

try:
    for i in range(10000):
        observations, reward = rl_bot.step([0.0, 0.0])
        # print(observations['proxy_sensor'])
        print(observations['light_sensor'])
        print(reward['light_sensor'])
except KeyboardInterrupt:
    rl_bot.destroy()
    print('exiting')
