import sqlite3
import os
import datetime

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

            for customer in db.list_customers():
                print(f"{customer['KundeNr']}\t| {customer['Navn']}\t| {customer['Epost']}\t| {customer['Telefon']}")
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
            for route in db.list_routes_by_day_and_station(day, station):
                print(f"{route['TogruteID']}\t| {route['OperatørNavn']}")
            print("============================================================")
        elif cmd == "finn reise":
            start_station = input("Startstasjon: ")
            end_station = input("Endestasjon: ")
            date = input("Dato (YYYY-MM-DD): ")
            time = input("Tidspunkt (HH:MM): ")
            if start_station and end_station and date and time:
                date1 = datetime.date.fromisoformat(date)
                date2 = date1 + datetime.timedelta(days=1)
                trips1, trips2 = db.find_trip(start_station, end_station, date, time)
                print(f"==== Reiser {date1.isoformat()} ====================")
                for trip in trips1:
                    print(
                        f"RuteID: {trip['TogruteID']}, Fra {trip['StartNavn']} "
                        f"Til {trip['StoppNavn']}, Avreise kl {trip['Tid']}")
                print(f"==== Reiser {date2.isoformat()} ====================")
                for trip in trips2:
                    print(
                        f"RuteID: {trip['TogruteID']}, Fra {trip['StartNavn']} "
                        f"Til {trip['StoppNavn']}, Avreise kl {trip['Tid']}")
            else:
                print("Avbrutt")
        elif cmd == "hjelp":
            print("Kommandoer:")
            print("reset: Resetter databasen")
            print("kunder: Viser alle kunder")
            print("finn reise: Finner reiser")
            print("hjelp: Viser denne hjelpen")
            print("exit: Avslutter programmet")
        else:
            print("Ukjent kommando, skriv hjelp for hjelp")
