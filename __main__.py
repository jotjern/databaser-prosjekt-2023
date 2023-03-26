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
            print("Database reset")
        elif cmd == "kunder":
            print("=== Kunder =================================================")
            for customer in db.list_customers():
                print(f"{customer['KundeNr']}\t| {customer['Navn']}\t| {customer['Epost']}\t| {customer['TlfNr']}")
            print("============================================================")
        elif cmd == "ny kunde":
            name = input("Navn: ")
            email = input("Epost: ")
            phone = input("Telefon: ")
            if name and email and phone:
                customer_id = db.add_customer(name, email, phone)
                print(f"Kunde #{customer_id} lagt til")
            else:
                print("Avbrutt")
        elif cmd == "kjøp billett":
            route_id = int(input("RuteID: "))
            date = input("Dato (YYYY-MM-DD): ")
            print("Hvilken vogn vil du kjøpe billett til?")
            for carriage in db.count_carriages_free_seats(route_id, date):
                name = {"Seng": "senger", "Sete": "seter"}[carriage["Type"]]
                print(f"Vogn #{carriage['VognNr']} har {carriage['LedigePlasser']} ledige {name}")
            carriage_number = int(input("Vognnummer: "))
            print("Hvilken plass vil du kjøpe?")
            for seat in db.find_tickets_in_carriage(route_id, date, carriage_number):
                print(f"{seat['PlassType']} #{seat['PlassNr']} er ledig")
            seat_number = int(input("Setenummer: "))
            customer_id = int(input("Hva er din kunde-ID? "))
            from_station = input("Fra stasjon: ")
            to_station = input("Til stasjon: ")
            db.purchase_ticket(route_id, date, carriage_number, seat_number, customer_id, from_station, to_station)
            print("Billett kjøpt!")
        elif cmd == "finn ruter":
            day = input("Dag: ")
            station = input("Stasjon: ")
            print(f"Ruter på {day} fra {station}:")
            for route in db.list_routes_by_day_and_station(day, station):
                print(f"\tRute #{route['TogruteID']} operert av {route['OperatørNavn']} går kl. {route['Tidspunkt']}")

        elif cmd == "finn reise":
            start_station = input("Startstasjon: ")
            end_station = input("Endestasjon: ")
            date = input("Dato (YYYY-MM-DD): ")
            time = input("Tidspunkt (HH:MM): ")

            if start_station and end_station and date and time:
                day_1_date = datetime.date.fromisoformat(date)
                day_2_date = day_1_date + datetime.timedelta(days=1)
                trips = db.find_trips(start_station, end_station, date, time)
                print(f"Reiser {day_1_date.isoformat()} og {day_2_date.isoformat()}:")
                for trip in trips:
                    print(f"\tRute #{trip['TogruteID']} fra {trip['StartNavn']} "
                          f"til {trip['StoppNavn']} går kl. {trip['Avgang']}")
                print("Billetter kan kjøpes med kommandoen 'kjøp billett'")
            else:
                print("Avbrutt")

        elif cmd == "se kjøp":
            customer_id = int(input("Kunde-ID: "))
            print(f"Kunde #{customer_id} sine billetter:")
            for ticket in db.find_future_purchases_by_customer(customer_id):
                # TogruteID, Dato, PlassNr, VognNr, FraStasjon, TilStasjon, OrdreNr, KjopDato, KjopTidspunkt, Kundenr
                print(f"\tOrdre #{ticket['OrdreNr']} - Rute #{ticket['TogruteID']} fra {ticket['FraStasjon']} "
                      f"til {ticket['TilStasjon']} avgang {ticket['Dato']} kjøpt {ticket['KjopDato']} kl. {ticket['KjopTidspunkt']}")

        elif cmd == "hjelp":
            print("Kommandoer:")
            print("reset - Resetter databasen")
            print("kunder - Viser alle kunder")
            print("ny kunde - Legger til en ny kunde")
            print("kjøp billett - Kjøper en billett")
            print("finn ruter - Viser alle ruter på en gitt dag fra en gitt stasjon")
            print("finn reise - Viser alle reiser mellom to stasjoner på en gitt dag")
        elif cmd == "exit":
            break
        else:
            print("Ukjent kommando, skriv hjelp for hjelp")
