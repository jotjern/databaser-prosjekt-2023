SELECT
    VognPåRute.VognNavn, VognPåRute.VognNr, count(*) AS LedigePlasser, PassasjerPlass.Type
FROM
    VognPåRute
CROSS JOIN
    PassasjerPlass
LEFT JOIN Billett ON
(
    Billett.TogruteID = VognPåRute.TogruteID
    AND Billett.PlassNr = PassasjerPlass.PlassNr
    AND Billett.Dato = ?2
    AND Billett.VognNr = VognPåRute.VognNr
)
WHERE
    PassasjerPlass.VognNavn = VognPåRute.VognNavn AND
    VognPåRute.TogruteID = ?1 AND
    ?2 IN (SELECT Dato FROM Togruteforekomst WHERE TogruteID = ?1) AND
    OrdreNr IS NULL
GROUP BY
    VognPåRute.VognNr, PassasjerPlass.Type