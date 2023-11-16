-- Active: 1698489563240@@127.0.0.1@3306@buaa_db_demo
-- Date: 2021-06-27 16:52:43
-- Type: SQL

DROP TABLE IF EXISTS `Patient`;
DROP TABLE IF EXISTS `Doctor`;
DROP TABLE IF EXISTS `Admin`;
DROP TABLE IF EXISTS `Drug`;
DROP TABLE IF EXISTS `Storage`;
DROP TABLE IF EXISTS `Counter`;

DROP TABLE IF EXISTS `RegistRelation`;
DROP TABLE IF EXISTS `ROOM`;
DROP TABLE IF EXISTS `Dispatcher`;
DROP TABLE IF EXISTS `diagnosis`;
DROP TABLE IF EXISTS `CheckCombine`;
DROP TABLE IF EXISTS `checkItems`;
DROP TABLE IF EXISTS `LaboratorySheet`;
DROP TABLE IF EXISTS `MedicinePurchase`;
DROP TABLE IF EXISTS `Titles`;

CREATE TABLE IF NOT EXISTS `USER` (
    `id` VarChar(25) NOT NULL,
    `USERNAME` VARCHAR(25) NOT NULL,
    `password` VARCHAR(25) NOT NULL,
    `type` VARCHAR(25) NOT NULL,
    PRIMARY KEY(`id`)
);

CREATE TABLE IF NOT EXISTS `Patient` (
    `id` VarCHAR(25) NOT NULL,
    `isComMem` BOOLEAN NOT NULL,
    `idCard` VarCHAR(25),
    `active` BOOLEAN NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `Titles` (
    `id` VARCHAR(25) NOT NULL,
    `name` VARCHAR(25) NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `Doctor` (
    `id` VarCHAR(25) NOT NULL,
    `Tid` VarCHAR(25) NOT NULL,
    `active` BOOLEAN NOT NULL,
    FOREIGN KEY (`Tid`) REFERENCES `Titles`(`id`),
    PRIMARY KEY (`id`)
);

CREATE TABLE IF  NOT EXISTS `Admin` (
    `id` VARCHAR(25) NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `Drug`(
    `id` VARCHAR(25) NOT NULL,
    `name` VARCHAR(25) NOT NULL,
    `price` FLOAT NOT NULL,
    `Description` TEXT NOT NULL,
    `isBanned` BOOLEAN NOT NULL,
    `Storage` FLOAT NOT NULL,
    PRIMARY KEY (`id`)
);

ALTER TABLE `Drug` RENAME COLUMN `amount` TO `Storage`

CREATE TABLE IF NOT EXISTS `Counter` (
    `id` VARCHAR(25) NOT NULL,
    `Pid` VARCHAR(25) NOT NULL,
    `Did` VARCHAR(25) NOT NULL,
    `isPaid` BOOLEAN NOT NULL,
    `price` FLOAT,
    `type` VARCHAR(25) NOT NULL,
    FOREIGN KEY (`Did`) REFERENCES `Doctor`(`id`),
    FOREIGN KEY (`Pid`) REFERENCES `Patient`(`id`),
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `RegistRelation` (
    `id` VARCHAR(25) NOT NULL,
    `ROOMID` VARCHAR(25) NOT NULL,
    FOREIGN KEY (`id`) REFERENCES `Counter`(`id`),
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `MedicinePurchase` (
    `id` VARCHAR(25) NOT NULL,
    `drugId` VARCHAR(25) NOT NULL,
    `amount` FLOAT NOT NULL,
    `time` DATETIME NOT NULL,
    FOREIGN KEY (`drugId`) REFERENCES `Drug`(`id`),
    Foreign Key (`id`) REFERENCES `Counter`(`id`),
    PRIMARY KEY (`id`, `drugId`)
);

CREATE TABLE IF NOT EXISTS `checkItems` (
    `id` VARCHAR(25) NOT NULL,
    `price` FLOAT NOT NULL,
    `description` VARCHAR(255) NOT NULL,
    `MinResult` FLOAT NOT NULL,
    `MaxResult` FLOAT NOT NULL,
    PRIMARY KEY (`id`)
);
CREATE TABLE IF NOT EXISTS `LaboratorySheet`(
    `id` VARCHAR(25) NOT NULL,
    `checkName` VARCHAR(255) NOT NULL,
    `beginTime` DATETIME NOT NULL,
    `OutputTime` DATETIME,
    `itemID` VARCHAR(25) NOT NULL,
    `result` VARCHAR(255) NOT NULL,
    FOREIGN KEY (`itemID`) REFERENCES `checkItems`(`id`),
    FOREIGN KEY (`id`) REFERENCES `Counter`(`id`),
    PRIMARY KEY (`id`, `itemID`)
);

CREATE TABLE IF NOT EXISTS `ROOM` (
    `id` VARCHAR(25) NOT NULL,
    `isOccupied` BOOLEAN NOT NULL,
    `QueueLen` int NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `Dispatcher` (
    `TimePeriod` VARCHAR(25) NOT NULL,
    `ROOMID` VARCHAR(25) NOT NULL,
    `doctorId` VARCHAR(25) ,
    `TitleId` VARCHAR(25),
    PRIMARY KEY (`TimePeriod`, `ROOMID`),
    FOREIGN KEY (`doctorId`) REFERENCES `Doctor`(`id`),
    FOREIGN KEY (`ROOMID`) REFERENCES `Room`(`id`)
);

CREATE TABLE IF NOT EXISTS `diagnosis`(
    `id` VARCHAR(25) NOT NULL,
    `patientId` VARCHAR(25) NOT NULL,
    `doctorId` VARCHAR(25) NOT NULL,
    `diagnosis` TEXT NOT NULL,
    `time` DATETIME NOT NULL,
    FOREIGN KEY (`patientId`) REFERENCES `Patient`(`id`),
    FOREIGN KEY (`doctorId`) REFERENCES `Doctor`(`id`),
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `CheckCombine`(
    `id` VARCHAR(25) NOT NULL,
    `itemId` VARCHAR(25) NOT NULL,
    `checkName` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`itemId`) REFERENCES `checkItems`(`id`)
);

SELECT * FROM `Patient`;