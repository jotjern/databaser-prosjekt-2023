import sqlite3
import os

from database import TogDatabase

if __name__ == "__main__":
    db = TogDatabase("database.db")

    if not db.is_initialized():
        db.reset_database()

    while True:
        cmd = input("Skriv kommando: ")
        if cmd == "reset":
            db.reset_database()
            print("Initialiserte databasen")
        elif cmd == "kunder":
            print("=== Kunder =================================================")

            for id_, name, email, phone in db.list_customers():
                print(f"{id_}\t| {name}\t| {email}\t| {phone}")
            print("============================================================")
        elif cmd == "ny kunde":
            name = input("Navn: ")
            email = input("Epost: ")
            phone = input("Telefon: ")
            if name and email and phone:
                db.add_customer(name, email, phone)
                print("Kunde lagt til")
            else:
                print("Avbrutt")
        elif cmd == "finn ruter":
            day = input("Dag: ")
            station = input("Stasjon: ")
            print(f"=== Ruter på {day} fra {station} ==========================")
            for id_, from_, to_, day_, time_ in db.list_routes_by_day_and_station(day, station):
                print(f"{id_}\t| {from_}\t| {to_}\t| {day_}\t| {time_}")
            print("============================================================")
        elif cmd == "hjelp":
            print("Kommandoer:")
            print("reset: Resetter databasen")
            print("kunder: Viser alle kunder")
            print("hjelp: Viser denne hjelpen")
            print("exit: Avslutter programmet")
        else:
            print("Ukjent kommando, skriv hjelp for hjelp")

    # print(db.list_routes_by_day_and_station("mandag", "Trondheim"))
