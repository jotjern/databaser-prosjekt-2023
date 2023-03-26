SELECT
    TogruteID, Dato, PlassNr, VognNr, FraStasjon,  TilStasjon, OrdreNr, KjopDato, KjopTidspunkt, Kundenr
FROM Billett
INNER JOIN KundeOrdre USING (OrdreNr)
WHERE KundeNr = ?1
