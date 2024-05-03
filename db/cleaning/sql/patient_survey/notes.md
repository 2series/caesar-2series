## SQLite Db

1. duplicate table HCAPHS
CREATE TABLE
    `HCAHPS-copy` (
        `Facility ID` INTEGER,
        `Facility Name` TEXT,
        `Address` BLOB,
        `City/Town` TEXT,
        `State` TEXT,
        `ZIP Code` INTEGER,
        `County/Parish` TEXT,
        `Telephone Number` BLOB,
        `HCAHPS Measure ID` BLOB,
        `HCAHPS Question` BLOB,
        `HCAHPS Answer Description` BLOB,
        `HCAHPS Answer Percent` REAL,
        `Number of Completed Surveys` INTEGER,
        `Survey Response Rate Percent` REAL,
        `Start Date` date,
        `End Date` date
    );

INSERT INTO
    `HCAHPS-copy`
SELECT
    *
FROM
    `HCAHPS`;


1. duplicate table hospital_beds
CREATE TABLE
    `hospital_beds-copy` (
        `Provider CCN` INTEGER,
        `Hospital Name` BLOB,
        `Fiscal Year Begin Date` date,
        `Fiscal Year End Date` date,
        `number_of_beds` INTEGER
    );

INSERT INTO
    `hospital_beds-copy`
SELECT
    *
FROM
    `hospital_beds`;

-- standardize col "Provider CCN" to 6 characters hospital_beds
SELECT
    CASE LENGTH(CAST(`Provider CCN` as TEXT))
        WHEN 5 THEN '0' || CAST(`Provider CCN` as TEXT)
        ELSE LTRIM(
            substr(
                '000000',
                1,
                6 - LENGTH(CAST(`Provider CCN` as TEXT))
            ) || CAST(`Provider CCN` as TEXT),
            '0'
        )
    END AS `Provider CCN`,
    `Hospital Name`,
    `Fiscal Year Begin Date`,
    `Fiscal Year End Date`,
    `number_of_beds`
FROM
    `hospital_beds-copy`;

-- update col "Provider CCN" in table "hospital_beds-copy"
UPDATE `hospital_beds-copy`
SET
    `Provider CCN` = CASE
        WHEN LENGTH(CAST(`Provider CCN` as TEXT)) = 5 THEN '0' || CAST(`Provider CCN` as TEXT)
        ELSE LTRIM(
            substr(
                '000000',
                1,
                6 - LENGTH(CAST(`Provider CCN` as TEXT))
            ) || CAST(`Provider CCN` as TEXT),
            '0'
        )
    END;





continue
https://youtu.be/6YwwHfxAfZI


