import json
import time

from axm.lexer import lex
from axm.parser import parse
from axm.runtime import Runtime
from engine.World import World


def load_game_config(path="GAME_CONFIG.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def run():
    # --- load config ---
    config = load_game_config()

    world_name = config["WORLD_NAME"]
    world_tick = config.get("WORLD_TICK", 0.01)
    axm_file = config["AXM_FILE_TO_RUN"]
    debug = config.get("DEBUG", False)

    # --- create world ---
    world = World(world_name)

    # --- load entities ---
    entities = config.get("WORLD_ENTITY", {})
    for name, data in entities.items():
        role = data.get("ROLE", "ENTITY")
        health = data.get("HEALTH", 100)
        x = data.get("X", 0)
        y = data.get("Y", 0)
        z = data.get("Z", 0)

        world.add_entity(name, role, health, x, y, z)

    runtime = Runtime(world)

    # --- load AXM code ---
    with open(axm_file, "r", encoding="utf-8") as f:
        code = f.read()

    tokens = lex(code)
    if debug:
        print("\n" + "="*20)
        print("TOKENS:")
        print("="*20)
        for i, t in enumerate(tokens):
            print(f"  {i:3d}: {t}")

    ast = parse(tokens)
    if debug:
        print("\n" + "="*20)
        print("AST:")
        print("="*20)
        for i, node in enumerate(ast):
            print(f"  {i:3d}: {node}")

    runtime.load(ast)

    # --- main loop ---
    while runtime.running:
        world.tick()
        runtime.tick()
        time.sleep(world_tick)


if __name__ == "__main__":
    run()
