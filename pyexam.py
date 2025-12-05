class Umano:

    def __init__(self, nome, vita_base, attacco_base, difesa_base, mana):
        self.nome = nome
        self.vita = vita_base
        self.attacco = attacco_base
        self.difesa = difesa_base
        self.mana = mana

    def è_vivo(self):
        return self.vita > 0

    def __str__(self):
        return (
            f"=== Scheda Personaggio ===\n"
            f"Nome: {self.nome}\n"
            f"Vita: {self.vita}\n"
            f"Attacco: {self.attacco}\n"
            f"Difesa: {self.difesa}\n"
        )

    import random

    def dadi(num_dadi, facce=6):
        if num_dadi < 1:
            raise ValueError("Il numero di dadi deve essere almeno 1")

        risultati = []
        for _ in range(num_dadi):
            rnd = random.Random()  # nuova istanza Random per ogni dado
            risultato = rnd.randint(1, facce)
            risultati.append(risultato)

        totale = sum(risultati)
        return totale

    # Esempio d'uso:
    # totale = dadi(3, 6)
    # print(f"Totale: {totale}")
    class Guerriero(Umano):
        def __init__(self, nome, vita_base, attacco_base, difesa_base, forza, punti_ferita, stamina, inventory):
            super().__init__(nome, vita_base, attacco_base, difesa_base)
            self.forza = forza
            self.punti_ferita = punti_ferita
            self.stamina = stamina
            self.inventory = inventory

        def __str__(self):
            return (
                f"=== Scheda Personaggio ===\n"
                f"Nome: {self.nome}\n"
                f"Vita: {self.vita}\n"
                f"Attacco: {self.attacco}\n"
                f"Difesa: {self.difesa}\n"
                f"forza: {self.forza}\n"
                f"punti_ferita: {self.punti_ferita}\n"
                f"stamina: {self.stamina}\n"
            )

    Vichingo = Guerriero("Thor", 100, 40, 15, forza=25, punti_ferita=100, stamina=50)

    Giaguaro = Guerriero("Kukulkán", 80, 30, 25, forza=20, punti_ferita=80, stamina=25)

    import random

    import Class_Umano_2025

    class mago(Umano):
        def __init__(self, nome):
            self.nome = nome
            self.vita_base += 10
            self.livello_magia = 5
            self.numero_incantesimi = 4
            self.incantesimi = {"palla di fuoco": 10,
                                "palla di ghiaccio": 8,
                                "lancio di fulmine": 12,
                                }

        def lancia_incantesimo(self, altro_personaggio):
            if not hasattr(altro_personaggio, 'resisti_incantesimo'):
                self.magia = random.choice(list(self.incantesimi.values()))
                altro_personaggio.vita_totale -= self.magia
            else:
                altro_personaggio.resisti_incantesimo()
            self.numero_incantesimi -= 1


class Orco:
    def __init__(self):
        self.nome = "Orco"

        self.vita_totale = 50

    def attacca(self, altro):
        altro.vita_totale -= 10

    def use_items(self):
        for item in self.inventory:
            # Mago
            if self.mago == "Mago":
                if item == "potion":
                    self.vita_base += self.vita_base * 0.5
                    self.mana += self.mana * 0.3
                    print(f"{self.nome} usa {item}: +50% Vita, +30% Mana")
                elif item == "staff":
                    self.mana -= 20
                    self.attaco_base += 25
                    print(f"{self.nome} usa {item}: -20 Mana, +25 Attaco")
                else:
                    print(f"{item} non trova questo item.")

            # guarrierro
            elif self.Guerrierro == "Guerrierro":
                if item == "sword":
                    self.attaco_base += 30
                    self.stamina -= 15
                    life_steal = 0.1 * self.attaco_base
                    self.vita_base += life_steal
                    print(f"{self.nome} usa {item}: +30 Attaco, -15 Stamina, +{life_steal:.1f} HP")
                elif item == "shield":
                    self.difesa_base += 20
                    self.stamina -= 10
                    print(f"{self.nome} usa {item}: +20 Difeso, -10 Stamina")
                else:
                    print(f"{item} non trova questo item.")

            else:
                print(f"{self.nome} non trova questo item.")
