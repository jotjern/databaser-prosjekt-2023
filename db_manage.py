import sqlite3
import os

from database import TogDatabase

if __name__ == "__main__":
    db = TogDatabase("database.db")

    while True:
        cmd = input("Skriv kommando: ")
        if cmd == "setup" or cmd == "reset":
            db.reset_database()
            print("Initialiserte databasen")
        elif cmd == "kunder":
            print("=== Kunder ===")
            for id_, name, email, phone in db.list_customers():
                print(f"{id_}\t{name}\t({email}\t{phone})")
            print("==============")
        elif cmd == "hjelp":
            print("Kommandoer:")
            print("setup: Initialiserer databasen")
            print("kunder: Viser alle kunder")
            print("hjelp: Viser denne hjelpen")
            print("exit: Avslutter programmet")
        else:
            print("Ukjent kommando, skriv hjelp for hjelp")

    # print(db.list_routes_by_day_and_station("mandag", "Trondheim"))
