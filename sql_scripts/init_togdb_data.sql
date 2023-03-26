INSERT INTO Banestrekning (Navn, Fremdriftsenergi) VALUES
    ('Nordlandsbanen', 'Diesel');

INSERT INTO Jernbanestasjon (Navn, MoH, BaneNavn, StoppNr) VALUES
    ('Trondheim', 5.1, 'Nordlandsbanen', 1),
    ('Steinkjer', 3.6, 'Nordlandsbanen', 2),
    ('Mosjøen', 6.8, 'Nordlandsbanen', 3),
    ('Mo i Rana', 3.5, 'Nordlandsbanen', 4),
    ('Fauske', 34.0, 'Nordlandsbanen', 5),
    ('Bodø', 4.1, 'Nordlandsbanen', 6);

INSERT INTO Delstrekning (FraStasjon, TilStasjon, Lengde, HarDobbeltspor) VALUES
    ('Trondheim', 'Steinkjer', 120, true),
    ('Steinkjer', 'Mosjøen', 280, false),
    ('Mosjøen', 'Mo i Rana', 90, false),
    ('Mo i Rana', 'Fauske', 170, false),
    ('Fauske', 'Bodø', 60, false);

INSERT INTO Operatør (Navn) VALUES
    ('SJ');

INSERT INTO Togrute (TogruteID, MedHovedretning, OperatørNavn) VALUES
    (0, true, 'SJ'),
    (1, true, 'SJ'),
    (2, false, 'SJ');

INSERT INTO Rutestopp (TogruteID, StasjonNavn, Tidspunkt, StoppNr) VALUES
    (0, 'Trondheim', '07:49', 1),
    (0, 'Steinkjer', '09:51', 2),
    (0, 'Mosjøen', '13:20', 3),
    (0, 'Mo i Rana', '14:31', 4),
    (0, 'Fauske', '16:49', 5),
    (0, 'Bodø', '17:34', 6),

    (1, 'Trondheim', '23:05', 1),
    (1, 'Steinkjer', '00:57', 2),
    (1, 'Mosjøen', '04:41', 3),
    (1, 'Mo i Rana', '05:55', 4),
    (1, 'Fauske', '08:19', 5),
    (1, 'Bodø', '09:05', 5),

    (2, 'Mo i Rana', '08:11', 1),
    (2, 'Mosjøen', '09:14', 2),
    (2, 'Steinkjer', '12:31', 3),
    (2, 'Trondheim', '14:13', 4);

INSERT INTO TogrutePåDag (TogruteID, Ukedag) VALUES
    (0, 'mandag'),
    (0, 'tirsdag'),
    (0, 'onsdag'),
    (0, 'torsdag'),
    (0, 'fredag'),

    (1, 'mandag'),
    (1, 'tirsdag'),
    (1, 'onsdag'),
    (1, 'torsdag'),
    (1, 'fredag'),
    (1, 'lørdag'),
    (1, 'søndag'),

    (2, 'mandag'),
    (2, 'tirsdag'),
    (2, 'onsdag'),
    (2, 'torsdag'),
    (2, 'fredag');

INSERT INTO Vogn (VognNavn, OperatørNavn) VALUES
    ('SJ-sittevogn-1', 'SJ'),
    ('SJ-sovevogn-1', 'SJ');

INSERT INTO VognPåRute (TogruteID, VognNavn, VognNr) VALUES
    (0, 'SJ-sittevogn-1',  1),
    (0, 'SJ-sittevogn-1',  2),

    (1, 'SJ-sittevogn-1',  1),
    (1, 'SJ-sovevogn-1',  2),

    (2, 'SJ-sittevogn-1',  1);

INSERT INTO PassasjerPlass (VognNavn, PlassNr, Type, Inndeling) VALUES
    ('SJ-sittevogn-1', 1, 'Sete', 1),
    ('SJ-sittevogn-1', 2, 'Sete', 1),
    ('SJ-sittevogn-1', 3, 'Sete', 1),
    ('SJ-sittevogn-1', 4, 'Sete', 1),
    ('SJ-sittevogn-1', 5, 'Sete', 2),
    ('SJ-sittevogn-1', 6, 'Sete', 2),
    ('SJ-sittevogn-1', 7, 'Sete', 2),
    ('SJ-sittevogn-1', 8, 'Sete', 2),
    ('SJ-sittevogn-1', 9, 'Sete', 3),
    ('SJ-sittevogn-1', 10, 'Sete', 3),
    ('SJ-sittevogn-1', 11, 'Sete', 3),
    ('SJ-sittevogn-1', 12, 'Sete', 3),
    ('SJ-sovevogn-1', 1, 'Seng', 1),
    ('SJ-sovevogn-1', 2, 'Seng', 1),
    ('SJ-sovevogn-1', 3, 'Seng', 2),
    ('SJ-sovevogn-1', 4, 'Seng', 2),
    ('SJ-sovevogn-1', 5, 'Seng', 3),
    ('SJ-sovevogn-1', 6, 'Seng', 3),
    ('SJ-sovevogn-1', 7, 'Seng', 4),
    ('SJ-sovevogn-1', 8, 'Seng', 4);