SELECT
    TogrutePåDag.TogruteID,
    Togrute.OperatørNavn,
    Togrute.MedHovedretning
FROM TogrutePåDag
INNER JOIN
    Togrute USING (TogruteID)
WHERE
    Ukedag = $1 AND
    TogruteID IN (
        SELECT TogruteID
        FROM Rutestopp
        WHERE StasjonNavn = $2
    );