SELECT * FROM Billett
INNER JOIN KundeOrdre USING (OrdreNr)
ORDER BY OrdreNr;