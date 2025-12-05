"""Esempio minimale di dungeon master assistito da chatbot.

Questo file mostra una struttura pronta da espandere:
- Modello dati di gioco (personaggi, stato, azioni).
- Motore di narrazione che può usare un LLM oppure un fallback deterministico.
- Ciclo CLI interattivo per testare rapidamente le tue idee.

Personalizza liberamente le classi o i prompt di narrazione in base al tuo regolamento.
"""

import os
import random
import textwrap
from dataclasses import dataclass, field
from typing import Optional

from openai import OpenAI


# --- Modello di dominio ----------------------------------------------------

@dataclass
class Character:
    """Rappresenta un personaggio giocante o non giocante."""

    name: str
    razza: str
    classe: str
    livello: int
    punti_ferita: int

    def apply_damage(self, amount: int) -> None:
        """Applica danni al personaggio senza scendere sotto zero."""

        self.punti_ferita = max(self.punti_ferita - amount, 0)

    def is_conscious(self) -> bool:
        """Ritorna True se il personaggio è ancora in grado di agire."""

        return self.punti_ferita > 0


@dataclass
class GameState:
    """Stato condiviso della sessione: location e membri del party."""

    location: str
    party: list[Character] = field(default_factory=list)
    scena_corrente: int = 1

    def snapshot(self) -> str:
        """Restituisce un riassunto testuale dello stato."""

        party_lines = [
            (
                f"- {pg.name} ({pg.razza} {pg.classe} liv. {pg.livello}) "
                f"— {pg.punti_ferita} PF"
            )
            for pg in self.party
        ]
        return textwrap.dedent(
            f"""
            Scena: {self.scena_corrente}
            Luogo: {self.location}
            Party:
            {os.linesep.join(party_lines) if party_lines else 'Nessun membro' }
            """
        ).strip()

    def advance_scene(self) -> None:
        """Incrementa il contatore di scena per tracciare il progresso."""

        self.scena_corrente += 1


# --- Motore di narrazione --------------------------------------------------

class NarrationEngine:
    """Genera descrizioni di scena usando un LLM o un fallback locale."""

    def __init__(self, client: Optional[OpenAI], system_prompt: str) -> None:
        self.client = client
        self.system_prompt = system_prompt

    def narrate(self, action: str, state: GameState) -> str:
        """Crea la narrazione in base all'azione del giocatore e allo stato."""

        prompt = self._build_prompt(action, state)

        # Se hai configurato una API key valida, usa il modello.
        if self.client:
            return self._call_model(prompt)

        # Altrimenti usa un generatore locale semplice ma riproducibile.
        return self._fallback_narration(action, state)

    def _build_prompt(self, action: str, state: GameState) -> str:
        """Costruisce un prompt strutturato pronto per il modello."""

        return textwrap.dedent(
            f"""
            Sei un Dungeon Master esperto. Descrivi la prossima scena.

            Stato attuale:
            {state.snapshot()}

            Istruzioni:
            - Rispondi in 4-6 frasi concise.
            - Mantieni il tono fantasy medioevale.
            - Non introdurre modifiche alle regole, solo narra l'esito.

            Azione del giocatore: {action}
            """
        ).strip()

    def _call_model(self, prompt: str) -> str:
        """Chiama il modello OpenAI con il system prompt fornito."""

        response = self.client.chat.completions.create(
            model="gpt-5.1",  # Cambia modello a seconda della tua disponibilità.
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content

    def _fallback_narration(self, action: str, state: GameState) -> str:
        """Genera una breve narrazione senza chiamate di rete."""

        outcomes = [
            "un incontro imprevisto con una creatura errante",
            "un indizio nascosto inciso su una pietra consunta",
            "una trappola che scatta con un suono metallico",
            "un PNG che chiede aiuto con tono disperato",
            "una stanza vuota che nasconde un passaggio segreto",
        ]
        consequence = random.choice(outcomes)

        # Per dare sensazione di progresso, avanzare scena e menzionarla.
        state.advance_scene()
        return textwrap.fill(
            (
                f"Mentre reagite a '{action}', la scena {state.scena_corrente} si apre: "
                f"{consequence}. Il party resta a {state.location}, ma l'atmosfera "
                "cambia e vi prepara alla prossima scelta."
            ),
            width=88,
        )


# --- Applicazione CLI ------------------------------------------------------

def build_openai_client(api_key: Optional[str]) -> Optional[OpenAI]:
    """Restituisce un client OpenAI se è disponibile una API key esplicita."""

    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def prompt_for_api_key() -> Optional[str]:
    """Chiede all'utente se vuole inserire la propria API key se non è in env."""

    existing_key = os.getenv("OPENAI_API_KEY")
    if existing_key:
        # Se la chiave è già impostata nell'ambiente usiamola direttamente.
        return existing_key

    choice = input(
        "Hai una OPENAI_API_KEY da usare? [s/N]: ".strip()
    ).strip().lower()
    if choice not in {"s", "si", "sì"}:
        return None

    typed_key = input("Inserisci ora la tua OPENAI_API_KEY: ").strip()
    return typed_key or None


def prompt_character_creation() -> Character:
    """Permette al giocatore di scegliere nome, razza e classe per il proprio PG."""

    print("\n--- Creazione del personaggio giocante ---")
    name = input("Nome del personaggio: ").strip() or "Eroe senza nome"

    available_races = [
        "Umano",
        "Elfo",
        "Nano",
        "Halfling",
        "Tiefling",
    ]
    available_classes = [
        "Guerriero",
        "Ladro",
        "Mago",
        "Chierico",
        "Ranger",
    ]

    def choose_from_list(options: list[str], label: str) -> str:
        print(f"Scegli la {label}:")
        for idx, option in enumerate(options, start=1):
            print(f"  {idx}) {option}")
        choice = input("Inserisci il numero o lascia vuoto per default: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print(f"Nessuna scelta valida, userò {options[0]} come default.")
        return options[0]

    razza = choose_from_list(available_races, "razza")
    classe = choose_from_list(available_classes, "classe")

    return Character(name=name, razza=razza, classe=classe, livello=1, punti_ferita=20)


def run_cli(state: GameState, engine: NarrationEngine) -> None:
    """Loop di prova per interagire con il motore di narrazione."""

    print("Benvenuto nel tavolo di prova! Digita 'quit' per uscire.\n")
    while True:
        action = input("Cosa fa il giocatore? ").strip()
        if action.lower() in {"quit", "exit"}:
            print("Sessione terminata. A presto!")
            return
        if not action:
            print("Nessuna azione inserita. Riprova.\n")
            continue

        narration = engine.narrate(action, state)
        print("\n--- Dungeon Master (AI) ---")
        print(narration)
        print("\nStato riassunto:")
        print(state.snapshot())
        print("\n")


# --- Esecuzione dimostrativa ----------------------------------------------

if __name__ == "__main__":
    # Crea il personaggio del giocatore con scelte guidate.
    player_character = prompt_character_creation()

    # Compagni di esempio che puoi modificare o rimuovere.
    party = [
        player_character,
        Character(
            name="Lira", razza="Mezzelfa", classe="Ladra", livello=3, punti_ferita=22
        ),
        Character(
            name="Thamior", razza="Elfo", classe="Mago", livello=3, punti_ferita=16
        ),
    ]
    initial_state = GameState(location="Cripte di Smeraldo", party=party)

    # Prompt di sistema coerente con il tuo tono di campagna.
    system_prompt = (
        "Sei un Dungeon Master che segue fedelmente lo stato di gioco fornito. "
        "Narra con toni fantasy classici, mantieni la coerenza e non barare con le regole."
    )

    api_key = prompt_for_api_key()
    engine = NarrationEngine(
        client=build_openai_client(api_key), system_prompt=system_prompt
    )
    run_cli(initial_state, engine)
