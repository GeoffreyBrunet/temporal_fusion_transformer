from data.process_data import Process_data


if __name__ == "__main__":
    path = "../data/LD2011_2014.txt.zip"
    process_data = Process_data
    df = process_data.generate_data(path)
    print(df.head)
    