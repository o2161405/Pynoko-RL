import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pandas as pd
import pynoko
from pynoko import Trick, Course, Character, Vehicle

# Get ghost file inputs used for resetting the Env
inputs = pd.read_csv("ghost.csv", header=None).values.tolist()
tricks = {
    0: Trick.NoTrick,
    1: Trick.Up,
    2: Trick.Down,
    3: Trick.Left,
    4: Trick.Right
}

# Define low and high values for the state
low = np.array([

])
high = np.array([

])

class MKWEnv(gym.Env):
    def __init__(self):
        # Kinoko Setup
        self.mkw = pynoko.KHostSystem()
        self.mkw.configure(Course.Luigi_Circuit, Character.Funky_Kong, Vehicle.Spear, False)
        self.mkw.init()

        # Gym Setup
        self.state = None
        self.observation_space = spaces.Box(low=low, high=high, dtype=np.float64)
        self.action_space = spaces.MultiDiscrete(np.array([
            2, # A, not A
            2, # B, not B
            5, # DPAD
            15, # Stick X
            15, # Stick Y
        ]))
        self.EPISODE_FRAMES = 0
        self.MAX_EPISODE_FRAMES = 5 * 60 * 60 # 18000 Frames
        self.DECAY_DECREMENT_END = 0.5

        # Reward & Done function variables
        self.lastRaceCompletion = 0
        self.rewardMultiplier = 1
        self.offroadVulnerableFrames = 0

    def step(self, action):
        # Reset environment initially
        if self.state is None: 
            self.state = self.reset()

        if self.lastRaceCompletion == None:
            self.lastRaceCompletion = self.mkw.raceCompletion()

        buttons = pynoko.buttonInput([])

        if action[0]:
            buttons += pynoko.KPAD_BUTTON_A

        if action[1]:
            buttons += pynoko.KPAD_BUTTON_B

        self.mkw.setInput(
                buttons,
                action[3] + 7,
                action[4] + 7,
                tricks[action[2]]
            )
        self.mkw.calc()

        # Update count offroad frames
        kart = self.mkw.kartObjectProxy()
        if kart.move().kclSpeedFactor() < 1.0:
            self.offroadVulnerableFrames += 1
        else:
            self.offroadVulnerableFrames = 0

        # Get new observation
        observation = self.getState()
        self.state = (observation - self.observation_space.low) / (self.observation_space.high - self.observation_space.low)

        # Determine reward and done flag
        reward = self.getReward()
        done = self.getDone()

        # Optional information
        info = {}

        self.EPISODE_FRAMES += 1
        self.lastRaceCompletion = self.mkw.raceCompletion()

        return self.state, reward, done, info

    def getState(self):
        kart = self.mkw.kartObjectProxy()
        kartState = kart.state()
        kartMove = kart.move()
        itemDirector = self.mkw.itemDirector()
        return np.array([
            *kart.pos().to_numpy(),
            *kart.main_rot().to_numpy(),
            *kart.ang_vel_2().to_numpy(),
            *kart.velocity().to_numpy(),
            kart.acceleration(),
            kart.is_bike(),
            kart.speed_ratio(),
            *kart.int_vel().to_numpy(),
            *kart.ext_vel().to_numpy(),

            kartState.isDrifting(),
            kartState.isInATrick(),
            kartState.isMushroomBoost(),
            kartState.isTouchingGround(),
            kartState.isTrickable(),
            kartState.isWheelie(),

            kartMove.driftState(),
            kartMove.mtCharge(),

            itemDirector.itemInventory(0).currentCount(),

            self.offroadVulnerableFrames,
            self.EPISODE_FRAMES,
        ])
    
    def getReward(self):
        reward = (self.mkw.raceCompletion() - self.lastRaceCompletion) * self.rewardMultiplier
        self.rewardMultiplier = max(self.rewardMultiplier - ((1 - self.DECAY_DECREMENT_END) / self.MAX_EPISODE_FRAMES), self.DECAY_DECREMENT_END)
        return reward

    def getDone(self):
        done = False
        kart = self.mkw.kartObjectProxy()

        # If RaceCompletion >4
        if self.mkw.raceManager().stage() == pynoko.RaceManager.Stage.FinishLocal:
            done = True

        # If offroad and not shrooming
        # kclSpeedFactor takes into account offroad invincibility (1.0 when invincible)
        if kart.move().kclSpeedFactor() < 1.0:
            done = True

        # If it's offroad and not in a shroom for a little bit
        # Allows agent to use the speed after the end of a shroom
        if self.offroadVulnerableFrames > 100:
            done = True

        if self.EPISODE_FRAMES > self.MAX_EPISODE_FRAMES:
            done = True

        return done

    def reset(self):
        # Reset Kinoko
        self.mkw.reset()

        # Skip turn around animation
        for _ in range(172):
            self.mkw.calc()

        # Walk Kinoko to a certain point using the ghost
        for frame in range(np.random.randint(400, 1100)):
            buttons = pynoko.buttonInput([])

            if inputs[frame][0]:
                buttons += pynoko.KPAD_BUTTON_A
            
            if inputs[frame][1]:
                buttons += pynoko.KPAD_BUTTON_B

            if inputs[frame][2]:
                buttons += pynoko.KPAD_BUTTON_ITEM

            self.mkw.setInput(
                buttons,
                inputs[frame][3] + 7,
                inputs[frame][4] + 7,
                tricks[inputs[frame][5]]
            )
            self.mkw.calc()

        self.lastRaceCompletion = None
        self.offroadVulnerableFrames = 0
        self.EPISODE_FRAMES = 0

        # Get observation and normalize
        observation = self.getState()
        observation = (observation - self.observation_space.low) / (self.observation_space.high - self.observation_space.low)

        return observation
    
    def render(self):
        pass

env = MKWEnv()
env.reset()