import csv

def save_to_csv_news(data, filename="data/news.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Index", "Title"])
        for idx, item in enumerate(data, start=1):
            writer.writerow([idx, item])
def save_to_csv_quotes(data, filename="data/quotes.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Index", "Title"])
        for idx, item in enumerate(data, start=1):
            writer.writerow([idx, item])
