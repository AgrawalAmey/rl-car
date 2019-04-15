import os
import pickle

from keras.models import load_model, Sequential
from keras.layers import Dense, Activation
import matplotlib.pyplot as plt
import numpy as np

from .env import RLBot


def train():
    env = RLBot()

    try:
        model = load_model('data/model.hdf5')
    except:
        model = Sequential()
        model.add(Dense(units=80, input_dim=40))
        model.add(Activation("relu"))
        model.add(Dense(units=40))
        model.add(Activation("relu"))
        model.add(Dense(units=20))
        model.add(Activation("relu"))
        model.add(Dense(units=3))
        model.add(Activation("relu"))
        model.compile(optimizer='Adam', loss='mse')

    # Set learning parameters
    y = .99
    e = 0.1
    num_episodes = 1500
    num_steps = 300
    # create lists to contain total rewards and steps per episode
    jList = []
    rList = []
    lList = []
    SPEED = 0.7

    for i in range(num_episodes):
        # Reset environment and get first new observation
        env.reset()
        s, r, _ = env.step([SPEED, SPEED])
        s = s.reshape((1, -1))
        Q = model.predict(s)
        a = Q.argmax()
        rAll = 0
        loss = 0
        # The Q-Network
        for j in range(num_steps):
            print("Step {} | State: {} | Action: {} | Reward: {}".format(j, s, a, r))
            # Choose an action by greedily (with e chance of random action)
            # from the Q-network
            Q = model.predict(s)
            a = Q.argmax()
            if np.random.rand(1) < e:
                a = np.random.randint(3)
                print("e = {}. Choosing Random Action: {}".format(e, a))
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

            s_, r_, done = env.step(speed)
            s_ = s_.reshape((1, -1))

            # Obtain the Q' values by feeding the new state through our network
            Q_ = model.predict(s_)
            # Obtain maxQ' and set our target value for chosen action.
            maxQ_ = np.max(Q_)
            targetQ = Q
            targetQ[0, a] = r + y * maxQ_
            # Train our network using target and predicted Q values
            loss += model.train_on_batch(s, targetQ)
            rAll += r
            s = s_
            r = r_
            if done:
                break
        # Reduce chance of random action as we train the model.
        e -= 0.001
        jList.append(j)
        rList.append(rAll)
        lList.append(loss)
        print("Episode: " + str(i))
        print("Loss: " + str(loss))
        print("e: " + str(e))
        print("Reward: " + str(rAll))
        pickle.dump({'jList': jList, 'rList': rList, 'lList': lList},
                    open("data/history.p", "wb"))
        model.save('data/model.hdf5')

    print("Average loss: " + str(sum(lList) / num_episodes))
    print("Average number of steps: " + str(sum(jList) / num_episodes))
    print("Average reward: " + str(sum(rList) / num_episodes))

    plt.plot(rList)
    plt.plot(jList)
    plt.plot(lList)

if __name__ == '__main__':
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    try:
        train()
    except KeyboardInterrupt:
        print('Exiting.')