SELECT
    TogrutePåDag.TogruteID,
    Togrute.OperatørNavn,
    Togrute.MedHovedretning,
    Rutestopp.Tidspunkt
FROM TogrutePåDag
INNER JOIN
    Togrute USING (TogruteID)
INNER JOIN Rutestopp
    ON Togrute.TogruteID = Rutestopp.TogruteID AND
       Rutestopp.StasjonNavn = ?2
WHERE
    Ukedag = ?1 AND
    Togrute.TogruteID IN (
        SELECT TogruteID
        FROM Rutestopp
        WHERE StasjonNavn = ?2
    );