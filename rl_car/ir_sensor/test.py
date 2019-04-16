import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy as np
from env_ir import RLCar
import matplotlib.pyplot as plt
import pickle
from keras.models import load_model, Sequential
from keras.layers import Dense, Activation


def train():
    env = RLCar()

    model = load_model('model_ir.hdf5')

    SPEED = 1
    num_episodes = 1500
    num_steps = 300
    rList = []
    jList = []

    for i in range(num_episodes):
        # Reset environment and get first new observation
        env.reset()
        s, r = env.step([SPEED, SPEED])
        s = s['light_sensor'].reshape((1, -1))
        r = r['light_sensor']
        Q = model.predict(s)
        a = Q.argmax()
        rAll = 0
        done = False
        loss = 0
        # The Q-Network
        for j in range(num_steps):
            # Choose an action by greedily (with e chance of random action)
            # from the Q-network
            Q = model.predict(s)
            a = Q.argmax()
            print("Step {} | State: {} | Action: {} | Reward: {}".format(j, s, a, r))
            # Get new state and reward from environment
            speed = np.zeros(2)
            # Q -> left, right, forward, break
            if a == 0:
                speed[0] = 0
                speed[1] = SPEED
            if a == 1:
                speed[0] = SPEED
                speed[1] = 0
            if a == 2:
                speed[0] = SPEED
                speed[1] = SPEED
            if a == 3:
                speed[0] = 0
                speed[1] = 0

            s_, r_ = env.step(speed)
            s_ = s_['light_sensor'].reshape((1, -1))
            r_ = r_['light_sensor']
            s = s_
            r = r_
            rAll += r
            if done is True:
                break
        # Reduce chance of random action as we train the model.
        jList.append(j)
        rList.append(rAll)
        print("Episode: " + str(i))
        print("Reward: " + str(rAll))

    print("Average number of steps: " + str(sum(jList) / num_episodes))
    print("Average reward: " + str(sum(rList) / num_episodes))

    plt.plot(rList)
    plt.plot(jList)


if __name__ == '__main__':
    try:
        train()
    except KeyboardInterrupt:
        print('Exiting.')
