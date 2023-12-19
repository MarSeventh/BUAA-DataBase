-- Active: 1698572182490@@120.46.80.149@3306@db21373405
-- Date: 2021-06-27 16:52:43
-- Type: SQL

DROP TABLE IF EXISTS `Patient`;
DROP TABLE IF EXISTS `Doctor`;
DROP TABLE IF EXISTS `Admin`;
DROP TABLE IF EXISTS `Drug`;
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
    `password` VARCHAR(50) NOT NULL,
    `type` VARCHAR(25) NOT NULL,
    `AVATAR` VARCHAR(50),
    PRIMARY KEY(`id`)
);

ALTER TABLE `USER` MODIFY COLUMN `password` VARCHAR(50) NOT NULL;
CREATE INDEX `index_id` ON `USER` (`id`)

CREATE TABLE IF NOT EXISTS `Patient` (
    `id` VarCHAR(25) NOT NULL,
    `isComMem` BOOLEAN NOT NULL,
    `idCard` VarCHAR(25),
    `active` BOOLEAN NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE INDEX `index_id` ON `Patient` (`id`)

CREATE TABLE IF NOT EXISTS `Titles` (
    `id` VARCHAR(25) NOT NULL,
    `name` VARCHAR(25) NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE INDEX `index_id` ON `Titles` (`id`)

CREATE TABLE IF NOT EXISTS `Doctor` (
    `id` VarCHAR(25) NOT NULL,
    `Tid` VarCHAR(25) NOT NULL,
    `active` BOOLEAN NOT NULL,
    FOREIGN KEY (`Tid`) REFERENCES `Titles`(`id`),
    PRIMARY KEY (`id`)
);

CREATE INDEX `index_id` ON `Doctor` (`id`)

CREATE TABLE IF NOT EXISTS `Drug`(
    `id` VARCHAR(25) NOT NULL,
    `price` FLOAT NOT NULL,
    `Description` TEXT NOT NULL,
    `isBanned` BOOLEAN NOT NULL,
    `Storage` FLOAT NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE INDEX `index_id` ON `Drug` (`id`)

CREATE TABLE IF NOT EXISTS `Counter` (
    `id` VARCHAR(25) NOT NULL,
    `Pid` VARCHAR(25) NOT NULL,
    `Did` VARCHAR(25) NOT NULL,
    `isPaid` BOOLEAN NOT NULL,
    `price` FLOAT,
    `DATE` DATE NOT NULL,
    `type` VARCHAR(25) NOT NULL,
    FOREIGN KEY (`Did`) REFERENCES `Doctor`(`id`),
    FOREIGN KEY (`Pid`) REFERENCES `Patient`(`id`),
    PRIMARY KEY (`id`)
);

CREATE INDEX `index_id` ON `Counter` (`id`)

CREATE TABLE IF NOT EXISTS `RegistRelation` (
    `id` VARCHAR(25) NOT NULL,
    `ROOMID` VARCHAR(25) NOT NULL,
    `isFinished` BOOLEAN NOT NULL,
    FOREIGN KEY (`id`) REFERENCES `Counter`(`id`),
    PRIMARY KEY (`id`)
);

CREATE INDEX `index_id` ON `RegistRelation` (`id`)

CREATE TABLE IF NOT EXISTS `MedicinePurchase` (
    `id` VARCHAR(25) NOT NULL,
    `drugId` VARCHAR(25) NOT NULL,
    `amount` FLOAT NOT NULL,
    FOREIGN KEY (`drugId`) REFERENCES `Drug`(`id`),
    Foreign Key (`id`) REFERENCES `Counter`(`id`),
    PRIMARY KEY (`id`, `drugId`)
);

CREATE INDEX `index_id` ON `MedicinePurchase` (`id`)


CREATE TABLE IF NOT EXISTS `checkItems` (
    `id` VARCHAR(25) NOT NULL,
    `price` FLOAT NOT NULL,
    `description` VARCHAR(255) NOT NULL,
    `MinResult` FLOAT NOT NULL,
    `MaxResult` FLOAT NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE INDEX `index_id` ON `checkItems` (`id`)

CREATE TABLE IF NOT EXISTS `LaboratorySheet`(
    `id` VARCHAR(25) NOT NULL,
    `checkName` VARCHAR(255) NOT NULL,
    `beginTime` DATETIME NOT NULL,
    `OutputTime` DATETIME,
    `itemID` VARCHAR(25) NOT NULL,
    `result` FLOAT NOT NULL,
    FOREIGN KEY (`itemID`) REFERENCES `checkItems`(`id`),
    FOREIGN KEY (`id`) REFERENCES `Counter`(`id`),
    PRIMARY KEY (`id`, `itemID`)
);

CREATE INDEX `index_id` ON `LaboratorySheet` (`id`)

CREATE TABLE IF NOT EXISTS `ROOM` (
    `id` VARCHAR(25) NOT NULL,
    `isOccupied` BOOLEAN NOT NULL,
    `QueueLen` int NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE INDEX `index_id` ON `ROOM` (`id`)

CREATE TABLE IF NOT EXISTS `Dispatcher` (
    `TimePeriod` VARCHAR(25) NOT NULL,
    `ROOMID` VARCHAR(25) NOT NULL,
    `doctorId` VARCHAR(25) ,
    `TitleId` VARCHAR(25),
    `DATE` VARCHAR(15) NOT NULL,
    PRIMARY KEY (`TimePeriod`, `ROOMID`, `DATE`),
    FOREIGN KEY (`doctorId`) REFERENCES `Doctor`(`id`),
    FOREIGN KEY (`ROOMID`) REFERENCES `Room`(`id`)
);

CREATE INDEX `index_TimePeriod` ON `Dispatcher` (`TimePeriod`)

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

CREATE INDEX `index_id` ON `diagnosis` (`id`)

CREATE TABLE IF NOT EXISTS `CheckCombine`(
    `id` VARCHAR(25) NOT NULL,
    `itemId` VARCHAR(25) NOT NULL,
    `checkName` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`id`, `itemId`),
    FOREIGN KEY (`itemId`) REFERENCES `checkItems`(`id`)
);

CREATE INDEX `index_id` ON `CheckCombine` (`id`)



SELECT * FROM checkcombine;

-----下面是数据库的初始化，填入一些必要的数据

INSERT INTO `Titles` (`id`, `name`) VALUES ('1', '全科');
INSERT INTO `Titles` (`id`, `name`) VALUES ('2', '内科');

INSERT INTO `Titles` (`id`, `name`) VALUES ('3', '外科');

INSERT INTO `Titles` (`id`, `name`) VALUES ('4', '眼科');

INSERT INTO `USER` (`id`, `USERNAME`, `password`, `type`) VALUES ('1', 'admin', 'buaadb', 'admin');

INSERT INTO `USER` (`id`, `USERNAME`, `PASSWORD`, `type`) VALUES ('2', 'John', '123456', 'doctor')

INSERT INTO `DOCTOR` (`id`, `tid`, `active`) VALUES ('2', '1', 1)

INSERT INTO `USER` (`id`, `USERNAME`, `PASSWORD`, `type`) VALUES ('3', '张三', '123456', 'doctor')


INSERT INTO `DOCTOR` (`id`, `tid`, `active`) VALUES ('3', '1', 1)


INSERT INTO `USER` (`id`, `USERNAME`, `PASSWORD`, `type`) VALUES ('4', '张伟', '123456', 'doctor')

INSERT INTO `DOCTOR` (`id`, `tid`, `active`) VALUES ('4', '2', 1)

INSERT INTO `USER` (`id`, `USERNAME`, `PASSWORD`, `type`) VALUES ('5', '泽连斯基', '123456', 'doctor')

INSERT INTO `DOCTOR` (`id`, `tid`, `active`) VALUES ('5', '2', 1)

SELECT `username` FROM `USER` WHERE `id` IN (SELECT `id` FROM `DOCTOR` WHERE `active` = 1 AND `Tid` = '1');

INSERT INTO `USER` (`id`, `USERNAME`, `PASSWORD`, `type`) VALUES ('6', '21373405', '123456', 'patient')

INSERT INTO `PATIENT` (`id`, `iscommem`, `active`) VALUES ('6', 1, 1);

INSERT INTO Checkitems (`id`, `price`, `description`, `MinResult`, `MaxResult`)
VALUES 
('1', 1, '白细胞 (10-9/L)', 4, 10),
('2', 1, '淋巴细胞绝对值 (10-9/L)', 0.8, 4),
('3', 1, '中间细胞绝对值 (10-9/L)', 0.10, 0.90),
('4', 1, '中性粒细胞绝对值 (10-9/L)', 2, 7),
('5', 1, '淋巴细胞百分比 (%)', 20, 42),
('6', 1, '中间细胞百分比 (%)', 3, 7),
('7', 1, '中性粒细胞百分率 (%)', 50, 70),
('8', 1, '红细胞 (10^12/L)', 3.5, 5.5),
('9', 1, '血红蛋白 (g/L)', 110, 160),
('10', 1, '红细胞压积 (%)', 35, 50),
('11', 1, '平均红细胞压积 (fL)', 80, 100),
('12', 1, '平均红细胞血红蛋白 (pg)', 27, 34),
('13', 1, '平均血红蛋白浓度 (g/l)', 320, 360),
('14', 1, '红细胞分布宽度 (%)', 10.6, 15.5),
('15', 1, '血小板计数 (10^9/L)', 100, 500),
('16', 1, '平均血小板体积 (fl)', 7.4, 12.5),
('17', 1, '血小板分布宽度 (fL)', 12, 18.1),
('18', 1, '血小板压积 (%)', 0.108, 0.282),
('19', 1, 'ALT（丙氨酸氨基转移酶）（U/L）', 10, 40),
('20', 1, 'AST（天门冬氨酸氨基转移酶）（U/L）', 10, 34),
('21', 1, 'ALP（碱性磷酸酶）（U/L）', 40, 129),
('22', 1, '总胆红素（mg/dL）', 0.2, 1.2),
('23', 1, '直接胆红素（mg/dL）', 0, 0.3),
('24', 1, '间接胆红素（mg/dL）', 0.2, 0.8),
('25', 1, '总蛋白（g/dL）', 6.0, 8.3),
('26', 1, '白蛋白（g/dL）', 3.5, 5.0),
('27', 1, '球蛋白（g/dL）', 2.3, 3.4),
('28', 1, 'PT（凝血酶原时间）（seconds）', 11, 13.5),
('29', 1, 'PTT（部分凝血活酶时间）（seconds）', 25, 35);


INSERT INTO CheckCombine (`id`, `itemId`, `checkName`)
VALUES 
('1', '1', '血常规'),
('1', '2', '血常规'),
('1', '3', '血常规'),
('1', '4', '血常规'),
('1', '5', '血常规'),
('1', '6', '血常规'),
('1', '7', '血常规'),
('1', '8', '血常规'),
('1', '9', '血常规'),
('1', '10', '血常规'),
('1', '11', '血常规'),
('1', '12', '血常规'),
('1', '13', '血常规'),
('1', '14', '血常规'),
('1', '15', '血常规'),
('1', '16', '血常规'),
('1', '17', '血常规'),
('1', '18', '血常规');


INSERT INTO CheckCombine (id, itemId, checkName)
VALUES 
('2', '19', '肝功能检查'),
('2', '20', '肝功能检查'),
('2', '21', '肝功能检查'),
('2', '22', '肝功能检查'),
('2', '23', '肝功能检查'),
('2', '24', '肝功能检查'),
('2', '25', '肝功能检查'),
('2', '26', '肝功能检查'),
('2', '27', '肝功能检查'),
('2', '28', '肝功能检查'),
('2', '29', '肝功能检查');

INSERT INTO Drug (id, name, price, Description, isBanned, Storage) VALUES
('1', '沙丁胺醇 (瓶)', 180, '支持呼吸系统', false, 180),
('2', '葡萄糖 (瓶)', 180, '提供能量补充', false, 180),
('3', '抗病毒颗粒 (盒)', 150, '对抗病毒', false, 150),
('4', '感冒灵 (盒)', 150, '缓解感冒症状', false, 150),
('5', 'VC泡腾片 (盒)', 150, '维生素补充', false, 150),
('6', '快克 (盒)', 150, '缓解不适症状', false, 150),
('7', '布洛芬 (盒)', 150, '镇痛、退烧', false, 150),
('8', '黄连素 (盒)', 150, '消炎杀菌', false, 150),
('9', '达喜 (盒)', 150, '消炎、镇痛', false, 150),
('10', '蒙脱石散 (盒)', 150, '解毒、止泻', false, 150),
('11', '红霉素软膏 (管)', 150, '治疗皮肤感染', false, 150),
('12', '风油精 (瓶)', 180, '缓解肌肉疼痛', false, 180),
('13', '清凉油 (瓶)', 180, '舒缓头痛', false, 180),
('14', '炉甘石 (瓶)', 180, '缓解咳嗽', false, 180),
('15', '尿素霜 (瓶)', 180, '保湿滋润', false, 180),
('16', '膏药贴 (盒)', 150, '外伤贴敷', false, 150),
('17', '驱蚊液 (瓶)', 180, '驱赶蚊虫', false, 180),
('18', '玻璃酸钠 (瓶)', 150, '消毒清洁', false, 150),
('19', '萘敏维 (瓶)', 150, '抗过敏', false, 150),
('20', '氧氟沙星滴眼液 (瓶)', 150, '眼部抗菌', false, 150),
('21', '金霉素眼膏 (瓶)', 150, '眼部消炎', false, 150),
('22', '云南白药气雾剂 (瓶)', 150, '呼吸道舒缓', false, 150),
('23', '创口贴 (盒)', 150, '外伤处理', false, 150),
('24', '湿润烧伤膏 (瓶)', 150, '烧伤舒缓', false, 150),
('25', '林可霉素利多卡因凝胶 (瓶)', 150, '外伤处理', false, 150),
('26', '碘伏 (瓶)', 180, '伤口消毒', false, 180),
('27', '酒精 (瓶)', 180, '消毒用途', false, 180),
('28', '过氧化氢溶液 (瓶)', 180, '伤口处理', false, 180),
('29', '84消毒片 (瓶)', 180, '消毒杀菌', false, 180),
('30', '枇杷糖 (盒)', 150, '缓解咽喉不适', false, 150),
('31', '喉宝 (盒)', 150, '舒缓咽喉', false, 150),
('32', '西瓜霜 (盒)', 150, '清凉口腔', false, 150),
('33', '棉签 (支)', 1000, '清洁使用', false, 1000),
('34', '棉球 (个)', 1000, '清洁使用', false, 1000),
('35', '绷带 (卷)', 150, '外伤包扎', false, 150),
('36', '纱布 (卷)', 150, '外伤包扎', false, 150),
('37', '压舌板 (个)', 150, '医疗使用', false, 150),
('38', '胶带 (卷)', 10, '粘合固定', false, 10),
('39', '口罩 (个)', 500, '防护使用', false, 500),
('40', '手套 (双)', 500, '防护使用', false, 500);


INSERT INTO `ROOM` (`id`, `isOccupied`, `QueueLen`) VALUES
('101', true, 0),
('102', true, 0),
('201', true, 0),
('202', true, 0);



SELECT * FROM drug;

CREATE TRIGGER `DELETE_DRUG` BEFORE DELETE ON `drug` FOR EACH ROW
BEGIN
    DELETE FROM `checkcombine` WHERE `id` = OLD.id;
END

CREATE TRIGGER `DELETE_PATIENT` BEFORE DELETE ON `patient` FOR EACH ROW
BEGIN
    IF `patient`.`isComMem` = 1 THEN
        DELETE FROM `counter` WHERE `Pid` = OLD.id;
    END IF;
END


SELECT id FROM USER WHERE `USERNAME` = '21373405' AND password = '123456';

SELECT * FROM DOCTOR;

INSERT INTO `Dispatcher` (`TimePeriod`,`ROOMID`,`doctorId`,`TitleId`,`DATE`) VALUES
('morning', '101', '2', '1', 'Monday'),
('afternoon', '101', '2', '1', 'Tuesday'),
('morning', '101', '2', '1', 'Wednesday'),
('afternoon', '101', '2', '1', 'Thursday'),
('morning', '101', '2', '1', 'Friday'),
('afternoon', '101', '2', '1', 'Saturday'),
('morning', '101', '2', '1', 'Sunday'),
('afternoon', '101', '3', '1', 'Monday'),
('morning', '101', '3', '1', 'Tuesday'),
('afternoon', '101', '3', '1', 'Wednesday'),
('morning', '101', '3', '1', 'Thursday'),
('afternoon', '101', '3', '1', 'Friday'),
('morning', '101', '3', '1', 'Saturday'),
('afternoon', '101', '3', '1', 'Sunday'),
('morning', '201', '4', '2', 'Monday'),
('afternoon', '201', '4', '2', 'Tuesday'),
('morning', '201', '4', '2', 'Wednesday'),
('afternoon', '201', '4', '2', 'Thursday'),
('morning', '201', '4', '2', 'Friday'),
('afternoon', '201', '4', '2', 'Saturday'),
('morning', '201', '4', '2', 'Sunday'),
('afternoon', '201', '5', '2', 'Monday'),
('morning', '201', '5', '2', 'Tuesday'),
('afternoon', '201', '5', '2', 'Wednesday'),
('morning', '201', '5', '2', 'Thursday'),
('afternoon', '201', '5', '2', 'Friday'),
('morning', '201', '5', '2', 'Saturday'),
('afternoon', '201', '5', '2', 'Sunday');

SELECT * FROM COUNTER ;

SELECT * FROM diagnosis;

SELECT * FROM checkcombine;


SELECT * FROM laboratorysheet;

SELECT * FROM registrelation;

SELECT * FROM counter;

SELECT * FROM patient;

SELECT * FROM `user`;

SELECT * FROM `doctor`;

SELECT * FROM laboratorysheet;

SELECT * FROM counter;

SELECT * FROM medicinepurchase;

INSERT INTO `Drug` (`id`, `name`, `price`, `Description`, `isBanned`, `Storage`) VALUES
('41', '原石', 500, '打原神用的', false, 500);

SELECT * FROM `drug`;


SELECT * FROM `registrelation`;

SELECT * FROM `User`;

SELECT * FROM `LaboratorySheet`;

SELECT * FROM `checkitems`;