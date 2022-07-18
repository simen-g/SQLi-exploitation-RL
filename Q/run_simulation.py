import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter as SGfilter
from IPython.display import clear_output
import datetime
import joblib
from tqdm import tqdm

import const
import utilities as ut
from env import SQLi_Environment
from agent import Agent

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

def train_agent_many_steps_and_analyze(agent, env, nepisodes, vuln_type):
    states = []
    agent.reset(env)
    for _ in tqdm(range(nepisodes)):
        agent.run_episode(vuln_type)
        states.append(ut.getdictshape(agent.Q)[0])

    steps = agent.steps_each_trial
    rewards = agent.rewards_each_trial

    print(steps)

    #plotting states per episode
    plt.plot(states)
    plt.xlabel('episodes')
    plt.ylabel('number of states')
    plt.show()

    #plotting steps per episode
    plt.plot(steps)
    #plt.plot(np.mean(np.array(steps).reshape(-1,5),axis=))
    plt.xlabel('episodes')
    plt.ylabel('number of steps')
    plt.show()

    #plotting reward per episode
    plt.plot(rewards)
    plt.xlabel('episodes')
    plt.ylabel('number of rewards')
    plt.show()

    #Smoothed line
    plt.plot(SGfilter(steps,10,0))
    plt.xlabel('episodes')
    plt.ylabel('number of steps')
    plt.show()


if __name__=="__main__":

    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    #Kan fjerne deterministic? Samme resultat av exploration=0
    parser.add_argument("-d", "--deterministic", help="Deterministic actions", action="store_true")
    parser.add_argument("-v", "--verbose", help="Verbose", action="store_true")
    parser.add_argument("-e", "--exploration", help="Exploration rate", action="store", type=float, choices=[(x/10) for x in range(0, 11, 1)], default=0.2)
    parser.add_argument("-u", "--url", help="URL", action="store", type=str, default="http://127.0.0.1:8000")
    parser.add_argument("-n", "--nepisodes", help="Number of Episodes", action="store", type=int, default=10)
    parser.add_argument("-t", "--type", help="Vulnerability type (1 = Stack based, 2 = Union based, 3 = Stack based + input filter, 4 = Union based + input filter, 5 = Random type)", action="store", type=int, choices=[(x) for x in range(0, 6, 1)], default=1)

    args = vars(parser.parse_args())
    verbose = args["verbose"]
    deterministic = args["deterministic"]
    exploration = args["exploration"]
    url = args["url"]
    number_of_episodes = args["nepisodes"]
    vuln_type = args["type"]

    agent = Agent(url, verbose, deterministic, exploration, number_of_episodes)
    env = SQLi_Environment(url, verbose)

    #run_one_episode_and_analyze(agent, env)
    train_agent_many_steps_and_analyze(agent, env, number_of_episodes, vuln_type)
