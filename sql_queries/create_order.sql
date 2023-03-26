INSERT INTO KundeOrdre
    (KjopDato, KjopTidspunkt, KundeNr)
VALUES
    (?, ?, ?)
RETURNING OrdreNr;