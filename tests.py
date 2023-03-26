from datetime import datetime, timedelta

from utils import hms_to_seconds
import unittest

from database import TogDatabase


class TaskTests(unittest.TestCase):
    def setUp(self) -> None:
        self.db = TogDatabase(":memory:")
        self.db.reset_database()

    def test_c_station_routes_list(self):
        """
        c) For en stasjon som oppgis, skal bruker få ut alle togruter som er
        innom stasjonenen gitt ukedag. Denne funksjonaliteten skal programmeres.
        """

        station = "Trondheim"
        for day in ("mandag", "tirsdag", "onsdag", "torsdag", "fredag", "lørdag", "søndag"):
            print(f"=== Ruter innom {station} på {day}er ===")
            routes = [route["TogruteID"] for route in self.db.list_routes_by_day_and_station(day, station)]
            if len(routes) == 0:
                print("Ingen ruter")
            elif len(routes) == 1:
                print("Rute", routes[0])
            else:
                print("Rute", ", ".join(map(str, routes[:-1])), "og", routes[-1])

    def test_d_find_trip(self):
        """
        d) Bruker skal kunne søke etter togruter som går mellom en startstasjon og en sluttstasjon, med
        utgangspunkt i en dato og et klokkeslett. Alle ruter den samme dagen og den neste skal
        returneres, sortert på tid. Denne funksjonaliteten skal programmeres.
        """

        for date in ("2023-04-03", "2023-04-04", "2023-04-05", "2023-04-06", "2023-04-07"):
            start_station = "Trondheim"
            end_station = "Steinkjer"
            time = "12:00"

            trips = self.db.find_trips(start_station, end_station, date, time)
            print(f"====== Ruter mellom {start_station} og {end_station} =======")
            for trip in trips:
                print(f"Rute {trip['TogruteID']}, drar fra {trip['StartNavn']} {trip['Ukedag']} kl. {trip['Avgang']} "
                      f"og ankommer {trip['StoppNavn']} kl. {trip['Ankomst']}")

                self.assertTrue(trip["StartNavn"] == start_station)
                self.assertTrue(trip["StoppNavn"] == end_station)
            print("=========================================================")

    def test_e_create_customer_account(self):
        """
        e) En bruker skal kunne registrere seg i kunderegisteret. Denne funksjonaliteten skal programmeres.
        """

        customer_id = self.db.add_customer("Customer", "customer@customer.com", "999 99 999")
        self.assertEqual(self.db.list_customers(), [
            {"Navn": "Customer", "Epost": "customer@customer.com", "TlfNr": "999 99 999", "KundeNr": 1}
        ])

        print(f"Registrerte kunde med ID {customer_id}")

    def test_g_purchase_ticket(self):
        """
        g) Registrerte kunder skal kunne finne ledige billetter for en oppgitt strekning på en ønsket togrute
        og kjøpe de billettene hen ønsker. Denne funksjonaliteten skal programmeres.
        """

        from_station, to_station = "Trondheim", "Steinkjer"
        date, time = "2023-04-03", "12:00"

        customer_id = self.db.add_customer("Other Customer", "other@customer.com", "999 99 999")
        print(f"Registrerte kunde med ID {customer_id}")

        trips = self.db.find_trips(from_station, to_station, date, time)
        trip = trips[0]

        print(f"Fant {len(trips)} ruter og valgte rute #{trip['TogruteID']}")
        tickets = self.db.find_tickets(trip["TogruteID"], date)
        ticket = tickets[0]
        print(f"Fant {len(tickets)} billetter og valgte plass {ticket['PlassNr']} i vogn {ticket['VognNr']}")

        order_id = self.db.purchase_ticket(
            trip["TogruteID"], date, ticket["VognNr"], ticket["PlassNr"], customer_id, from_station, to_station
        )
        print(f"Kjøpte billett med ordrenummer {order_id}")

    def test_h_find_purchases(self):
        """
        h) For en bruker skal man kunne finne all informasjon om de kjøpene hen har gjort for fremtidige
        reiser. Denne funksjonaliteten skal programmeres.
        """

        customer_id = self.db.add_customer("Third Customer", "third@customer.com", "999 99 999")
        print(f"Registrerte kunde med ID {customer_id}")

        from_station, to_station = "Trondheim", "Steinkjer"
        date, time = "2023-04-03", "12:00"

        trips = self.db.find_trips(from_station, to_station, date, time)
        trip = trips[0]

        print(f"Fant {len(trips)} ruter og valgte rute #{trip['TogruteID']}")

        order_ids = []
        for date in ("2023-04-03", "2023-04-04"):
            tickets = self.db.find_tickets(trip["TogruteID"], date)
            ticket = tickets[0]
            print(f"Fant {len(tickets)} billetter og valgte plass {ticket['PlassNr']} i vogn {ticket['VognNr']}")

            order_ids.append(self.db.purchase_ticket(
                trip["TogruteID"], date, ticket["VognNr"], ticket["PlassNr"], customer_id, from_station, to_station
            ))

        print("Fant følgende billetter:")
        last_order_id = None
        purchases = self.db.find_future_purchases_by_customer(customer_id)
        for purchase in purchases:
            if purchase["OrdreNr"] != last_order_id:
                last_order_id = purchase["OrdreNr"]
                print(f"Bestilling #{purchase['OrdreNr']} kjøpt {purchase['KjopDato']} kl. {purchase['KjopTidspunkt']}")

            print(f"\tBillett fra {purchase['FraStasjon']} til {purchase['TilStasjon']} på rute #{purchase['TogruteID']} {purchase['Dato']}")

            self.assertTrue(purchase["KundeNr"] == customer_id)


if __name__ == '__main__':
    unittest.main()
