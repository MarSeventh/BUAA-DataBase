-- Active: 1698489563240@@127.0.0.1@3306@buaa_db_demo
-- Date: 2021-06-27 16:52:43
-- Type: SQL

CREATE TABLE IF NOT EXISTS `Patient` (
    `id` VarCHAR(25) NOT NULL,
    `name` VarCHAR(25) NOT NULL,
    `isComMem` BOOLEAN NOT NULL,
    `password` VarCHAR(25) NOT NULL,
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
    `name` VarCHAR(25) NOT NULL,
    `password` VarCHAR(25) NOT NULL,
    `TitleId` VarCHAR(25) NOT NULL,
    `active` BOOLEAN NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF  NOT EXISTS `Admin` (
    `id` VARCHAR(25) NOT NULL,
    `password` VARCHAR(25) NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `Drug`(
    `id` VARCHAR(25) NOT NULL,
    `name` VARCHAR(25) NOT NULL,
    `price` FLOAT NOT NULL,
    `Description` TEXT NOT NULL,
    `islegal` BOOLEAN NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `Storage` (
    `id` VARCHAR(25) NOT NULL,
    `amount` DOUBLE NOT NULL,
    FOREIGN KEY (`id`) REFERENCES `Drug`(`id`) ON DELETE CASCADE;
);

CREATE TABLE IF NOT EXISTS `Counter` (
    `id` VARCHAR(25) NOT NULL,
    `Pid` VARCHAR(25) NOT NULL,
    `Did` VARCHAR(25) NOT NULL,
    `isPaid` BOOLEAN NOT NULL,
    `price` FLOAT NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `RegistRelation` (
    `id` VARCHAR(25) NOT NULL,
    `patientId` VARCHAR(25) NOT NULL,
    `doctorId` VARCHAR(25) NOT NULL,
    `ROOMID` VARCHAR(25) NOT NULL,
    FOREIGN KEY (`patientId`) REFERENCES `Patient`(`id`),
    FOREIGN KEY (`doctorId`) REFERENCES `Doctor`(`id`),
    FOREIGN KEY (`id`) REFERENCES `Counter`(`id`),
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `MedicinePurchase` (
    `id` VARCHAR(25) NOT NULL,
    `patientid` VARCHAR(25) NOT NULL,
    `drugId` VARCHAR(25) NOT NULL,
    `amount` FLOAT NOT NULL,
    `time` DATETIME NOT NULL,
    FOREIGN KEY (`patientId`) REFERENCES `Patient`(`id`),
    FOREIGN KEY (`drugId`) REFERENCES `Drug`(`id`),
    Foreign Key (`id`) REFERENCES `Counter`(`id`),
    PRIMARY KEY (`id`)
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
    `patientId` VARCHAR(25) NOT NULL,
    `doctorId` VARCHAR(25) NOT NULL,
    `checkName` VARCHAR(255) NOT NULL,
    `beginTime` DATETIME NOT NULL,
    `OutputTime` DATETIME,
    `itemID` VARCHAR(25) NOT NULL,
    `result` VARCHAR(255) NOT NULL,
    FOREIGN KEY (`patientId`) REFERENCES `Patient`(`id`),
    FOREIGN KEY (`doctorId`) REFERENCES `Doctor`(`id`),
    FOREIGN KEY (`itemID`) REFERENCES `checkItems`(`id`),
    PRIMARY KEY (`id`, `checkName`)
);

CREATE TABLE IF NOT EXISTS `ROOM` (
    `id` VARCHAR(25) NOT NULL,
    `isOccupied` BOOLEAN NOT NULL,
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

