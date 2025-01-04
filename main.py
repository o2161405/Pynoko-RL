from pathlib import Path
from datetime import datetime
import argparse

import numpy as np
#import pandas as pd

import gymnasium as gym
from gymnasium import spaces

from stable_baselines3 import DQN, PPO

import pynoko
from pynoko import Trick, Course, Character, Vehicle

# Get ghost file inputs used for resetting the Env
#inputs = pd.read_csv("ghost.csv", header=None).values.tolist()
tricks = {
    0: Trick.NoTrick,
    1: Trick.Up,
    2: Trick.Down,
    3: Trick.Left,
    4: Trick.Right
}

MAX_EPISODE_FRAMES = 5 * 60 * 60 # 18000 Frames

# Define low and high values for the state
low = np.array([
    0, # Race completion
    # --- KartObject --- #
    -24595, # Pos X
    530, # Pos Y
    -13731.7, # Pos Z
    0, # Main Rot X
    0, # Main Rot Y
    0, # Main Rot Z
    0, # Main Rot W
    -150, # Angular Velocity X
    -150, # Angular Velocity Y
    -150, # Angular Velocity Z
    -150, # Velocity X
    -150, # Velocity Y
    -150, # Velocity Z
    -150, # Acceleration
    0, # isBike
    0, # speedRatio
    -120, # Internal Velocity X
    -120, # Internal Velocity Y
    -120, # Internal Velocity Z
    -120, # External Velocity X
    -120, # External Velocity Y
    -120, # External Velocity Z

    # --- KartState --- #
    0, # isDrifting
    0, # isInATrick
    0, # isMushroomBoost
    0, # isTouchingGround
    0, # isTrickable
    0, # isWheelie

    # --- KartMove --- #
    0, # driftState
    0, # mtCharge

    # --- ItemInventory --- #
    0,

    # --- Class Variables --- #
    0, # offroadVulnerableFrames
    0 # current_frame
], dtype=np.float32)

high = np.array([
    4.2, # Race completion
    # --- KartObject --- #
    23083, # Pos X
    3500, # Pos Y
    54637, # Pos Z
    1, # Main Rot X
    1, # Main Rot Y
    1, # Main Rot Z
    1, # Main Rot W
    150, # Angular Velocity X
    150, # Angular Velocity Y
    150, # Angular Velocity Z
    150, # Velocity X
    150, # Velocity Y
    150, # Velocity Z
    150, # Acceleration
    1, # isBike
    1, # speedRatio
    120, # Internal Velocity X
    120, # Internal Velocity Y
    120, # Internal Velocity Z
    120, # External Velocity X
    120, # External Velocity Y
    120, # External Velocity Z

    # --- KartState --- #
    1, # isDrifting
    1, # isInATrick
    1, # isMushroomBoost
    1, # isTouchingGround
    1, # isTrickable
    1, # isWheelie

    # --- KartMove --- #
    2, # driftState
    270, # mtCharge

    # --- ItemInventory --- #
    3,

    # --- Class Variables --- #
    100, # offroadVulnerableFrames
    MAX_EPISODE_FRAMES # current_frame
], dtype=np.float32)

class MKWEnv(gym.Env):
    def __init__(self):
        # Kinoko Setup
        self.mkw = pynoko.KHostSystem()
        self.mkw.configure(Course.Luigi_Circuit, Character.Funky_Kong, Vehicle.Spear, False)
        self.mkw.init()

        # Gym Setup
        self.observation_space = spaces.Box(low=low, high=high, dtype=np.float32)
        self.action_space = spaces.MultiDiscrete(np.array([
            2, # A, not A
            2, # B, not B
            15, # Stick X
            15, # Stick Y
            5, # DPAD
        ]))
        self.current_frame = 0
        self.DECAY_DECREMENT_END = 0.5

        # Reward & Done function variables
        self.rewardMultiplier = 1
        self.offroadVulnerableFrames = 0

    def step(self, action):
        buttons = pynoko.buttonInput([])

        if action[0]:
            buttons += pynoko.KPAD_BUTTON_A

        if action[1]:
            buttons += pynoko.KPAD_BUTTON_B

        self.mkw.setInput(
                buttons,
                action[2],
                action[3],
                tricks[action[4]]
            )
        self.mkw.calc()

        # Update count offroad frames
        kart = self.mkw.kartObjectProxy()
        if kart.move().kclSpeedFactor() < 1.0:
            self.offroadVulnerableFrames += 1
        else:
            self.offroadVulnerableFrames = 0

        # Get new observation
        state = self.getState()

        # Determine reward and done flag
        reward = self.getReward()
        done = self.getDone()

        # Optional information
        info = {}
        truncated = False

        self.current_frame += 1

        return state, reward, done, truncated, info

    def getState(self):
        kart = self.mkw.kartObjectProxy()
        kartState = kart.state()
        kartMove = kart.move()
        itemDirector = self.mkw.itemDirector()

        currentDrift = kartMove.driftState()
        match currentDrift:
            case pynoko.KartMove.DriftState.NotDrifting:
                currentDrift = 0
            case pynoko.KartMove.DriftState.ChargingMt:
                currentDrift = 1
            case pynoko.KartMove.DriftState.ChargedMt:
                currentDrift = 2
            case pynoko.KartMove.DriftState.ChargedSmt:
                currentDrift = 3

        observation = np.array([
            self.mkw.raceCompletion(),
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

            currentDrift,
            kartMove.mtCharge(),

            itemDirector.itemInventory(0).currentCount(),

            self.offroadVulnerableFrames,
            self.current_frame
        ], dtype=np.float32)

        return (observation - self.observation_space.low) / (self.observation_space.high - self.observation_space.low)
    
    def getReward(self):
        if self.lastRaceCompletion == None:
            self.lastRaceCompletion = self.mkw.raceCompletion()

        reward = (self.mkw.raceCompletion() - self.lastRaceCompletion) * self.rewardMultiplier

        self.lastRaceCompletion = self.mkw.raceCompletion()
        self.rewardMultiplier = max(self.rewardMultiplier - ((1 - self.DECAY_DECREMENT_END) / MAX_EPISODE_FRAMES), self.DECAY_DECREMENT_END)
        return reward

    def getDone(self):
        done = False
        kart = self.mkw.kartObjectProxy()

        # If RaceCompletion >4
        if self.mkw.raceManager().stage() == pynoko.RaceManager.Stage.FinishLocal:
            print("Finish frame: ", self.current_frame)
            done = True

        """
        # If offroad and not shrooming
        # kclSpeedFactor takes into account offroad invincibility (1.0 when invincible)
        if kart.move().kclSpeedFactor() < 0.8:
            print("Offroad frame: ", selef.current_frame)
            done = True
        """

        # If it's offroad and not in a shroom for a little bit
        # Allows agent to use the speed after the end of a shroom
        if self.offroadVulnerableFrames > 60:
            print("Offroad frame: ", self.current_frame)
            done = True

        if self.current_frame >= MAX_EPISODE_FRAMES:
            done = True

        if done:
            print("Done completion: ", self.mkw.raceCompletion())


        return done

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        # Reset Kinoko
        self.mkw.reset()

        # Skip turn around animation
        for _ in range(172):
            self.mkw.calc()

        """
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
        """

        self.lastRaceCompletion = None
        self.offroadVulnerableFrames = 0
        self.current_frame = 0

        # Get observation and normalize
        observation = self.getState()

        return observation, {}
    
    def render(self):
        pass


def main(args):
    MODEL_DIR = Path("models")
    MODEL_DIR.mkdir(exist_ok=True)

    if args.model == None:
        if args.mode == "train":
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            model_file = MODEL_DIR / ("model_" + timestamp)
        elif args.mode == "test":
            model_file = MODEL_DIR / "model_best"
        elif args.mode == "retrain":
            print("--model argument required in retrain mode")
            exit(1)
    else:
        model_file = args.model

    env = MKWEnv()

    if args.mode == "train":
        model = PPO("MlpPolicy", env, verbose=1)
    else:
        model = PPO.load(model_file, env=env)

    if args.mode == "train" or args.mode == "retrain":
        model.learn(total_timesteps=1e6)

        model.save(str(model_file))
        print(f"Saved model {model_file}")

    # TODO: test


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script operations: train, test, retrain.")
    parser.add_argument(
        "mode",
        choices=["train", "test", "retrain"],
        help="Choose the operation: 'train', 'test', or 'retrain'."
    )
    parser.add_argument(
        "--model",
        type=str,
        required=False,
        help="Path to the model file."
    )
    args = parser.parse_args()
    main(args)
