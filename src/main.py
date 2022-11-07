from src.data.process_data import generate_data


if __name__ == "__main__":
    df = generate_data("../data/LD2011_2014.txt.zip")
    print(df.head)
    