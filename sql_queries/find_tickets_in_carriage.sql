SELECT
    Billett.OrdreNr AS OrdreNr,
    ?2 AS Dato,
    VognPåRute.VognNavn AS VognNavn,
    VognPåRute.VognNr AS VognNr,
    PassasjerPlass.PlassNr AS PlassNr,
    PassasjerPlass.Type AS PlassType
FROM VognPåRute
CROSS JOIN PassasjerPlass
LEFT OUTER JOIN Billett ON
(
    Billett.TogruteID = VognPåRute.TogruteID
    AND Billett.PlassNr = PassasjerPlass.PlassNr
    AND Billett.Dato = ?2
    AND Billett.VognNr = VognPåRute.VognNr
)
WHERE PassasjerPlass.VognNavn = VognPåRute.VognNavn
AND VognPåRute.TogruteID = ?1
AND ?2 IN (SELECT Dato FROM Togruteforekomst WHERE TogruteID = ?1)
AND OrdreNr IS NULL
AND VognPåRute.VognNr = ?3