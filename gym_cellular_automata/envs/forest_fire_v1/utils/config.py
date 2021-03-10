import numpy as np
from pathlib import Path

from gym import spaces

# Solves './gym_cellular_automata/envs/forest_fire_v1/'
forest_fire_dir = Path(__file__).parents[1]

FOREST_FIRE_CONFIG_FILE = forest_fire_dir / "forest_fire_v1.yaml"


def get_config_dict(file):
    import yaml

    yaml_file = open(file, "r")
    yaml_content = yaml.load(yaml_file, Loader=yaml.SafeLoader)
    return yaml_content


def get_forest_fire_config_dict():
    config = get_config_dict(FOREST_FIRE_CONFIG_FILE)

    config["effects"] = parse_effects(config)

    config["wind"] = parse_wind(config)

    return config


def parse_wind(config):

    # fmt: off
    up_left    = config["wind_probs"]["up_left"]
    up         = config["wind_probs"]["up"]
    up_right   = config["wind_probs"]["up_right"]
    left       = config["wind_probs"]["left"]
    self       = config["wind_probs"]["self"]
    right      = config["wind_probs"]["right"]
    down_left  = config["wind_probs"]["down_left"]
    down       = config["wind_probs"]["down"]
    down_right = config["wind_probs"]["down_right"]
    
    wind = np.array(
        [[up_left,   up,     up_right],
         [left,      self,      right],
         [down_left, down, down_right]],
    )
    # fmt: on

    wind_space = spaces.Box(0.0, 1.0, shape=(3, 3))

    assert wind_space.contains(wind), "Bad Wind Data, check ranges [0.0-1.0]"

    return wind


def parse_effects(config):
    effects_str = config["effects"]
    effects = dict()

    for cell_name in effects_str:
        cell_symbol = config["cell_symbols"][cell_name]

        substitution_name = effects_str[cell_name]
        substitution = config["cell_symbols"][substitution_name]

        effects[cell_symbol] = substitution

    return effects


CONFIG = get_forest_fire_config_dict()
