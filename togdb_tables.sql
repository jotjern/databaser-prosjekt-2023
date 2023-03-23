CREATE TABLE Banestrekning(
    Navn TEXT PRIMARY KEY,
    Fremdriftsenergi TEXT
);

CREATE TABLE Jernbanestasjon(
    Navn TEXT PRIMARY KEY,
    MoH REAL,
    BaneNavn TEXT NOT NULL,
    StoppNr INTEGER,
    FOREIGN KEY (BaneNavn) REFERENCES Banestrekning (Navn)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Delstrekning(
    FraStasjon TEXT NOT NULL,
    TilStasjon TEXT NOT NULL,
    Lengde INTEGER,
    HarDobbeltspor INTEGER,
    PRIMARY KEY (FraStasjon, TilStasjon),
    FOREIGN KEY (FraStasjon) REFERENCES Jernbanestasjon (Navn)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (TilStasjon) REFERENCES Jernbanestasjon (Navn)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Operatør(
    Navn TEXT PRIMARY KEY
);

CREATE TABLE Togrute(
    TogruteID INTEGER PRIMARY KEY,
    MedHovedretning INTEGER,
    OperatørNavn TEXT NOT NULL,
    FOREIGN KEY (OperatørNavn) REFERENCES Operatør (Navn)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE TogrutePåDag(
    TogruteID INTEGER NOT NULL,
    Ukedag TEXT NOT NULL,
    PRIMARY KEY (TogruteID, Ukedag),
    FOREIGN KEY (TogruteID) REFERENCES Togrute (TogruteID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Rutestopp(
    TogruteID INTEGER NOT NULL,
    StasjonNavn TEXT NOT NULL,
    Tidspunkt TEXT,
    StoppNr INTEGER,
    PRIMARY KEY (TogruteID, StasjonNavn),
    FOREIGN KEY (TogruteID) REFERENCES Togrute (TogruteID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (StasjonNavn) REFERENCES Jernbanestasjon (Navn)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Vogn (
    VognNavn TEXT PRIMARY KEY,
    OperatørNavn TEXT NOT NULL,
    FOREIGN KEY (OperatørNavn) REFERENCES Operatør (Navn)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Sittevogn (
    VognNavn TEXT PRIMARY KEY,
    AntallRader INTEGER,
    SeterPerRad INTEGER,
    FOREIGN KEY (VognNavn) REFERENCES Vogn (VognNavn)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);


CREATE TABLE Sovevogn(
    VognNavn TEXT PRIMARY KEY,
    AntallKupéer INTEGER,
    SengerPerKupé INTEGER,
    FOREIGN KEY (VognNavn) REFERENCES Vogn (VognNavn)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);


CREATE TABLE VognPåRute(
    TogruteID INTEGER NOT NULL,
    VognNavn TEXT NOT NULL,
    VognNr INTEGER,
    PRIMARY KEY (TogruteID, VognNr),
    FOREIGN KEY (TogruteID) REFERENCES Togrute (TogruteID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (VognNavn) REFERENCES Vogn (VognNavn)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE PassasjerPlass(
    VognNavn TEXT NOT NULL,
    PlassNr INTEGER NOT NULL,
    PRIMARY KEY (VognNavn, PlassNr)
);

CREATE TABLE Seng(
    VognNavn TEXT NOT NULL,
    PlassNr INTEGER NOT NULL,
    PRIMARY KEY (VognNavn, PlassNr),
    FOREIGN KEY (VognNavn) REFERENCES Sovevogn (VognNavn)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (VognNavn, PlassNr) REFERENCES PassasjerPlass (VognNavn, PlassNr)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);


CREATE TABLE Sete(
    VognNavn TEXT NOT NULL,
    PlassNr INTEGER NOT NULL,
    PRIMARY KEY (VognNavn, PlassNr),
    FOREIGN KEY (VognNavn) REFERENCES Sittevogn (VognNavn)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (VognNavn, PlassNr) REFERENCES PassasjerPlass (VognNavn, PlassNr)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Togruteforekomst(
    TogruteID INTEGER NOT NULL,
    Dato TEXT NOT NULL,
    PRIMARY KEY (TogruteID, Dato),
    FOREIGN KEY (TogruteID) REFERENCES Togrute (TogruteID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Kunde(
    KundeNr INTEGER PRIMARY KEY,
    Navn TEXT,
    Epost TEXT,
    TlfNr TEXT
);

CREATE TABLE KundeOrdre(
    OrdreNr INTEGER PRIMARY KEY,
    Dato TEXT,
    Tidspunkt TEXT,
    KundeNr INTEGER NOT NULL,
    FOREIGN KEY (KundeNr) REFERENCES Kunde (KundeNr)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE Billett(
    TogruteID INTEGER NOT NULL,
    Dato TEXT NOT NULL,
    VognNavn TEXT NOT NULL,
    PlassNr INTEGER NOT NULL,
    FraStasjon TEXT NOT NULL,
    TilStasjon TEXT NOT NULL,
    OrdreNr INTEGER NOT NULL,
    PRIMARY KEY (TogruteID, Dato, VognNavn, PlassNr, FraStasjon, TilStasjon),
    FOREIGN KEY (TogruteID, Dato) REFERENCES Togruteforekomst (TogruteID, Dato)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (VognNavn, PlassNr) REFERENCES PassasjerPlass (VognNavn, PlassNr)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (FraStasjon) REFERENCES Jernbanestasjon (Navn)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (TilStasjon) REFERENCES Jernbanestasjon (Navn)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (OrdreNr) REFERENCES KundeOrdre (OrdreNr)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);