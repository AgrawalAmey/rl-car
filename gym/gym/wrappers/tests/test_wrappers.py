import gym
from gym import error
from gym import wrappers
from gym.wrappers import SkipWrapper

import tempfile
import shutil


def test_skip():
    every_two_frame = SkipWrapper(2)
    env = gym.make("FrozenLake-v0")
    env = every_two_frame(env)
    obs = env.reset()
    env.render()

def test_configured():
    env = gym.make("FrozenLake-v0")
    env = wrappers.TimeLimit(env)
    env.configure()

    # Make sure all layers of wrapping are configured
    assert env._configured
    assert env.env._configured
    env.close()

# TODO: Fix Cartpole issue and raise WrapAfterConfigureError correctly
# def test_double_configured():
#     env = gym.make("FrozenLake-v0")
#     every_two_frame = SkipWrapper(2)
#     env = every_two_frame(env)
#
#     env.configure()
#     try:
#         env = wrappers.TimeLimit(env)
#     except error.WrapAfterConfigureError:
#         pass
#     else:
#         assert False
#
#     env.close()

def test_no_double_wrapping():
    temp = tempfile.mkdtemp()
    try:
        env = gym.make("FrozenLake-v0")
        env = wrappers.Monitor(env, temp)
        try:
            env = wrappers.Monitor(env, temp)
        except error.DoubleWrapperError:
            pass
        else:
            assert False, "Should not allow double wrapping"
        env.close()
    finally:
        shutil.rmtree(temp)
