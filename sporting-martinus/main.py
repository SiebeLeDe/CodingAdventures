import pathlib as pl
from dataclasses import dataclass


@dataclass
class Player:
    first_name: str
    family_name: str


def load_team_members(file_path: pl.Path):
    team_members = []
    with open(file_path, "r") as file:
        for line in file:
            first_name, *family_name = line.strip().split(" ")
            team_members.append(Player(first_name=first_name, family_name=" ".join(family_name)))
    return team_members


def generate_training_schedule(team_members):
    # Placeholder for training schedule generation logic
    raise NotImplementedError("Training schedule generation is not implemented yet.")


def generate_bar_list_schedule(team_members):
    # Placeholder for bar list schedule generation logic
    raise NotImplementedError("Bar list schedule generation is not implemented yet.")


def main():
    print("Hello from sporting-martinus!")
    parent_dir = pl.Path(__file__).parent
    team_members_file = parent_dir / "spelerslijst.txt"

    print(f"Loading team members from: {team_members_file}")
    team_members = load_team_members(team_members_file)
    print("Team Members:")
    for member in team_members:
        print(f"- {member.first_name} {member.family_name}")


if __name__ == "__main__":
    main()
