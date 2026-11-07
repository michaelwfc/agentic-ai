import numpy as np
from tqdm import trange



class Bandit:
    """
    Pseudocode for a complete bandit algorithm using incrementally computed sample averages and epsilion-greedy action selection

    initialize, for a = 1 to k:
        Q(a) = 0
        N(a) = 
    loop:
        # do greedy action selection
        A =  argmax(Q(a))     , with probability of 1-epsilon
             a random action  , with probability of epsilon
        # bandit function take an action and return a corresponding reward.
        R = bandit(A) 
        # update the actions
        N(A) = N(A) +1
        # incrementally computed sample averages
        Q(A) = Q(A) + 1/N(A)( R - Q(A))

    """    
    def __init__(self, k_arm=10, epsilon=0., initial=0., step_size=0.1, sample_averages=False, UCB_param=None,
                 gradient=False, gradient_baseline=False, true_reward=0.):
        """_summary_

        Args:
            k_arm (int, optional): # of arms. Defaults to 10.
            epsilon (_type_, optional): probability for exploration in epsilon-greedy algorithm. Defaults to 0..
            initial (_type_, optional):  initial estimation for each action. Defaults to 0..
            step_size (float, optional):  constant step size for updating estimations. Defaults to 0.1.
            sample_averages (bool, optional): if True, use sample averages to update estimations instead of constant step size. Defaults to False.
            UCB_param (_type_, optional):  if not None, use UCB algorithm to select action. Defaults to None.
            gradient (bool, optional): if True, use gradient based bandit algorithm. Defaults to False.
            gradient_baseline (bool, optional): if True, use average reward as baseline for gradient based bandit algorithm. Defaults to False.
            true_reward (_type_, optional): _description_. Defaults to 0..
        """                 
        self.k = k_arm
        self.step_size = step_size
        self.sample_averages = sample_averages
        self.indices = np.arange(self.k)
        self.time = 0
        self.UCB_param = UCB_param
        self.gradient = gradient
        self.gradient_baseline = gradient_baseline
        self.average_reward = 0
        self.true_reward = true_reward
        self.epsilon = epsilon
        self.initial = initial

    
    def reset(self):
        """reset after each run
        """
        # set the initial estimate reward to zeor
        # ? set the true reward for each run ? 
        self.q_true = np.random.randn(self.k) + self.true_reward
        # initial and maintain estimates of the action values
        self.q_estimation = np.zeros(self.k) + self.initial
        # initial and maintain actions
        self.action_count = np.zeros(self.k)

        # best action
        self.best_action =  np.argmax(self.q_true)
    
    def act(self):
        """take action at step by epslion-greed  action selection

        Args:
            step: _description_
        """
        """
        # get the action  by max estimate reward 
        action = np.argmax(self.q_estimation)
        # random choose at each action
        probability = np.zeros(self.k) + self.epsilon/self.k
        # add probability of 1-self.epsilon at max estimation reward
        probability[action] = probability[action] + (1-self.epsilon)
        # choose the action by probability
        action = np.random.choice(a= self.indices,p=probability)
        """
        if np.random.rand() < self.epsilon:
            action =  np.random.choice(self.indices)
        
        elif self.UCB_param:
            # if use upper confidence bound (UCB) action selection instead of greed
            ucb_estimation  = self.q_estimation + self.UCB_param* np.sqrt(np.log(self.time+1))/(self.action_count+1e-5)
            action =np.random.choice(np.where(ucb_estimation== ucb_estimation.max())[0])
        else:
            max_estimation = self.q_estimation.max()
            action =np.random.choice(np.where(self.q_estimation== max_estimation)[0])
            
        # update the action states
        self.action_count[action] += 1

        return action


    
    def step(self,action:int):
        """take an action, get an reward, and  update estimation for this action incrementally computed sample averages
        Args:
            action: _description_
        """
        # get the true reward of action
        q_ture = self.q_true[action]
        # add random
        reward = np.random.randn() + q_ture
        if self.sample_averages:
            # in stationary, estimate aciton valut by sample average the past valuse
            # update the estimation of action by incrementally computed sample averages
            self.q_estimation[action] += 1/self.action_count[action] * (reward - self.q_estimation[action])
        else:
            # in nonstatinayr, a weighted average of past rewards and the initial estimate Q1 is better
            # update estimation with constant step size
            self.q_estimation[action] += self.step_size * (reward - self.q_estimation[action])
        
        self.time +=1
        return reward

def run_simulate():
    reward_record = np.zeros(shape= (runs,steps))
    bandit = Bandit(epsilon=epsilon,sample_averages=True)
    for run in trange(runs,desc='runing'):
        bandit.reset()
        for step in range(steps):
            # choose an aciton by epsilion-greedy action selection
            action = bandit.take_action(step)
            # get reward for the current step
            reward = bandit.step(action)
            # record the reward
            reward_record[run,step] =  reward

    # draw a pic of fig_2_2
    average_reward = reward_record.mean(axis=0)
    return average_reward

if __name__ == "__main__":
    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np
    from tqdm import trange
    from rl_introduction_course_code.chapter02.ten_armed_testbed import simulate

    runs=1000
    steps=2000
    epsilon = 0.1  

    epsilons = [0.1, 0, 0.01]
    bandits = [Bandit(epsilon=eps, sample_averages=True) for eps in epsilons]
    best_action_counts, rewards = simulate(runs, steps, bandits)

    plt.figure(figsize=(10, 20))

    for eps, rewards in zip(epsilons, rewards):
        plt.plot(rewards, label='$\epsilon = %.02f$' % (eps))
    plt.xlabel('steps')
    plt.ylabel('average reward')
    plt.legend()

