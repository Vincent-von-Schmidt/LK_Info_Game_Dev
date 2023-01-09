import yaml

with open("data/settings.yaml", "r") as file:
    config: dict = yaml.safe_load(file.read())

debug: bool = config["general"]["debug"]
