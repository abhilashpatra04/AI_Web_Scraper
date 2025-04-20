def parse_prompt(prompt):
    prompt = prompt.lower()
    if "hacker news" in prompt:
        return {"site": "hacker news", "data": "titles"}
    elif "quotes" in prompt or "quotes to scrape" in prompt:
        return {"site": "quotes.toscrape.com", "data": "quotes"}
    else:
        return {"site": None, "data": None}
