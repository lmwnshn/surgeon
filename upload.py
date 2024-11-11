import pickle
from datasets import Dataset


MAILING_LISTS = [
    "pgsql-hackers",
    "pgsql-performance",
]


def main():
    DATASET = {}
    FILTERED_TEXTS = {}
    for mailing_list in MAILING_LISTS:
        with open(f"./dataset_{mailing_list}.pickle", "rb") as f:
            DATASET[mailing_list] = {}
            DATASET[mailing_list]["threads"] = pickle.load(f)
        ds = Dataset.from_dict(DATASET[mailing_list])
        ds.push_to_hub(f"wanshenl/{mailing_list}")
        with open(f"./filteredtexts_{mailing_list}.pickle", "rb") as f:
            FILTERED_TEXTS[mailing_list] = {}
            FILTERED_TEXTS[mailing_list] = pickle.load(f)
        ds = Dataset.from_dict(FILTERED_TEXTS[mailing_list])
        ds.push_to_hub(f"wanshenl/{mailing_list}-processed")


if __name__ == "__main__":
    main()

