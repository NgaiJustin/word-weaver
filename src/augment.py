import pandas as pd
import sys


def augment_csv(csv_path):
    """
    Augment the given csv by adding a column with the same name as the csv
    but with a suffix of `_augmented`. The new column will contain the
    augmented data.
    """
    # read csv
    df = pd.read_csv(csv_path)

    # augment data
    augmented_data = []
    for row in df.iterrows():
        augmented_data.append(row[1][0] + 1)

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
