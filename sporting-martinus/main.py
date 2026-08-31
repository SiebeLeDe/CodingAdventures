import pathlib as pl
from dataclasses import dataclass
import random
from collections.abc import Sequence, MutableSequence
from datetime import datetime, timedelta


@dataclass
class Player:
    first_name: str
    family_name: str

    def __str__(self) -> str:
        return f"{self.first_name} {self.family_name}"

    def __lt__(self, other: "Player") -> bool:
        return self.first_name[0].lower() < other.first_name[0].lower()


def generate_training_dates(start_date: str, end_date: str, interval_days: int) -> list[str]:
    """Generate a list of training dates between start_date and end_date with a given interval."""

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    delta = timedelta(days=interval_days)

    dates = []
    current_date = start
    while current_date <= end:
        dates.append(current_date.strftime("%Y-%m-%d"))
        current_date += delta

    return dates


def shuffle_team_members(team_members: MutableSequence[Player]) -> None:
    """Shuffle the list of team members in place."""
    random.shuffle(team_members)


def load_team_members(file_path: pl.Path):
    team_members = []
    with open(file_path, "r") as file:
        for line in file:
            first_name, *family_name = line.strip().split(" ")
            team_members.append(Player(first_name=first_name, family_name=" ".join(family_name)))
    team_members.sort()
    return team_members


def not_available_data(date: str, dates: Sequence[str], periods: Sequence[tuple[str, str]]) -> bool:
    """
    Check if a given date is in the list of dates or within any of the specified periods.
    """
    if date in dates:
        return True
    for start, end in periods:
        if start <= date <= end:
            return True
    return False


def generate_training_schedule(team_members: Sequence[Player], start_date: str, end_date: str, interval_days: int) -> dict[str, Player]:
    """
    Randomly assign team members to training sessions.

    Example start_date: "2026-09-02"
    Example end_date: "2027-06-02"
    Example interval_days: 7 (once a week)
    """
    skip_dates = ["2026-09-09"]
    skip_periods = [("2026-12-12", "2027-01-12")]
    dates = generate_training_dates(start_date, end_date, interval_days)
    schedule = {}
    for i, date in enumerate(dates):
        member = team_members[i % len(team_members)]
        if not_available_data(date, skip_dates, skip_periods):
            continue
        schedule[date] = member

    return schedule


def generate_bar_list_schedule(team_members):
    # Placeholder for bar list schedule generation logic
    raise NotImplementedError("Bar list schedule generation is not implemented yet.")


def main():
    print("Hello from sporting-martinus!")
    parent_dir = pl.Path(__file__).parent
    team_members_file = parent_dir / "spelerslijst.txt"

    # print(f"Loading team members from: {team_members_file}")
    team_members = load_team_members(team_members_file)
    shuffle_team_members(team_members)

    with open(parent_dir / "spelerslijst-random.txt", "w") as file:
        file.writelines(f"{member.first_name} {member.family_name}\n" for member in team_members)

    # For training schedule generation
    start_date = "2026-09-02"
    end_date = "2027-06-02"
    interval_days = 7  # Once a week

    training_schedule = generate_training_schedule(team_members, start_date, end_date, interval_days)
    print("Training Schedule:")
    for date, member in training_schedule.items():
        print(f"- {date}: {member}")

    # training_schedule_file = parent_dir / "2026_2027-SPM4-trainingsschema.csv"
    # # Save the training schedule to a CSV file
    # with open(training_schedule_file, "w") as file:
    #     file.write("Datum,Naam\n")
    #     for date, member in training_schedule.items():
    #         file.write(f"{date},{member.first_name}\n")


if __name__ == "__main__":
    main()
