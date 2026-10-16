import sys

import yaml


def set_hero(variant: str) -> None:
    with open("content/site.yaml") as f:
        data = yaml.safe_load(f)
    data["hero_variant"] = variant
    with open("content/site.yaml", "w") as f:
        yaml.safe_dump(data, f)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        set_hero(sys.argv[1])
