import polars as pl

def make_fake_data(path="data/fake_data.csv"):
    data = {
        "id": [1, 2, 3, 4, 5],
        "name": ["Alice", "Bob", "Charlie", "Diana", "Ethan"],
        "age": [25, 30, 35, 40, 28],
        "city": ["London", "Manchester", "Bristol", "Leeds", "Liverpool"],
        "score": [88, 92, 79, 85, 90],
    }
    df = pl.DataFrame(data)
    df.write_csv(path)
    print(f"Saved fake data to {path}")

if __name__ == "__main__":
    make_fake_data()
