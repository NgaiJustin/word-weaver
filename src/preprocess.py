import sys
import random
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


def process_entry(entry: pd.Series, shuffle_letters: bool) -> pd.DataFrame:
    """
    Process a single row from the csv
    """
    word = entry.fake_lemma
    sentence_with_word = entry.sentence.replace(
        "_", entry.option2 if entry.label == 1 else entry.option1
    )
    defintion_of_word = entry.definition

    if shuffle_letters:
        # TODO: perhaps consider a smarter way to shuffle the letter so that the word looks more
        # like a English word
        shuffle_word = list(word)
        random.shuffle(shuffle_word)
        word = "".join(shuffle_word)
        sentence_with_word = sentence_with_word.replace(entry.fake_lemma, word)
        defintion_of_word = defintion_of_word.replace(entry.fake_lemma, word)

    return pd.DataFrame(
        {
            "word": [word],
            "sentence": [sentence_with_word],
            "definition": [defintion_of_word],
        }
    )


def augment_csv(csv_path):
    """
    Augment the given csv by adding a column with the same name as the csv
    but with a suffix of `_augmented`. The new column will contain the
    augmented data.
    """
    # read csv
    df = pd.read_csv(csv_path)
    augmented_df = pd.DataFrame(columns=["word", "sentence", "definition"])

    # create a new augmented_df by processing each entry
    for i, entry in tqdm(df.iterrows(), total=len(df)):
        shuffle_letters = int(i) % 2 == 0  # type: ignore
        processed_df = process_entry(entry, shuffle_letters)
        augmented_df = pd.concat([augmented_df, processed_df], ignore_index=True)  # type: ignore

    # write to new csv
    augmented_df.to_csv(csv_path[:-4] + "_augmented.csv", index=False)


if __name__ == "__main__":
    # verify only one arg and arg is a file
    if len(sys.argv) != 2 or not sys.argv[1].endswith(".csv"):
        print("Usage: python augment.py <csv_path>")
        sys.exit(1)

    # augment csv and write to `<name>_augmented.csv`
    csv_path = sys.argv[1]
    augment_csv(csv_path)
    print(f"Wrote to {csv_path[:-4]}_augmented.csv")
