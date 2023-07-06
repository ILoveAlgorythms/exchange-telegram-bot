# ************************************************************
# Sequel Pro SQL dump
# Version 5446
#
# https://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 8.0.23)
# Database: p2p_exchange_bot
# Generation Time: 2023-07-06 17:13:31 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
SET NAMES utf8mb4;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table accounts_information_all_days
# ------------------------------------------------------------

CREATE TABLE `accounts_information_all_days` (
   `bank_id` INT UNSIGNED NOT NULL DEFAULT '0',
   `bank_name` VARCHAR(128) NOT NULL DEFAULT '',
   `account_id` INT UNSIGNED NOT NULL DEFAULT '0',
   `account_number` VARCHAR(512) NOT NULL DEFAULT '',
   `account_info` VARCHAR(512) NOT NULL DEFAULT '-',
   `account_limit` FLOAT NOT NULL DEFAULT '0',
   `total_uses` BIGINT NOT NULL DEFAULT '0',
   `total_sum` DOUBLE NOT NULL DEFAULT '0',
   `last_use` TIMESTAMP NULL DEFAULT NULL
) ENGINE=MyISAM;



# Dump of table accounts_information_per_day
# ------------------------------------------------------------

CREATE TABLE `accounts_information_per_day` (
   `bank_id` INT UNSIGNED NOT NULL DEFAULT '0',
   `bank_name` VARCHAR(128) NOT NULL DEFAULT '',
   `account_id` INT UNSIGNED NOT NULL DEFAULT '0',
   `account_number` VARCHAR(512) NOT NULL DEFAULT '',
   `account_limit` FLOAT NOT NULL DEFAULT '0',
   `account_info` VARCHAR(512) NOT NULL DEFAULT '-',
   `total_uses` BIGINT NOT NULL DEFAULT '0',
   `total_sum` DOUBLE NOT NULL DEFAULT '0',
   `starts_time` VARCHAR(19) NULL DEFAULT NULL,
   `last_use` TIMESTAMP NULL DEFAULT NULL
) ENGINE=MyISAM;



# Dump of table banks
# ------------------------------------------------------------

CREATE TABLE `banks` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `country_code` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `slug` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` enum('active','inactive','deleted') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'active',
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `created_at` timestamp NOT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `banks` WRITE;
/*!40000 ALTER TABLE `banks` DISABLE KEYS */;

INSERT INTO `banks` (`id`, `name`, `country_code`, `slug`, `status`, `updated_at`, `created_at`)
VALUES
	(1,'Wise','de','WiseE','active',NULL,'2023-05-13 13:53:20'),
	(2,'AdvCash','de','Advcash','active',NULL,'2023-05-13 13:46:18'),
	(3,'Тинькофф','ru','TinkoffNew','active',NULL,'2023-04-27 02:29:49'),
	(4,'AliPay','cn','Alipay','active',NULL,'2023-04-27 02:29:49'),
	(5,'Сбербанк','ru','-','active',NULL,'2023-05-13 14:13:33'),
	(8,'Райффайзенбанк','ru','-','active',NULL,'2023-05-16 20:36:15'),
	(10,'ERC-20','usdt','-','active',NULL,'2023-05-16 21:49:42'),
	(11,'BEP-20','usdt','-','active',NULL,'2023-05-16 21:50:06'),
	(12,'TRC-20','usdt','-','active',NULL,'2023-05-16 21:50:24'),
	(16,'Номер карты (Китай)','cn','-','active',NULL,'2023-06-23 10:46:42'),
	(17,'Wechat','cn','-','active',NULL,'2023-06-24 17:55:57');

/*!40000 ALTER TABLE `banks` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table config
# ------------------------------------------------------------

CREATE TABLE `config` (
  `technical_break` tinyint(1) NOT NULL DEFAULT '1',
  `notifications_deal_chat_id` bigint NOT NULL,
  `notifications_support_chat_id` bigint NOT NULL,
  `time_limit_dispute` int NOT NULL DEFAULT '0' COMMENT 'Кол-во времени, которое даётся на открытие спора (в минутах)',
  `limit_deals_per` int NOT NULL DEFAULT '0' COMMENT 'Кол-во сделок, которые можно совершать в time_limit_deals (в минутах)',
  `time_limit_deals` int NOT NULL DEFAULT '0' COMMENT 'Промежуток времени, в котором можно создавать limit_deals_per ',
  `time_cancel_deal` int NOT NULL DEFAULT '15',
  `affilate_mode` tinyint(1) NOT NULL DEFAULT '1',
  `google_sheet_id` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT '',
  `affilate_status` tinyint NOT NULL DEFAULT '1',
  `affilate_base_asset` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'USDT',
  `affilate_min_amount_withdrawal` float NOT NULL DEFAULT '30',
  `created_at` timestamp NOT NULL,
  `updated_at` timestamp NOT NULL ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `config` WRITE;
/*!40000 ALTER TABLE `config` DISABLE KEYS */;

INSERT INTO `config` (`technical_break`, `notifications_deal_chat_id`, `notifications_support_chat_id`, `time_limit_dispute`, `limit_deals_per`, `time_limit_deals`, `time_cancel_deal`, `affilate_mode`, `google_sheet_id`, `affilate_status`, `affilate_base_asset`, `affilate_min_amount_withdrawal`, `created_at`, `updated_at`)
VALUES
	(0,-1001989209456,-1001842587194,60,20,1,45,1,'',1,'USDT',30,'2023-04-25 09:15:21','2023-07-06 11:23:49');

/*!40000 ALTER TABLE `config` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table countries
# ------------------------------------------------------------

CREATE TABLE `countries` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `slug` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `countries` WRITE;
/*!40000 ALTER TABLE `countries` DISABLE KEYS */;

INSERT INTO `countries` (`id`, `slug`, `name`, `updated_at`, `created_at`)
VALUES
	(1,'ru','🇷🇺 Россия',NULL,NULL),
	(2,'ae','🇦🇪 ОАЭ',NULL,NULL),
	(3,'cn','🇨🇳 Китай',NULL,NULL),
	(4,'de','🇩🇪 Германия',NULL,NULL),
	(8,'usdt','usdt',NULL,'2023-05-16 20:42:35'),
	(9,'trx','trx',NULL,'2023-05-16 21:59:19');

/*!40000 ALTER TABLE `countries` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table deals
# ------------------------------------------------------------

CREATE TABLE `deals` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `uid` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '',
  `manager_id` int NOT NULL DEFAULT '0',
  `user_id` int NOT NULL,
  `from_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `from_amount` float NOT NULL,
  `from_bank_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'Bank',
  `from_bank_id` int NOT NULL DEFAULT '0',
  `from_payment_account_id` int NOT NULL DEFAULT '0',
  `from_requisites` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '-',
  `to_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `to_amount` float NOT NULL,
  `orig_to_amount` float NOT NULL,
  `to_bank_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `requisites` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `exchange_rate` float NOT NULL,
  `orig_exchange_rate` float NOT NULL,
  `spread` float NOT NULL DEFAULT '0',
  `profit` float DEFAULT '0',
  `profit_asset` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'USDT',
  `calculated_amount` float NOT NULL,
  `status` enum('new','accepted','process','paid','dispute','completed','declined') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'new',
  `expires` float NOT NULL DEFAULT '15',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_at` timestamp NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `deals` WRITE;
/*!40000 ALTER TABLE `deals` DISABLE KEYS */;

INSERT INTO `deals` (`id`, `uid`, `manager_id`, `user_id`, `from_name`, `from_amount`, `from_bank_name`, `from_bank_id`, `from_payment_account_id`, `from_requisites`, `to_name`, `to_amount`, `orig_to_amount`, `to_bank_name`, `requisites`, `exchange_rate`, `orig_exchange_rate`, `spread`, `profit`, `profit_asset`, `calculated_amount`, `status`, `expires`, `updated_at`, `created_at`)
VALUES
	(1,'367D59',0,1,'RUB',43555.5,'Сбербанк',5,0,'-','EUR',500,48395,'Wise','4199241',87.111,96.79,10,0,'USDT',1,'declined',15,'2023-06-24 17:51:52','2023-06-21 15:48:23'),
	(2,'9ED934',0,1,'RUB',43555.5,'Альфабанк',6,0,'-','EUR',500,48395,'Wise','1240919024',87.111,96.79,10,0,'USDT',1,'declined',15,'2023-06-24 17:51:46','2023-06-21 15:55:36'),
	(3,'0C348B',0,1,'RUB',43555.5,'Альфабанк',6,0,'-','EUR',500,48395,'AdvCash','12941924',87.111,96.79,10,0,'USDT',1,'declined',15,'2023-06-24 17:51:43','2023-06-21 21:57:28'),
	(4,'B60C2C',0,1,'RUB',43555.5,'Сбербанк',5,0,'-','EUR',500,48395,'AdvCash','129519529125',87.111,96.79,10,0,'USDT',1,'declined',15,'2023-06-24 17:51:39','2023-06-21 21:58:31'),
	(5,'C3D8EB',0,1,'RUB',500,'Сбербанк',5,0,'-','EUR',5.74,5.16582,'Wise','519259',87.111,96.79,10,0,'USDT',1,'declined',15,'2023-06-24 17:51:34','2023-06-21 21:59:58'),
	(6,'011630',0,1,'RUB',500,'Альфабанк',6,0,'-','EUR',5.74,5.16582,'Wise','124012040',87.111,96.79,10,0,'USDT',1,'declined',15,'2023-06-24 17:51:29','2023-06-22 12:16:36'),
	(7,'93386F',0,3,'RUB',9051.85,'Сбербанк',5,1,'-','USDT',100,8857,'TRC-20','JJJJJJJJJJJJJJJJJJJ',90.519,88.57,-2.2,2,'USDT',1,'completed',15,'2023-06-24 14:04:26','2023-06-22 19:00:56'),
	(8,'7D947A',0,3,'RUB',5000,'Сбербанк',5,1,'-','USDT',55.237,56.4525,'TRC-20','Ллллллллллл',90.519,88.57,-2.2,0,'USDT',1,'completed',15,'2023-06-22 19:20:25','2023-06-22 19:08:58'),
	(9,'601960',0,3,'RUB',50000,'Сбербанк',5,2,'-','USDT',552.373,564.525,'TRC-20','ааааааааааааааа',90.519,88.57,-2.2,0,'USDT',1,'declined',15,'2023-06-22 22:15:19','2023-06-22 20:36:03'),
	(10,'79FD99',0,1,'RUB',5000,'Тинькофф',3,5,'-','USDT',55.237,56.4525,'BEP-20','124195291',90.519,88.57,-2.2,0,'USDT',1,'declined',15,'2023-06-22 22:15:14','2023-06-22 22:12:25'),
	(11,'271C33',0,1,'RUB',5000,'Тинькофф',3,5,'-','USDT',55.237,56.4525,'BEP-20','124195291',90.519,88.57,-2.2,0,'USDT',1,'declined',15,'2023-06-22 22:15:10','2023-06-22 22:12:50'),
	(12,'B1EB3D',0,1,'RUB',45259.3,'Тинькофф',3,5,'-','USDT',500,44285,'BEP-20','1925195',90.519,88.57,-2.2,0,'USDT',1,'declined',15,'2023-06-22 22:15:05','2023-06-22 22:13:01'),
	(13,'4302BB',0,1,'RUB',5069.04,'Тинькофф',3,5,'-','USDT',56,4959.92,'ERC-20','194121920515',90.519,88.57,-2.2,0,'USDT',1,'declined',15,'2023-06-22 22:15:00','2023-06-22 22:13:40'),
	(14,'714588',0,3,'USDT',100,'TRC-20',12,0,'-','CNY',743.04,688,'Номер карты (Китай)','вввввввввввввввввввввв',7.43,6.88,-8,0,'USDT',1,'declined',15,'2023-06-23 11:40:54','2023-06-23 11:40:36'),
	(15,'81BB31',0,3,'RUB',5000,'Сбербанк',5,1,'-','USDT',55.237,56.4525,'TRC-20','ffffffffffffffffffffffffff',90.519,88.57,-2.2,5.5,'USDT',1,'completed',15,'2023-06-24 17:53:49','2023-06-24 17:46:51'),
	(16,'B93BC7',0,3,'RUB',5000,'Сбербанк',5,2,'-','USDT',55.237,56.4525,'TRC-20','kkkkkkkkkkkkkkkkkkkkkkkk',90.519,88.57,-2.2,0,'USDT',1,'declined',15,'2023-06-24 18:05:54','2023-06-24 18:05:12'),
	(17,'FD589A',0,3,'RUB',50000,'Сбербанк',5,2,'-','USDT',552.373,564.525,'TRC-20','jjjjjjjjjjjjjjjjjjjjjjjjjjj',90.519,88.57,-2.2,100,'USDT',1,'completed',15,'2023-06-24 18:09:42','2023-06-24 18:06:43'),
	(18,'E628CD',0,3,'RUB',5000,'Сбербанк',5,1,'-','USDT',55.237,56.4525,'TRC-20','рррррррррррррррррррр',90.519,88.57,-2.2,0,'USDT',1,'completed',15,'2023-06-24 18:10:49','2023-06-24 18:08:05'),
	(19,'139A34',0,3,'RUB',5000,'Сбербанк',5,1,'-','USDT',55.237,56.4525,'TRC-20','аааааааааааааааааааааа',90.519,88.57,-2.2,0,'USDT',1,'declined',15,'2023-06-27 13:00:28','2023-06-24 18:11:03'),
	(20,'03CB40',0,1,'USDT',116.366,'BEP-20',11,0,'-','CNY',750,109.012,'Номер карты (Китай)','12049125912591',6.445,6.88,6.32,0,'USDT',1,'declined',15,'2023-06-26 19:43:11','2023-06-26 19:43:05'),
	(21,'ABAD97',0,1,'USDT',775.773,'BEP-20',11,6,'-','CNY',5000,726.744,'Wechat','905919219 91294',6.445,6.88,6.32,0,'USDT',1,'declined',15,'2023-06-27 01:25:26','2023-06-26 20:12:50'),
	(22,'6AE6F1',0,1,'RUB',45259.3,'Сбербанк',5,1,'-','USDT',500,44285,'TRC-20','1941929125',90.519,88.57,-2.2,0,'USDT',1,'declined',15,'2023-06-27 01:28:30','2023-06-27 01:28:11'),
	(23,'DD8A6E',0,5,'RUB',55500,'Сбербанк',5,1,'-','USDT',613.134,626.623,'TRC-20','TCZKVaF6KPLrdtqn39Ng3tGV8ipGF5vJY4',90.519,88.57,-2.2,0,'USDT',1,'declined',15,'2023-06-27 13:07:55','2023-06-27 12:37:48'),
	(24,'461581',0,1,'USDT',500,'BEP-20',11,6,'-','CNY',3246.01,3465,'Номер карты (Китай)','1249120951209',6.492,6.93,6.32,0,'USDT',1,'declined',15,'2023-06-27 13:01:06','2023-06-27 12:52:10'),
	(25,'2A8B6C',0,3,'RUB',5000,'Райффайзенбанк',8,3,'-','USDT',54.529,53.7115,'TRC-20','ооооооооооо',91.694,93.09,1.5,0,'USDT',1,'declined',15,'2023-06-27 13:00:45','2023-06-27 12:56:18'),
	(26,'7EAFDE',0,1,'USDT',770.176,'BEP-20',11,6,'-','CNY',5000,721.501,'Номер карты (Китай)','1125912951295',6.492,6.93,6.32,0,'USDT',1,'declined',15,'2023-06-27 13:01:12','2023-06-27 12:57:01'),
	(27,'BC68D8',0,3,'RUB',5000,'Тинькофф',3,5,'-','USDT',54.529,53.7115,'TRC-20','gsfddddddddddd',91.694,93.09,1.5,0,'USDT',1,'declined',15,'2023-06-27 13:00:53','2023-06-27 12:59:12'),
	(28,'299B45',0,3,'RUB',5000,'Тинькофф',3,5,'-','USDT',54.529,53.7115,'TRC-20','gggggggggg',91.694,93.09,1.5,0,'USDT',1,'declined',15,'2023-06-27 12:59:56','2023-06-27 12:59:32'),
	(29,'F6C802',0,5,'RUB',55500,'Сбербанк',5,1,'-','USDT',603.979,594.919,'TRC-20','TCZKVaF6KPLrdtqn39Ng3tGV8ipGF5vJY4',91.891,93.29,1.5,0,'USDT',1,'declined',15,'2023-06-27 13:38:09','2023-06-27 13:22:56'),
	(30,'B90E55',0,1,'USDT',500,'BEP-20',11,0,'-','CNY',3246.01,3465,'Номер карты (Китай)','10924099024',6.492,6.93,6.32,0,'USDT',1,'declined',15,'2023-06-27 15:42:42','2023-06-27 15:35:43'),
	(31,'E17C7B',0,1,'USDT',770.176,'BEP-20',11,0,'-','CNY',5000,721.501,'Номер карты (Китай)','102419409124',6.492,6.93,6.32,0,'USDT',1,'declined',15,'2023-06-27 15:42:54','2023-06-27 15:40:50'),
	(32,'0C8031',0,1,'USDT',500,'BEP-20',11,0,'-','CNY',3246.01,3465,'Номер карты (Китай)','129419251925',6.492,6.93,6.32,0,'USDT',1,'declined',15,'2023-06-27 15:42:49','2023-06-27 15:42:34'),
	(33,'5D8745',0,1,'RUB',45861.6,'Райффайзенбанк',8,3,'-','USDT',500,46560,'ERC-20','12491951295',91.723,93.12,1.5,0,'USDT',1,'completed',15,'2023-06-27 15:44:17','2023-06-27 15:43:59'),
	(34,'C3E60B',1,1,'RUB',5000,'Райффайзенбанк',8,3,'-','USDT',54.576,53.7577,'TRC-20','10512051095125',91.615,93.01,1.5,1,'USDT',1,'completed',15,'2023-06-27 15:49:14','2023-06-27 15:48:37'),
	(35,'FDB9FC',0,5,'RUB',15000,'Тинькофф',3,5,'-','USDT',163.518,161.065,'TRC-20','TCZKVaF6KPLrdtqn39Ng3tGV8ipGF5vJY4',91.733,93.13,1.5,0,'USDT',1,'declined',15,'2023-06-27 16:27:39','2023-06-27 16:11:50'),
	(36,'9C3BE6',0,5,'RUB',8725,'Сбербанк',5,1,'-','USDT',95.154,93.7265,'TRC-20','TCZKVaF6KPLrdtqn39Ng3tGV8ipGF5vJY4',91.694,93.09,1.5,0,'USDT',1,'declined',15,'2023-06-27 16:45:46','2023-06-27 16:30:09'),
	(37,'3635B7',3,3,'RUB',5000,'Сбербанк',5,1,'-','USDT',54.453,53.6366,'TRC-20','оооооооооооооооо',91.822,93.22,1.5,0,'USDT',1,'declined',15,'2023-06-27 17:01:37','2023-06-27 17:00:26'),
	(38,'6154BA',0,1,'RUB',45910.9,'Райффайзенбанк',8,3,'-','USDT',500,46610,'BEP-20','9234591941',91.822,93.22,1.5,0,'USDT',1,'declined',15,'2023-06-27 17:15:56','2023-06-27 17:00:44'),
	(39,'843042',0,5,'RUB',17000,'Сбербанк',5,1,'-','USDT',185.141,182.364,'TRC-20','TCZKVaF6KPLrdtqn39Ng3tGV8ipGF5vJY4',91.822,93.22,1.5,0,'USDT',1,'declined',15,'2023-06-27 17:15:56','2023-06-27 17:00:54'),
	(40,'53D5AE',12,5,'RUB',13485,'Тинькофф',3,5,'-','USDT',146.861,144.658,'TRC-20','TCZKVaF6KPLrdtqn39Ng3tGV8ipGF5vJY4',91.822,93.22,1.5,7.03,'USDT',1,'completed',15,'2023-06-27 17:33:01','2023-06-27 17:03:14'),
	(41,'1511F1',0,5,'RUB',29760,'Тинькофф',3,5,'-','USDT',324.002,319.142,'TRC-20','TCZKVaF6KPLrdtqn39Ng3tGV8ipGF5vJY4',91.851,93.25,1.5,0,'USDT',1,'declined',15,'2023-06-27 17:28:00','2023-06-27 17:12:11'),
	(42,'F24B78',12,5,'RUB',17000,'Тинькофф',3,5,'-','USDT',185.201,182.423,'TRC-20','TCZKVaF6KPLrdtqn39Ng3tGV8ipGF5vJY4',91.792,93.19,1.5,9.26,'USDT',1,'completed',15,'2023-06-27 17:30:49','2023-06-27 17:20:36'),
	(43,'A36D2A',12,5,'RUB',29760,'Тинькофф',3,5,'-','USDT',324.176,319.313,'TRC-20','TCZKVaF6KPLrdtqn39Ng3tGV8ipGF5vJY4',91.802,93.2,1.5,16.87,'USDT',1,'completed',15,'2023-06-27 17:44:25','2023-06-27 17:34:21'),
	(44,'A247A4',12,5,'RUB',55500,'Сбербанк',5,1,'-','USDT',604.497,595.43,'TRC-20','TCZKVaF6KPLrdtqn39Ng3tGV8ipGF5vJY4',91.812,93.21,1.5,32.14,'USDT',1,'completed',15,'2023-06-27 18:14:37','2023-06-27 18:04:28'),
	(45,'3DE0B3',12,5,'RUB',8725,'Сбербанк',5,1,'-','USDT',94.97,93.5456,'TRC-20','TCZKVaF6KPLrdtqn39Ng3tGV8ipGF5vJY4',91.871,93.27,1.5,4.21,'USDT',1,'completed',15,'2023-06-27 18:21:44','2023-06-27 18:07:40'),
	(46,'C74719',12,5,'RUB',11500,'Сбербанк',5,1,'-','USDT',125.176,123.298,'TRC-20','TCZKVaF6KPLrdtqn39Ng3tGV8ipGF5vJY4',91.871,93.27,1.5,5.82,'USDT',1,'completed',15,'2023-06-27 18:32:21','2023-06-27 18:08:44'),
	(47,'81A823',3,1,'RUB',68353.6,'Сбербанк',5,0,'-','CNY',5000,71800,'Номер карты (Китай)','120959 124091209',13.671,14.36,4.8,0,'USDT',1,'declined',16,'2023-06-27 22:09:02','2023-06-27 18:49:45'),
	(48,'FB226D',0,5,'RUB',20500,'Тинькофф',3,5,'-','USDT',222.068,218.737,'TRC-20','TCZKVaF6KPLrdtqn39Ng3tGV8ipGF5vJY4',92.314,93.72,1.5,0,'USDT',1,'declined',45,'2023-06-28 15:23:55','2023-06-28 14:38:44'),
	(49,'12DC8E',12,5,'RUB',20500,'Тинькофф',3,5,'-','USDT',220.866,217.553,'TRC-20','TCZKVaF6KPLrdtqn39Ng3tGV8ipGF5vJY4',92.817,94.23,1.5,11.24,'USDT',1,'completed',45,'2023-06-28 16:37:11','2023-06-28 16:27:21'),
	(50,'819C33',0,13,'RUB',46487.1,'Тинькофф',3,5,'-','USDT',500,47195,'TRC-20','Sffghhhh',92.974,94.39,1.5,0,'USDT',1,'declined',45,'2023-06-28 18:27:55','2023-06-28 17:42:09'),
	(51,'2F56CF',0,5,'RUB',66960,'Сбербанк',5,1,'-','USDT',719.286,708.496,'TRC-20','TCZKVaF6KPLrdtqn39Ng3tGV8ipGF5vJY4',93.092,94.51,1.5,0,'USDT',1,'declined',45,'2023-06-28 21:33:59','2023-06-28 20:48:40'),
	(52,'E8B4DF',12,5,'RUB',10500,'Тинькофф',3,5,'-','USDT',112.411,110.724,'TRC-20','TCZKVaF6KPLrdtqn39Ng3tGV8ipGF5vJY4',93.408,94.83,1.5,5.04,'USDT',1,'completed',45,'2023-06-29 10:47:05','2023-06-29 10:30:32'),
	(53,'D10DA3',12,5,'RUB',13940,'Тинькофф',3,5,'-','USDT',148.269,146.045,'TRC-20','TCZKVaF6KPLrdtqn39Ng3tGV8ipGF5vJY4',94.018,95.45,1.5,7.11,'USDT',1,'completed',45,'2023-06-29 12:05:38','2023-06-29 11:42:39'),
	(54,'C151E5',0,5,'RUB',11750,'Тинькофф',3,5,'-','USDT',124.976,123.101,'TRC-20','TCZKVaF6KPLrdtqn39Ng3tGV8ipGF5vJY4',94.018,95.45,1.5,0,'USDT',1,'declined',45,'2023-06-29 12:29:30','2023-06-29 11:43:56'),
	(55,'85FDFC',12,5,'RUB',11750,'Тинькофф',3,5,'-','USDT',125.002,123.127,'TRC-20','TCZKVaF6KPLrdtqn39Ng3tGV8ipGF5vJY4',93.999,95.43,1.5,5.69,'USDT',1,'completed',45,'2023-06-29 12:38:39','2023-06-29 12:30:41'),
	(56,'476F68',12,5,'RUB',10500,'Тинькофф',3,5,'-','USDT',111.844,110.167,'TRC-20','TCZKVaF6KPLrdtqn39Ng3tGV8ipGF5vJY4',93.88,95.31,1.5,5.08,'USDT',1,'completed',45,'2023-06-29 15:19:22','2023-06-29 15:10:00'),
	(57,'8E65B2',18,18,'RUB',7097.16,'Сбербанк',5,0,'-','CNY',500,7455,'AliPay','12041092490',14.194,14.91,4.8,0,'USDT',1,'declined',45,'2023-07-05 16:00:36','2023-07-05 15:48:10'),
	(58,'A7E3B1',18,18,'RUB',5000,'Сбербанк',5,1,'-','USDT',51.729,50.9528,'BEP-20','120419241',96.658,98.13,1.5,0,'USDT',1,'declined',45,'2023-07-05 16:00:31','2023-07-05 15:48:25'),
	(59,'C0A88A',3,3,'RUB',96589.1,'Сбербанк',5,1,'-','USDT',1000,98060,'TRC-20','Коктаиаиаиаоа',96.589,98.06,1.5,0,'USDT',1,'declined',45,'2023-07-05 16:00:56','2023-07-05 15:59:54'),
	(60,'195A98',3,3,'RUB',50000,'Сбербанк',5,1,'-','USDT',510.576,502.917,'TRC-20','Ппоплпоплагпо',97.929,99.42,1.5,0,'USDT',1,'declined',45,'2023-07-06 10:38:19','2023-07-06 10:38:06'),
	(61,'719057',18,18,'RUB',5000,'Сбербанк',5,1,'-','USDT',50.554,49.7958,'TRC-20','12941249125',98.904,100.41,1.5,0,'USDT',1,'declined',45,'2023-07-06 10:47:39','2023-07-06 10:40:03'),
	(62,'3458B4',18,18,'RUB',5000,'Тинькофф',3,5,'-','USDT',50.554,49.7958,'BEP-20','124012590125',98.904,100.41,1.5,0,'USDT',1,'declined',45,'2023-07-06 10:47:29','2023-07-06 10:41:46'),
	(63,'30B5EF',18,18,'RUB',5000,'Сбербанк',5,1,'-','USDT',50.554,49.7958,'BEP-20','12951925912591250',98.904,100.41,1.5,0,'USDT',1,'declined',45,'2023-07-06 10:47:34','2023-07-06 10:42:00'),
	(64,'177B78',18,18,'RUB',5000,'Сбербанк',5,0,'-','CNY',343.275,326.797,'Номер карты (Китай)','591129519025',14.566,15.3,4.8,0,'USDT',1,'declined',45,'2023-07-06 10:47:25','2023-07-06 10:42:09'),
	(65,'3E26D1',18,18,'RUB',49451.9,'Сбербанк',5,1,'-','USDT',500,50205,'BEP-20','125912951925912519205',98.904,100.41,1.5,0,'USDT',1,'declined',45,'2023-07-06 10:47:21','2023-07-06 10:42:21'),
	(66,'D97CF4',18,18,'USDT',766.856,'BEP-20',11,6,'-','CNY',5000,718.391,'Номер карты (Китай)','5219915212590',6.52,6.96,6.32,0,'USDT',1,'declined',45,'2023-07-06 10:47:17','2023-07-06 10:42:32'),
	(67,'4D9930',18,18,'RUB',49451.9,'Сбербанк',5,1,'-','USDT',500,50205,'BEP-20','500192519255912',98.904,100.41,1.5,0,'USDT',1,'declined',45,'2023-07-06 10:47:12','2023-07-06 10:42:46'),
	(68,'3B08D0',18,18,'RUB',5000,'Сбербанк',5,1,'-','USDT',50.554,49.7958,'BEP-20','129419024901',98.904,100.41,1.5,0,'USDT',1,'declined',45,'2023-07-06 10:47:07','2023-07-06 10:44:45'),
	(69,'62B476',0,18,'RUB',5000,'Сбербанк',5,1,'-','USDT',50.772,50.01,'BEP-20','121925912',98.48,99.98,1.5,0,'USDT',1,'declined',45,'2023-07-06 11:34:56','2023-07-06 10:49:37'),
	(70,'A7DCAB',0,18,'RUB',49240.1,'Тинькофф',3,5,'-','USDT',500,49990,'ERC-20','941294',98.48,99.98,1.5,0,'USDT',1,'declined',45,'2023-07-06 11:34:56','2023-07-06 10:49:48'),
	(71,'85B867',0,18,'RUB',5000,'Сбербанк',5,1,'-','USDT',50.772,50.01,'BEP-20','12591295',98.48,99.98,1.5,0,'USDT',1,'declined',45,'2023-07-06 11:35:56','2023-07-06 10:49:58'),
	(72,'060AC6',0,18,'RUB',5000,'Сбербанк',5,1,'-','USDT',50.772,50.01,'BEP-20','12941924',98.48,99.98,1.5,0,'USDT',1,'declined',45,'2023-07-06 11:36:57','2023-07-06 10:51:29'),
	(73,'0DF327',12,5,'RUB',38466,'Сбербанк',5,1,'-','USDT',390.557,384.698,'TRC-20','TCZKVaF6KPLrdtqn39Ng3tGV8ipGF5vJY4',98.49,99.99,1.5,21.7,'USDT',1,'completed',45,'2023-07-06 11:38:53','2023-07-06 11:12:36'),
	(74,'DD7412',12,5,'RUB',42000,'Сбербанк',5,1,'-','USDT',428.582,422.153,'TRC-20','TCZKVaF6KPLrdtqn39Ng3tGV8ipGF5vJY4',97.998,99.49,1.5,22.42,'USDT',1,'completed',45,'2023-07-06 11:47:47','2023-07-06 11:21:18'),
	(75,'F416A7',12,5,'RUB',44650,'Сбербанк',5,1,'-','USDT',455.623,448.789,'TRC-20','TCZKVaF6KPLrdtqn39Ng3tGV8ipGF5vJY4',97.998,99.49,1.5,21.76,'USDT',1,'completed',45,'2023-07-06 11:52:40','2023-07-06 11:25:18'),
	(76,'C4BBD4',12,5,'RUB',96560,'Райффайзенбанк',8,3,'-','USDT',983.649,968.894,'TRC-20','TCZKVaF6KPLrdtqn39Ng3tGV8ipGF5vJY4',98.165,99.66,1.5,54.52,'USDT',1,'completed',45,'2023-07-06 12:07:46','2023-07-06 11:42:47'),
	(77,'2652DF',12,5,'RUB',25990,'Сбербанк',5,2,'-','USDT',268.448,264.422,'TRC-20','TCZKVaF6KPLrdtqn39Ng3tGV8ipGF5vJY4',96.816,98.29,1.5,13.66,'USDT',1,'completed',45,'2023-07-06 13:59:05','2023-07-06 13:29:45'),
	(78,'75E611',0,5,'RUB',65000,'Тинькофф',3,5,'-','USDT',668.658,658.628,'TRC-20','TCZKVaF6KPLrdtqn39Ng3tGV8ipGF5vJY4',97.21,98.69,1.5,0,'USDT',1,'declined',45,'2023-07-06 16:41:37','2023-07-06 15:56:35');

/*!40000 ALTER TABLE `deals` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table dialogs
# ------------------------------------------------------------

CREATE TABLE `dialogs` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `deal_id` int NOT NULL DEFAULT '0',
  `type` enum('support','deal','other') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'support',
  `status` enum('open','answered') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'open',
  `title` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'Ticket',
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `created_at` timestamp NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Dump of table messages
# ------------------------------------------------------------

CREATE TABLE `messages` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `dialog_id` int NOT NULL,
  `text` varchar(2048) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `attach` json NOT NULL,
  `content_type` enum('text','video','document','photo') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'text',
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `created_at` timestamp NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Dump of table pages
# ------------------------------------------------------------

CREATE TABLE `pages` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `slug` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `page_title` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `page_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `document` json DEFAULT NULL,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_at` timestamp NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `pages` WRITE;
/*!40000 ALTER TABLE `pages` DISABLE KEYS */;

INSERT INTO `pages` (`id`, `user_id`, `slug`, `page_title`, `page_content`, `document`, `updated_at`, `created_at`)
VALUES
	(1,1,'faq','FAQ','❗️Этот раздел редактируется в административной панели\\.\n\nСтраницы -> Faq -> Изменить текст','null','2023-06-17 10:09:35','2023-05-01 09:41:55'),
	(2,1,'agreement','Условия предоставления сервиса','Прочтите соглашение','{\"path\": \"/media/Соглашение.docx\", \"file_id\": \"BQACAgIAAxkBAAIKVmScUAHBbx62nvZyLlJAY1xDKx9vAAJZLwAC-8DgSFZ5egGWqVVcLwQ\"}','2023-06-28 18:21:37','2023-05-01 09:41:55'),
	(3,1,'admin_note','Заметки для админов/менеджеров','Бан пользователя:\n— /ban логин/@логин/телеграм айди\n\nВыдать админку:\n— /set\\_admin огин/@логин/телеграм айди','null','2023-05-28 17:37:14','2023-05-01 09:41:55'),
	(4,1,'verification','Верификация личности','\\*Для начала работы со мной тебе потребуется пройти быструю верификацию\\.\\*\n\nЕсть 2 способа это сделать:\n\n1\\. Верификация карты 💳:\nЕсли ты будешь отправлять деньги с карты которая у тебя в наличии, необходимо сделать фото карты на фоне открытого в телеграм моего юзернейм @GreenWalletExchangeBot\nПосле этого можешь совершать любой обмен оплачивая именно с этой карты\\.\n\n2\\. Верификация личности 👤:\nЕсли ты хочешь отправлять и принимать платежи с разных карт, необходимо сделать селфи видео, где показать свой паспорт и открытый телеграм с нашим юзернейм\\. После этого можешь совершать любые обмены без ограничений\\.\n\nПримечание: данная верификация проходит в рамках борьбы с мошенничеством, служит для защиты наших пользователей, является конфиденциальной и не разглашается третьим лицам, кроме случаев предусмотренных законодательством\\.\n\nПолное описание процесса верификации смотри в прикрепленном файле\\.','null','2023-06-21 07:54:05','2023-05-01 09:41:55');

/*!40000 ALTER TABLE `pages` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table pairs
# ------------------------------------------------------------

CREATE TABLE `pairs` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT '0',
  `from_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT 'Отдаваемый актив',
  `from_handler_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'EMPTY' COMMENT 'Отдаваемый актив',
  `from_country_code` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'ru',
  `min_from_amount` float NOT NULL DEFAULT '0',
  `max_from_amount` float NOT NULL DEFAULT '0',
  `from_type` enum('fiat','crypto') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'fiat',
  `verification_account` tinyint NOT NULL DEFAULT '0',
  `to_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT 'Получаемый актив',
  `to_handler_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'EMPTY' COMMENT 'Получаемый актив',
  `to_country_code` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'ru' COMMENT 'Айди категории банков для получаемого актива',
  `to_type` enum('fiat','crypto') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'fiat',
  `to_requisites_comment` varchar(2048) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '-',
  `handler_direction` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'EMPTY',
  `proxy_asset` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'USDT' COMMENT 'Прокси актив (USDT, BUSD) для фильтра котировок на Binance',
  `spread` float NOT NULL DEFAULT '0' COMMENT 'Спред',
  `price_handler` enum('binance','cryptoexchage') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'cryptoexchage',
  `handler_inverted` tinyint(1) NOT NULL DEFAULT '0',
  `auto_requisites` tinyint(1) NOT NULL DEFAULT '0',
  `is_active` tinyint(1) NOT NULL DEFAULT '0',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_at` timestamp NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `pairs` WRITE;
/*!40000 ALTER TABLE `pairs` DISABLE KEYS */;

INSERT INTO `pairs` (`id`, `user_id`, `from_name`, `from_handler_name`, `from_country_code`, `min_from_amount`, `max_from_amount`, `from_type`, `verification_account`, `to_name`, `to_handler_name`, `to_country_code`, `to_type`, `to_requisites_comment`, `handler_direction`, `proxy_asset`, `spread`, `price_handler`, `handler_inverted`, `auto_requisites`, `is_active`, `updated_at`, `created_at`)
VALUES
	(1,0,'RUB','SBERRUB','ru',100,100000,'fiat',1,'EUR','WISEEUR','de','fiat','-','in','USDT',10,'cryptoexchage',0,1,0,'2023-06-22 18:57:28','2023-04-26 11:17:27'),
	(2,0,'EUR','WISEEUR','de',100,10000,'fiat',0,'RUB','SBERRUB','ru','fiat','-','out','USDT',2,'cryptoexchage',0,0,0,'2023-05-13 09:57:08','2023-04-26 11:17:27'),
	(14,0,'RUB','EMPTY','RU',1000,100000,'crypto',0,'USDT','EMPTY','RU','fiat','-','EMPTY','USDT',2,'cryptoexchage',0,0,0,'2023-05-16 20:23:35','2023-05-16 19:17:12'),
	(17,0,'RUB','SBERRUB','RU',5000,100000,'fiat',0,'USDT','USDTTRC20','usdt','crypto','-','EMPTY','USDT',1.5,'cryptoexchage',0,1,1,'2023-06-27 12:54:40','2023-05-16 21:38:16'),
	(21,3,'RUB','SBERRUB','ru',5000,200000,'fiat',0,'CNY','WIRECNY','cn','fiat','-','EMPTY','USDT',4.8,'cryptoexchage',0,0,1,'2023-06-23 10:45:48','2023-06-23 10:37:17'),
	(22,3,'USDT','USDTTRC20','usdt',100,3500,'fiat',0,'CNY','CARDCNY','cn','fiat','-','EMPTY','USDT',6.32,'cryptoexchage',0,1,1,'2023-06-26 19:56:56','2023-06-23 10:50:26');

/*!40000 ALTER TABLE `pairs` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table payment_accounts
# ------------------------------------------------------------

CREATE TABLE `payment_accounts` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `bank_id` int NOT NULL,
  `account` varchar(512) NOT NULL DEFAULT '',
  `account_limit` float NOT NULL DEFAULT '0',
  `account_info` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '-',
  `account_period_limit` bigint NOT NULL DEFAULT '1440',
  `status` enum('active','inactive','deleted') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'active',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_at` timestamp NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account` (`account`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `payment_accounts` WRITE;
/*!40000 ALTER TABLE `payment_accounts` DISABLE KEYS */;

INSERT INTO `payment_accounts` (`id`, `user_id`, `bank_id`, `account`, `account_limit`, `account_info`, `account_period_limit`, `status`, `updated_at`, `created_at`)
VALUES
	(1,3,5,'2202206707015033',200000,'Старожук Никита Андреевич',1440,'active',NULL,'2023-06-22 18:59:56'),
	(2,3,5,'2202206739415060',200000,'Макарова Елизавета Антоновна',1440,'active',NULL,'2023-06-22 18:59:56'),
	(3,3,8,'2200300503321703',200000,'Старожук Никита Андреевич',1440,'active',NULL,'2023-06-22 19:23:32'),
	(5,3,3,'2200700822997705',200000,'Старожук Никита Андреевич',1440,'active',NULL,'2023-06-22 19:25:42'),
	(6,3,11,'0x115A1b3712bB13C985FF78d3745bb200bA3748cA',1000000,'Менеджер №1',1440,'active','2023-06-28 14:46:25','2023-06-24 18:00:31'),
	(8,3,12,'TDwMPNq2R7WhN8FPuSN3hZrQUccYNZH5Yx',1000000,'Менеджер №1',1440,'active','2023-06-27 14:07:33','2023-06-24 18:01:50'),
	(12,3,5,'4276380147568047',100000,'Валерий Грек',1440,'active','2023-06-28 14:39:50','2023-06-28 14:39:50'),
	(13,3,8,'2200300118777380',100000,'Александр Савилов',1440,'active','2023-06-28 14:41:30','2023-06-28 14:41:31'),
	(14,3,8,'2200300517482004',100000,'Валерий Грек',1440,'active','2023-06-28 14:41:30','2023-06-28 14:41:31'),
	(15,3,12,'TXpD47j8PZ981vfS9TnXeqtUUgYWTBRCEp',1000000,'Менеджер №2',1440,'active','2023-06-28 14:43:07','2023-06-28 14:43:07'),
	(16,3,11,'0x8c67F90F5a347035C2180aC78D8D0bF3724aC064',1000000,'Менеджер №2',1440,'active','2023-06-28 14:45:46','2023-06-28 14:43:50');

/*!40000 ALTER TABLE `payment_accounts` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table reviews
# ------------------------------------------------------------

CREATE TABLE `reviews` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `object_id` int NOT NULL,
  `type` enum('deal','ticket','other') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'deal',
  `updated_at` timestamp NOT NULL ON UPDATE CURRENT_TIMESTAMP,
  `created_at` timestamp NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Dump of table rooms
# ------------------------------------------------------------

CREATE TABLE `rooms` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `dialog_id` int DEFAULT NULL,
  `manager_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `status` enum('free','busy','cleaning','close') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'free',
  `updated_at` int DEFAULT NULL,
  `created_at` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Dump of table tasks
# ------------------------------------------------------------

CREATE TABLE `tasks` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Dump of table transactions
# ------------------------------------------------------------

CREATE TABLE `transactions` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL DEFAULT '0',
  `recieve_id` int NOT NULL DEFAULT '0',
  `type` enum('tx','affiliate','chargeback') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'tx',
  `amount` float NOT NULL DEFAULT '0',
  `asset` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `status` enum('success','pending','declined') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'pending',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_at` timestamp NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



# Dump of table users
# ------------------------------------------------------------

CREATE TABLE `users` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `uid` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT '',
  `telegram_id` bigint NOT NULL,
  `refferer_id` int NOT NULL DEFAULT '0',
  `language_code` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'ru',
  `username` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'username_is_empty',
  `verification` enum('anonymous','process','card_verified','full_verified') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT 'anonymous',
  `verification_data` json DEFAULT NULL,
  `role` enum('user','manager','admin') NOT NULL DEFAULT 'user',
  `is_admin` int NOT NULL DEFAULT '0',
  `is_agreement` tinyint(1) NOT NULL DEFAULT '0',
  `is_banned` tinyint(1) NOT NULL DEFAULT '0',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_at` timestamp NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;

INSERT INTO `users` (`id`, `uid`, `telegram_id`, `refferer_id`, `language_code`, `username`, `verification`, `verification_data`, `role`, `is_admin`, `is_agreement`, `is_banned`, `updated_at`, `created_at`)
VALUES
	(2,'937E04',1776127555,18,'ru','mr_x0r','anonymous','null','user',0,1,0,'2023-07-06 19:05:28','2023-04-26 17:02:17'),
	(3,'326794',5698719743,4,'ru','ZergTrust','anonymous','null','admin',1,1,0,'2023-07-06 19:19:11','2023-04-28 11:56:54'),
	(4,'4559DB',37913419,0,'ru','MrGreen4you','anonymous','null','admin',1,1,0,'2023-07-06 17:01:35','2023-04-28 12:10:34'),
	(5,'00CF13',812027680,0,'ru','mrslera','anonymous','null','user',1,1,0,'2023-07-06 17:01:35','2023-04-28 12:12:25'),
	(6,'E75945',1620022975,4,'ru','ibatenka','card_verified','{\"card_verified\": \"4276550100766313\"}','user',1,1,0,'2023-07-06 19:19:13','2023-05-08 14:55:46'),
	(7,'ACC960',5343576955,0,'ru','mr_osminolog','anonymous','null','user',0,1,0,'2023-07-06 17:01:35','2023-05-12 11:08:42'),
	(8,'B9E6A4',567350571,0,'ru','KirSchmunk','anonymous','null','user',0,1,0,'2023-07-06 17:01:35','2023-05-12 20:22:38'),
	(9,'9F7611',397039103,0,'ru','arturkogut','anonymous','null','user',0,1,0,'2023-07-06 17:01:35','2023-05-12 20:45:04'),
	(10,'691A53',409074651,0,'ru','MiyukiMori','anonymous','null','user',0,1,0,'2023-07-06 19:19:21','2023-05-15 23:12:13'),
	(11,'986660',391711549,0,'ru','Trust5001','anonymous','null','user',0,1,0,'2023-07-06 17:01:35','2023-05-18 15:43:18'),
	(12,'08B7F5',801293585,0,'ru','prepo_d','anonymous','null','admin',0,1,0,'2023-07-06 19:19:23','2023-06-20 17:52:05'),
	(13,'D69B3F',379600791,0,'ru','honeydreamer','anonymous',NULL,'user',0,1,0,'2023-07-06 17:01:35','2023-06-28 17:31:29'),
	(15,'56E121',5054991166,0,'ru','Bredfried','anonymous',NULL,'user',0,1,0,'2023-07-06 17:01:35','2023-06-28 17:35:07'),
	(18,'3FEF47',1450360842,0,'ru','paulfake','anonymous',NULL,'admin',0,0,0,'2023-07-06 19:33:47','2023-07-06 18:08:13'),
	(19,'088DD5',563886330,3,'ru','anastas428','anonymous',NULL,'user',0,1,0,'2023-07-06 19:18:40','2023-07-04 14:31:38');

/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;




# Replace placeholder table for accounts_information_per_day with correct view syntax
# ------------------------------------------------------------

DROP TABLE `accounts_information_per_day`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `accounts_information_per_day`
AS SELECT
   `banks`.`id` AS `bank_id`,
   `banks`.`name` AS `bank_name`,
   `payment_accounts`.`id` AS `account_id`,
   `payment_accounts`.`account` AS `account_number`,
   `payment_accounts`.`account_limit` AS `account_limit`,
   `payment_accounts`.`account_info` AS `account_info`,coalesce(count(`deals`.`id`),0) AS `total_uses`,coalesce(sum(`deals`.`from_amount`),0) AS `total_sum`,date_format(now(),'%Y-%m-%d 00:00:00') AS `starts_time`,(select `deals`.`updated_at`
FROM `deals` where ((`deals`.`from_payment_account_id` = `payment_accounts`.`id`) and (`deals`.`status` = 'completed')) order by `deals`.`id` desc limit 0,1) AS `last_use` from ((`banks` join `payment_accounts` on((`payment_accounts`.`bank_id` = `banks`.`id`))) left join `deals` on(((`deals`.`from_payment_account_id` = `payment_accounts`.`id`) and (`deals`.`status` = 'completed') and (cast(`deals`.`created_at` as date) = curdate())))) where (`payment_accounts`.`status` = 'active') group by `payment_accounts`.`id`;


# Replace placeholder table for accounts_information_all_days with correct view syntax
# ------------------------------------------------------------

DROP TABLE `accounts_information_all_days`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `accounts_information_all_days`
AS SELECT
   `banks`.`id` AS `bank_id`,
   `banks`.`name` AS `bank_name`,
   `payment_accounts`.`id` AS `account_id`,
   `payment_accounts`.`account` AS `account_number`,
   `payment_accounts`.`account_info` AS `account_info`,
   `payment_accounts`.`account_limit` AS `account_limit`,coalesce(count(`deals`.`id`),0) AS `total_uses`,coalesce(sum(`deals`.`from_amount`),0) AS `total_sum`,(select `deals`.`updated_at`
FROM `deals` where ((`deals`.`from_payment_account_id` = `payment_accounts`.`id`) and (`deals`.`status` = 'completed')) order by `deals`.`id` desc limit 0,1) AS `last_use` from ((`banks` join `payment_accounts` on((`payment_accounts`.`bank_id` = `banks`.`id`))) left join `deals` on(((`deals`.`from_payment_account_id` = `payment_accounts`.`id`) and (`deals`.`status` = 'completed')))) where (`payment_accounts`.`status` = 'active') group by `payment_accounts`.`id`;

/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
