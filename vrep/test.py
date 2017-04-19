from env import RLBot

bot = RLBot()

try:
    for i in range(10000):
        observations, reward = bot.step([1, 1])
        # print(observations['proxy_sensor'])
        print(observations['light_sensor'])
        print(reward['light_sensor'])
except KeyboardInterrupt:
    bot.destroy()
    print('exiting')
