from agent.parser import parse_prompt
from agent.utils import save_to_csv_quotes, save_to_csv_news
from scraper.base_scraper import scrape_hacker_news, scrape_quotes


def main():
    user_input = input("Ask me to scrape something: ")
    task = parse_prompt(user_input)

    if task['site'] == 'hacker news':
        data = scrape_hacker_news()
        save_to_csv_news(data)
    elif task['site'] == 'quotes from toscrape.com':
        data = scrape_quotes()
        save_to_csv_quotes(data)
    else:
        print("Sorry, that site is not supported yet.")


if __name__ == "__main__":
    main()