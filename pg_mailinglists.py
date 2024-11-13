from datasets import Dataset, load_dataset
from pathlib import Path


def main():
    MAILING_LISTS = [
        "pgsql-hackers",
        "pgsql-performance",
    ]
    for f in Path(".").glob("pgsql*"):
        f.unlink()
    for mailing_list in MAILING_LISTS:
        dataset = load_dataset(f"wanshenl/{mailing_list}", split="train")
        for i, row in enumerate(dataset):
            thread = row["threads"]
            if len(thread) == 0:
                continue
            filename = f"{mailing_list}_thread_{i}.txt"
            folder = Path("mailinglists")
            folder.mkdir(exist_ok=True)
            with open(folder / filename, "w") as f:
                for msg in thread:
                    msg_date = msg["msg_date"]
                    msg_from = msg["msg_from"]
                    msg_subject = msg["msg_subject"]
                    msg_contents = msg["msg_contents"]
                    print(f"Date: {msg_date}", file=f)
                    print(f"From: {msg_from}", file=f)
                    print(f"Subject: {msg_subject}", file=f)
                    print(f"Body: {msg_contents}", file=f)


if __name__ == "__main__":
    main()
