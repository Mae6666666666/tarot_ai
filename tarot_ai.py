from random import randint
import random
from config import API_KEY, BASE_URL, MODEL
import json
import requests
from ddgs import DDGS
from openai import OpenAI

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

AI_DESCRIPTION = {
    "name":"Caine",
    "system_prompt": """
You are a tarot reader AI. Your role is to give thoughtful, creative, and slightly mystical tarot readings based on the cards provided.

The user will give you:
- Their reason for the reading
- A list of tarot cards drawn

You must follow these rules:

1. CARD STRUCTURE:
- The first card represents the SITUATION
- The second card represents the CHALLENGE
- The third card represents the OUTCOME

2. EXTRA CARDS (REVERSALS):
- If there are more than 3 cards, the extra cards are "reversed" meanings
- These reversed cards mirror the first cards in order:
    - 4th card = reversed SITUATION
    - 5th card = reversed CHALLENGE
    - 6th card = reversed OUTCOME

3. INTERPRETATION STYLE:
- Be imaginative, mystical, and slightly dramatic but still clear
- Do NOT be overly scary or negative
- Keep it appropriate for a general audience
- Focus on reflection, guidance, and possibilities—not fixed fate

4. OUTPUT FORMAT:
Structure your response EXACTLY like this:

🔮 Tarot Reading 🔮

✨ Your Question:
[Repeat or summarize the user's reason]

🃏 Your Cards:
- Situation: [Card Name]
- Challenge: [Card Name]
- Outcome: [Card Name]

(If extra cards exist, add:)
- Reversed Situation: [Card Name]
- Reversed Challenge: [Card Name]
- Reversed Outcome: [Card Name]

🌙 Interpretation:
- Situation: [Meaning]
- Challenge: [Meaning]
- Outcome: [Meaning]

(If reversed cards exist, add:)
- Reversed Situation: [Meaning]
- Reversed Challenge: [Meaning]
- Reversed Outcome: [Meaning]

🌟 Final Insight:
Give a short overall conclusion tying everything together.

5. CARD MEANINGS:
Use general tarot meanings:
- Major Arcana = big life themes
- Cups = emotions/relationships
- Pentacles = money/work/material life
- Swords = thoughts/conflict
- Wands = action/energy

Reversed cards should suggest:
- blockage
- delay
- internal struggle
- or opposite energy

Keep interpretations concise but meaningful.
"""
}


tarot_cards = [
    # Major Arcana (22)
    "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor",
    "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit",
    "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance",
    "The Devil", "The Tower", "The Star", "The Moon", "The Sun",
    "Judgement", "The World",

    # Minor Arcana - Cups (14)
    "Ace of Cups", "Two of Cups", "Three of Cups", "Four of Cups", "Five of Cups",
    "Six of Cups", "Seven of Cups", "Eight of Cups", "Nine of Cups", "Ten of Cups",
    "Page of Cups", "Knight of Cups", "Queen of Cups", "King of Cups",

    # Minor Arcana - Pentacles (14)
    "Ace of Pentacles", "Two of Pentacles", "Three of Pentacles", "Four of Pentacles", "Five of Pentacles",
    "Six of Pentacles", "Seven of Pentacles", "Eight of Pentacles", "Nine of Pentacles", "Ten of Pentacles",
    "Page of Pentacles", "Knight of Pentacles", "Queen of Pentacles", "King of Pentacles",

    # Minor Arcana - Swords (14)
    "Ace of Swords", "Two of Swords", "Three of Swords", "Four of Swords", "Five of Swords",
    "Six of Swords", "Seven of Swords", "Eight of Swords", "Nine of Swords", "Ten of Swords",
    "Page of Swords", "Knight of Swords", "Queen of Swords", "King of Swords",

    # Minor Arcana - Wands (14)
    "Ace of Wands", "Two of Wands", "Three of Wands", "Four of Wands", "Five of Wands",
    "Six of Wands", "Seven of Wands", "Eight of Wands", "Nine of Wands", "Ten of Wands",
    "Page of Wands", "Knight of Wands", "Queen of Wands", "King of Wands"
]

user_cards = []

why_the_reading = input("Why do you want this reading today?: ")
count = 0


for i in range(1, 4):
    count += 1
    double_card = randint(1, 20)
    random_card = ""
    print(input(f"Generating card number {count}..."))
    random_card += (random.choice(tarot_cards))
    print(random_card)
    tarot_cards.remove(random_card)
    user_cards.append(random_card)
    if double_card == 1:
        input("Oh? whats this?")
        input("The tarot gods must really have a lot to say to you today...")
        input("You got an extra card! press enter to see the extra card!")
        random_card = ""
        random_card += (random.choice(tarot_cards))
        print(random_card)
        user_cards.append(random_card)
        tarot_cards.remove(random_card)
print("Please wait, consulting the stars...")
# print("Your cards for today are: ")
# print(user_cards)

messages = [
        {"role": "system", "content": AI_DESCRIPTION["system_prompt"]},
        {"role": "user", "content": f"""
        Reason for reading: {why_the_reading}
        Cards drawn: {user_cards}
"""}]

response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
        )

message = response.choices[0].message.content
print(message)
