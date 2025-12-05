import os
from openai import OpenAI
from ai_backend import chiama_modello

client = OpenAI(api_key=os.getenv("testapikey"))

def chiama_modello(prompt: str) -> str:
    """
    Invia un prompt al modello ChatGPT e restituisce il testo generato.
    """
    response = client.chat.completions.create(
        model="gpt-5.1",
        messages=[
            {"role": "system", "content": "Sei un Dungeon Master in un gioco fantasy."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

while True:
    azione = input("Cosa vuoi fare? ")
    prompt = f"Il giocatore fa: {azione}. Descrivi cosa accade dopo."

    risposta = chiama_modello(prompt)
    print("\n--- Dungeon Master (AI) ---")
    print(risposta)