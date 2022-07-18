import numpy as np
import env
import generate_actions as generate
import sys
import utilities as ut
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

"""
agent.py is based on FMZennaro's agent on https://github.com/FMZennaro/CTF-RL/blob/master/Simulation1/agent.py
"""

class Agent():
    def __init__(self, url, verbose, deterministic, exploration, number_of_episodes):
        self.env = env.SQLi_Environment(url, verbose)

        self.verbose = verbose
        self.deterministic = deterministic
        self.exploration = exploration
        self.set_learning_options()
        self.used_actions = []
        self.powerset = None

        self.steps = 0
        self.rewards = 0
        self.total_steps = 0
        self.steps_each_trial = []
        self.rewards_each_trial = []
        self.total_trials = 0
        self.total_successes = 0
        self.url = url
        self.number_of_episodes = number_of_episodes

        self.max_columns = 3
        self.actions = generate.generate_actions(None, self.max_columns)
        self.num_actions = len(self.actions)
        self.Q = {(): np.ones(self.num_actions)}

    def set_learning_options(self, learningrate=0.1,discount=0.9, max_step = 1000):
        #self.expl = exploration
        self.lr = learningrate
        self.discount = discount
        self.max_step = max_step

    def _select_action(self):
        if (np.random.random() < self.exploration and not self.deterministic):
            if self.verbose:
                print("Choosing a random action")
            return np.random.randint(0,self.num_actions)
        else:
            return np.argmax(self.Q[self.state])

    def step(self):
        self.steps = self.steps + 1
        #print(f"Step {self.steps}:")

        if self.verbose:
            print()
            print(f"Step {self.steps}:")
            print(f"My state is: {self.state}")
            print(f"My Q row looks like this: {self.Q[self.state]}")
            print(f"My action ranking is: {np.argsort(self.Q[self.state])[::-1]}")

        action = self._select_action()
        if self.verbose:
            print(f"Choosing action number {action}")
            print("Action equal highest rank: ",action == np.argsort(self.Q[self.state])[::-1][0])


        state_resp, reward, termination, result_message = self.env.step(action)
        self.rewards = self.rewards + reward
        self._analyze_response(action, state_resp, reward)
        self.terminated = termination
        self.used_actions.append(action)
        if self.verbose:
            print(result_message)
        return

    #vuln_type determines what kind of vulnerability the environment should be set to
        #1 = Stack based
        #2 = Union based
        #3 = Stack based + input filter
        #4 = Union based + input filter
        #5 = random
    def run_episode(self, vuln_type):
        _,_,self.terminated,debug_message = self.env.reset(vuln_type)

        if(self.verbose):
            print(f"{debug_message}\n\n\n")

        while (not self.terminated) and (self.steps < self.max_step):
            self.step()

        self.total_trials += 1
        self.total_steps += self.steps
        self.steps_each_trial.append(self.steps)
        self.rewards_each_trial.append(self.rewards)
        self.steps = 0
        self.rewards = 0
        if(self.terminated):
            self.total_successes += 1
        return self.terminated



    def _update_state(self, action_nr, response_interpretation):
        """
        action_nr is an integer between 0 and num_actions
        response interpretation is either -1 or 1
        """
        action_nr += 1
        x = list(set(list(self.state) + [response_interpretation*action_nr]))
        x.sort()
        x = tuple(x)
        self.Q[x] = self.Q.get(x, np.ones(self.num_actions))

        self.oldstate = self.state
        self.state = x


    def _update_Q(self, action, reward):
        best_action_newstate = np.argmax(self.Q[self.state])
        self.Q[self.oldstate][action] = self.Q[self.oldstate][action] + self.lr * (reward + self.discount*self.Q[self.state][best_action_newstate] - self.Q[self.oldstate][action])


    def _analyze_response(self, action, response, reward):
        expl1 = 1     # Successfull SQLi, but query did not get flag (should probably be using union based instead of stack based)
        expl2 = 2     # Correct escape character, but broke query
        flag  = 3     # FLAG
        wrong1 = 0     # Wrong escape
        wrong2 = -1 # Should not be returned


        #The response is triggering some kind of SQLi on the website
        if(response==expl1 or response==expl2 or response == flag):
            self._update_state(action, response_interpretation = 1)
        #The response is not triggering any SQLi on the website
        elif(response==wrong1):
            self._update_state(action, response_interpretation = -1)
        else:
            print("ILLEGAL RESPONSE")
            sys.exit()

        self._update_Q(action, reward)


    def reset(self,env):
        self.env = env
        self.terminated = False
        self.state = () #empty tuple
        self.oldstate = None
        self.used_actions = []

        self.steps = 0
        self.rewards = 0

    def run(self):
        a.reset(self.env)
        for i in range(number_of_episodes):
            a.run_episode()
        if verbose:
            print(f"\nSteps per trial: {a.steps_each_trial}")
            print(f"Total steps: {a.total_steps}")
            print(f"Number of trials: {a.total_trials} \nNumber of successes: {a.total_successes}")


if __name__ == "__main__":
    #Parse command line arguments
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    #Kan fjerne deterministic? Samme resultat av exploration=0
    parser.add_argument("-d", "--deterministic", help="Deterministic actions", action="store_true")
    parser.add_argument("-v", "--verbose", help="Verbose", action="store_true")
    parser.add_argument("-e", "--exploration", help="Exploration rate", action="store", type=float, choices=[(x/10) for x in range(0, 11, 1)], default=0.2)
    parser.add_argument("-u", "--url", help="URL", action="store", type=str, default="http://127.0.0.1:8000")
    parser.add_argument("-n", "--nepisodes", help="Number of episodes", action="store", type=int, default=10)
    args = vars(parser.parse_args())
    parser.add_argument("-t", "--type", help="Vulnerability type (1 = Stack based, 2 = Union based, 3 = Stack based + input filter, 4 = Union based + input filter, 5 = Random type)", action="store", type=int, choices=[(x) for x in range(0, 6, 1)], default=1)

    verbose = args["verbose"]
    deterministic = args["deterministic"]
    exploration = args["exploration"]
    url = args["url"]
    number_of_episodes = args["nepisodes"]
    vuln_type = args["type"]

    a = Agent(url, verbose, deterministic, exploration, number_of_episodes, vuln_type)

    a.run()
