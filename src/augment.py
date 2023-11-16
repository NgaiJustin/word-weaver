import sys
from dataclasses import dataclass

import pandas as pd
from tqdm import tqdm


@dataclass
class Entry:
    id: int
    lemma: str
    fake_lemma: str
    pos: str
    tag: str
    pronoun: str
    definition: str
    sentence: str
    option1: str
    option2: str
    label: int


def process_entry(entry: pd.Series):
    """
    Process a single row from the csv
    """
    print(f"Before: {entry.sentence}")
    entry.sentence = entry.sentence.replace(
        "_", entry.option2 if entry.label == 1 else entry.option1
    )
    entry.sentence = entry.sentence.replace(entry.fake_lemma, "_")
    print(f"After: {entry.sentence}")

    return entry.sentence


def augment_csv(csv_path):
    """
    Augment the given csv by adding a column with the same name as the csv
    but with a suffix of `_augmented`. The new column will contain the
    augmented data.
    """
    # read csv
    df = pd.read_csv(csv_path)

    # augment data
    augmented_data = df.apply(process_entry, axis=1)  # type: ignore

    # add new column to df
    df[csv_path[:-4] + "_augmented"] = augmented_data

    # write to new csv
    df.to_csv(csv_path[:-4] + "_augmented.csv", index=False)


if __name__ == "__main__":
    # verify only one arg and arg is a file
    if len(sys.argv) != 2 or not sys.argv[1].endswith(".csv"):
        print("Usage: python augment.py <csv_path>")
        sys.exit(1)

    # augment csv and write to `<name>_augmented.csv`
    csv_path = sys.argv[1]
    augment_csv(csv_path)
    print(f"Wrote to {csv_path[:-4]}_augmented.csv")
