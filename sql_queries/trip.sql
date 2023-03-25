SELECT 
    TogrutePåDag.TogruteID,
    StartStasjon.StasjonNavn AS StartNavn,
    StoppStasjon.StasjonNavn AS StoppNavn,
    StartStasjon.Tidspunkt AS Tid
FROM (TogrutePåDag
    INNER JOIN Rutestopp AS StartStasjon ON (TogrutePåDag.TogruteID = StartStasjon.TogruteID))
    INNER JOIN Rutestopp AS StoppStasjon ON (TogrutePåDag.TogruteID = StoppStasjon.TogruteID)
WHERE
   (((Ukedag = $1) AND (StartStasjon.StoppNr < StoppStasjon.StoppNr))
   AND (StartStasjon.StasjonNavn = $2)) AND (StoppStasjon.StasjonNavn = $3)
ORDER BY Tid ASC;