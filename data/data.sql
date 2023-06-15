# ************************************************************
# Sequel Pro SQL dump
# Version 5446
#
# https://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 8.0.23)
# Database: p2p_exchange_bot
# Generation Time: 2023-05-28 17:46:45 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
SET NAMES utf8mb4;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table banks
# ------------------------------------------------------------

CREATE TABLE `banks` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `country_code` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `slug` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `spread` float DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `created_at` timestamp NOT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `banks` WRITE;
/*!40000 ALTER TABLE `banks` DISABLE KEYS */;

INSERT INTO `banks` (`id`, `name`, `country_code`, `slug`, `spread`, `updated_at`, `created_at`)
VALUES
	(1,'Wise','de','WiseE',0,NULL,'2023-05-13 13:53:20'),
	(2,'AdvCash','de','Advcash',0,NULL,'2023-05-13 13:46:18'),
	(3,'Тинькофф','ru','TinkoffNew',0,NULL,'2023-04-27 02:29:49'),
	(4,'AliPay','cn','Alipay',0,NULL,'2023-04-27 02:29:49'),
	(5,'Сбербанк','ru','-',NULL,NULL,'2023-05-13 14:13:33'),
	(6,'Альфабанк','ru','-',NULL,NULL,'2023-05-13 14:15:37'),
	(8,'Райффайзенбанк','ru','-',NULL,NULL,'2023-05-16 20:36:15'),
	(10,'ERC-20','usdt','-',NULL,NULL,'2023-05-16 21:49:42'),
	(11,'BEP-20','usdt','-',NULL,NULL,'2023-05-16 21:50:06'),
	(12,'TRC-20','usdt','-',NULL,NULL,'2023-05-16 21:50:24'),
	(13,'TRC-20','trx','-',NULL,NULL,'2023-05-16 21:59:39'),
	(14,'BEP-20','trx','-',NULL,NULL,'2023-05-16 22:00:14');

/*!40000 ALTER TABLE `banks` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table config
# ------------------------------------------------------------

CREATE TABLE `config` (
  `technical_break` tinyint(1) NOT NULL DEFAULT '1',
  `notifications_deal_chat_id` bigint NOT NULL,
  `notifications_support_chat_id` bigint NOT NULL,
  `updated_at` timestamp NOT NULL ON UPDATE CURRENT_TIMESTAMP,
  `created_at` timestamp NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `config` WRITE;
/*!40000 ALTER TABLE `config` DISABLE KEYS */;

INSERT INTO `config` (`technical_break`, `notifications_deal_chat_id`, `notifications_support_chat_id`, `updated_at`, `created_at`)
VALUES
	(0,-947509265,-1001460302084,'2023-05-28 20:45:34','2023-04-25 09:15:21');

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
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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
  `manager_id` int NOT NULL DEFAULT '0',
  `user_id` int NOT NULL,
  `from_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `from_amount` float NOT NULL,
  `from_bank_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'Bank',
  `to_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `to_amount` float NOT NULL,
  `orig_to_amount` float NOT NULL,
  `to_bank_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `requisites` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `exchange_rate` float NOT NULL,
  `orig_exchange_rate` float NOT NULL,
  `spread` float NOT NULL DEFAULT '0',
  `profit` float DEFAULT '0',
  `calculated_amount` float NOT NULL,
  `status` enum('new','accepted','process','paid','dispute','completed','declined') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'new',
  `expires` float NOT NULL DEFAULT '15',
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `created_at` timestamp NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `deals` WRITE;
/*!40000 ALTER TABLE `deals` DISABLE KEYS */;

INSERT INTO `deals` (`id`, `manager_id`, `user_id`, `from_name`, `from_amount`, `from_bank_name`, `to_name`, `to_amount`, `orig_to_amount`, `to_bank_name`, `requisites`, `exchange_rate`, `orig_exchange_rate`, `spread`, `profit`, `calculated_amount`, `status`, `expires`, `updated_at`, `created_at`)
VALUES
	(1,1,2,'RUB',1000,'Тинькофф','EUR',12.66,0,'Advcash','12094 9128438 012929',75,0,0,NULL,1,'completed',15,'2023-05-08 13:59:58','2023-05-08 13:40:51'),
	(2,1,6,'RUB',2000,'Тинькофф','EUR',25.35,0,'Wise','38381914',76.6,0,0,NULL,1,'completed',15,'2023-05-08 14:59:52','2023-05-08 14:56:16'),
	(3,1,6,'RUB',1000,'Тинькофф','EUR',12.64,0,'Advcash','828392923',75.95,0,0,NULL,1,'declined',15,'2023-05-08 18:26:00','2023-05-08 16:10:52'),
	(4,1,6,'RUB',1200,'Тинькофф','EUR',15.16,0,'Wise','910203047',76.83,0,0,NULL,1,'declined',15,'2023-05-08 16:51:57','2023-05-08 16:49:12'),
	(5,1,2,'RUB',1500,'Тинькофф','EUR',18.96,0,'Wise','381028',76.81,0,0,NULL,1,'completed',15,'2023-05-08 16:54:15','2023-05-08 16:52:23'),
	(6,1,6,'RUB',6666,'Тинькофф','EUR',83.87,0,'Wise','666 ddd 9999',77.17,0,0,NULL,1,'completed',15,'2023-05-08 23:07:34','2023-05-08 20:43:58'),
	(7,1,6,'RUB',6666,'Тинькофф','EUR',83.79,0,'Wise','444 666 999',77.25,0,0,NULL,1,'completed',15,'2023-05-09 01:46:57','2023-05-08 20:49:19'),
	(8,1,6,'RUB',6666,'Тинькофф','EUR',83.81,0,'Wise','Bbbbbbbbb',77.23,0,0,NULL,1,'completed',15,'2023-05-09 00:37:11','2023-05-08 20:58:51'),
	(9,1,1,'RUB',1111,'Тинькофф','EUR',13.91,0,'Advcash','124124112',71.59,0,0,NULL,1,'completed',15,'2023-05-09 07:55:36','2023-05-09 07:34:47'),
	(10,1,6,'RUB',1000,'Тинькофф','EUR',12.51,0,'Wise','Twowodncie',77.62,0,0,NULL,1,'completed',15,'2023-05-09 07:46:21','2023-05-09 07:45:02'),
	(11,1,6,'RUB',1000,'Тинькофф','EUR',12.52,0,'Wise','4276550100374',77.57,0,0,NULL,1,'completed',15,'2023-05-09 07:55:32','2023-05-09 07:48:15'),
	(12,1,2,'RUB',1000,'Wise','USDT',12.54,0,'Тинькофф','124902',0,0,0,NULL,1,'declined',15,'2023-05-09 11:34:09','2023-05-09 10:02:12'),
	(13,3,6,'RUB',1800,'Тинькофф','EUR',22.65,0,'Wise','666666',77.3,0,0,NULL,1,'declined',15,'2023-05-09 19:37:08','2023-05-09 11:55:45'),
	(14,1,3,'RUB',15000,'Тинькофф','EUR',188.75,0,'Wise','1337228161',77.3,0,0,NULL,1,'declined',15,'2023-05-11 21:54:08','2023-05-09 12:04:06'),
	(15,1,6,'RUB',12121,'Тинькофф','EUR',152.72,0,'Wise','1e12e12e1e12',77.2,0,0,NULL,1,'completed',15,'2023-05-09 19:33:23','2023-05-09 19:30:53'),
	(16,1,6,'EUR',1000,'Тинькофф','RUB',917.43,0,'Advcash','10299412-12',6005.54,0,0,NULL,1,'declined',15,'2023-05-09 20:00:26','2023-05-09 19:41:04'),
	(17,1,6,'RUB',1250,'Тинькофф','EUR',15.83,0,'Advcash','6666777',80.66,0,0,NULL,1,'declined',15,'2023-05-09 23:57:49','2023-05-09 23:46:16'),
	(18,0,1,'AED',100,'Advcash','RUB',2038,2038,'Тинькофф','12pep12d',20.38,20.38,0,0,1,'declined',15,'2023-05-12 07:57:17','2023-05-11 23:34:59'),
	(19,0,1,'RUB',1000,'Тинькофф','EUR',10.726,10.5119,'Wise','1001024',93.227,95.13,2,0.214069,1,'declined',15,'2023-05-12 07:57:27','2023-05-11 23:39:23'),
	(20,0,1,'RUB',1000,'Тинькофф','EUR',10.726,10.5119,'Wise','1241241',93.227,95.13,2,0.214069,1,'declined',15,'2023-05-12 07:57:24','2023-05-11 23:44:43'),
	(21,0,1,'EUR',100,'Wise','RUB',6935.46,7077,'Тинькофф','12414124',69.355,70.77,2,-141.54,1,'declined',15,'2023-05-12 07:57:30','2023-05-11 23:47:31'),
	(22,0,1,'AED',100,'Advcash','RUB',1997.24,2038,'Тинькофф','129412',19.972,20.38,2,40.76,1,'declined',15,'2023-05-12 07:57:20','2023-05-11 23:51:12'),
	(23,0,1,'RUB',1000,'Advcash','AED',44.482,43.592,'Тинькофф','12041249',22.481,22.94,2,-0.890021,1,'declined',15,'2023-05-12 12:37:14','2023-05-12 09:51:00'),
	(24,0,1,'RUB',1000,'Wise','AED',44.501,43.611,'Тинькофф','124912491',22.471,22.93,2,-0.89001,1,'declined',15,'2023-05-12 12:52:38','2023-05-12 10:02:31'),
	(25,0,1,'EUR',100,'Wise','RUB',6880.58,7021,'Тинькофф','02305012',68.806,70.21,2,140.42,1,'declined',15,'2023-05-12 10:33:15','2023-05-12 10:33:08'),
	(26,1,7,'RUB',100,'Тинькофф','EUR',1.06,1.05977,'Wise','82928347272',94.36,94.36,0,-0.000228911,1,'declined',15,'2023-05-12 11:12:12','2023-05-12 11:09:04'),
	(27,0,7,'RUB',100,'Тинькофф','EUR',1.06,1.05977,'Advcash','Пррррррр',94.36,94.36,0,-0.000228911,1,'declined',15,'2023-05-12 11:28:05','2023-05-12 11:27:27'),
	(28,1,7,'RUB',10000,'Advcash','AED',445.983,437.063,'Тинькофф','4276550100766313',22.422,22.88,2,-8.92006,1,'completed',15,'2023-05-12 13:07:01','2023-05-12 13:06:02'),
	(29,1,6,'RUB',1000,'Advcash','AED',44.598,43.7063,'Тинькофф','Dwispxpfld',22.422,22.88,2,-0.891706,1,'declined',15,'2023-05-12 13:28:49','2023-05-12 13:08:10'),
	(30,1,1,'AED',100,'Wise','RUB',1983.52,2024,'Тинькофф','124192491',19.835,20.24,2,40.48,1,'declined',15,'2023-05-12 14:02:17','2023-05-12 13:46:41'),
	(31,1,2,'RUB',100,'Advcash','AED',4.402,4.31406,'Тинькофф','1401024',22.716,23.18,2,-0.0879362,1,'declined',15,'2023-05-12 16:43:38','2023-05-12 16:36:58'),
	(32,1,1,'RUB',100,'Тинькофф','EUR',1.156,1.04047,'Wise','1204194912',86.499,96.11,10,-0.115526,1,'declined',15,'2023-05-12 19:18:20','2023-05-12 18:58:01'),
	(33,1,8,'RUB',10000,'Тинькофф','EUR',115.404,103.864,'Wise','1111222233334444',86.652,96.28,10,-11.5403,1,'completed',15,'2023-05-12 20:27:41','2023-05-12 20:24:39'),
	(34,1,9,'EUR',10000,'Wise','RUB',703150,717500,'Тинькофф','+78653212456',70.315,71.75,2,14350,1,'completed',15,'2023-05-12 20:48:42','2023-05-12 20:46:09'),
	(35,0,1,'AED',1000,'Advcash','RUB',20384,20800,'Тинькофф','12491924',20.384,20.8,2,416,1,'declined',15,'2023-05-13 10:00:07','2023-05-12 22:05:27'),
	(36,1,2,'RUB',100000,'Тинькофф','EUR',1150.1,1035.09,'Advcash','Jjjnnnn',86.949,96.61,10,-115.009,1,'declined',15,'2023-05-12 22:55:29','2023-05-12 22:40:10'),
	(37,1,1,'RUB',10000,'Альфабанк','EUR',115.189,103.67,'AdvCash','124912941924',86.814,96.46,10,-11.5191,1,'declined',15,'2023-05-13 14:48:29','2023-05-13 14:16:08'),
	(38,1,1,'EUR',200,'AdvCash','AED',0,0,'AE Bank','Jsissowoeoeoeoe',0,0,0,0,1,'declined',15,'2023-05-14 13:17:16','2023-05-14 12:34:42'),
	(39,0,1,'USD',1000,'AdvCash','CNY',6377.49,6480,'AliPay','129419249129',6.377,6.48,1.582,102.514,1,'declined',15,'2023-05-15 23:13:51','2023-05-15 23:11:33'),
	(40,1,10,'USD',1488,'Wise','CNY',9489.7,9642.24,'AliPay','28383726173',6.377,6.48,1.582,152.54,1,'declined',15,'2023-05-15 23:14:54','2023-05-15 23:12:46'),
	(41,0,1,'AED',1000,'Wise','RUB',20560.4,20980,'Сбербанк','12031239012309',20.56,20.98,2,419.6,1,'declined',15,'2023-05-16 01:09:31','2023-05-16 01:09:26'),
	(42,1,2,'RUB',1000,'Тинькофф','EUR',11.372,10.2344,'AdvCash','12192491',87.939,97.71,10,-1.13763,1,'declined',15,'2023-05-16 15:29:49','2023-05-16 15:16:39'),
	(43,1,6,'RUB',1000,'Тинькофф','EUR',11.368,10.2312,'AdvCash','8382837373',87.966,97.74,10,-1.13677,1,'completed',15,'2023-05-16 16:01:18','2023-05-16 15:18:37'),
	(44,1,1,'RUB',1000,'Тинькофф','EUR',11.369,10.2323,'Wise','12489128918294',87.957,97.73,10,-1.13673,1,'declined',15,'2023-05-16 16:56:46','2023-05-16 15:36:15'),
	(45,4,4,'RUB',150,'Тинькофф','EUR',1.698,1.52796,'Wise','0000000000000000',88.353,98.17,10,-0.170038,1,'accepted',15,'2023-05-16 22:11:01','2023-05-16 22:10:06'),
	(46,3,3,'RUB',5000,'Сбербанк','TRX',895.48,886.525,'TRC-20','1234123412341234',5.584,5.64,1,-8.95518,1,'completed',15,'2023-05-18 16:00:17','2023-05-18 15:38:31'),
	(47,1,1,'RUB',1000,'Альфабанк','EUR',11.469,10.322,'AdvCash','Влвдала',87.192,96.88,10,-1.14695,1,'declined',15,'2023-05-18 15:58:54','2023-05-18 15:43:30'),
	(48,3,11,'RUB',6000,'Райффайзенбанк','TRX',1074.58,1063.83,'TRC-20','1234123412341234',5.584,5.64,1,-10.7462,1,'completed',15,'2023-05-18 15:46:12','2023-05-18 15:43:50'),
	(49,1,1,'RUB',5000,'Райффайзенбанк','USDT',57.687,57.1102,'TRC-20','194901241',86.674,87.55,1,-0.576777,1,'completed',15,'2023-05-18 15:53:59','2023-05-18 15:52:58'),
	(50,3,3,'RUB',5000,'Сбербанк','TRX',897.07,888.099,'TRC-20','12341234123412',5.574,5.63,1,-8.97053,1,'completed',15,'2023-05-18 16:05:45','2023-05-18 16:04:37'),
	(51,3,4,'RUB',5000,'Сбербанк','USDT',57.74,57.1625,'TRC-20','TUQqmPCTHdf37xRdgqFmTjoNvU38eKJJAQ',86.595,87.47,1,-0.577544,1,'completed',15,'2023-05-18 16:40:58','2023-05-18 16:25:27'),
	(52,3,3,'RUB',5000,'Сбербанк','USDT',57.648,57.0711,'BEP-20','sdfhdfhadhf',86.734,87.61,1,-0.576889,1,'declined',15,'2023-05-18 18:07:15','2023-05-18 17:51:06');

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
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `dialogs` WRITE;
/*!40000 ALTER TABLE `dialogs` DISABLE KEYS */;

INSERT INTO `dialogs` (`id`, `user_id`, `deal_id`, `type`, `status`, `title`, `updated_at`, `created_at`)
VALUES
	(1,1,0,'support','answered','214','2023-05-16 01:19:07','2023-05-06 11:31:24'),
	(2,1,0,'support','answered','214','2023-05-18 09:14:44','2023-05-06 11:40:21'),
	(3,1,0,'support','answered','214','2023-05-18 16:03:24','2023-05-06 11:41:14'),
	(4,1,0,'support','answered','214','2023-05-18 16:03:00','2023-05-06 11:42:06'),
	(5,1,0,'support','answered','214','2023-05-18 16:03:37','2023-05-06 11:43:05'),
	(6,1,0,'support','answered','214','2023-05-18 16:03:15','2023-05-06 15:33:59'),
	(7,2,0,'support','answered','214','2023-05-28 19:43:08','2023-05-07 00:36:55'),
	(8,2,0,'deal','open','📋 Сделка №26','2023-05-08 11:06:31','2023-05-08 11:03:18'),
	(9,2,26,'deal','open','📋 Сделка №26','2023-05-08 11:06:31','2023-05-08 11:06:10'),
	(10,2,26,'deal','open','📋 Сделка №26',NULL,'2023-05-08 11:07:08'),
	(11,2,27,'deal','open','📋 Сделка №27',NULL,'2023-05-08 11:38:39'),
	(12,2,1,'deal','open','📋 Сделка №1',NULL,'2023-05-08 13:41:04'),
	(13,6,2,'deal','open','📋 Сделка №2',NULL,'2023-05-08 14:57:54'),
	(14,2,0,'support','answered','Проблемы со сделкой','2023-05-18 16:47:49','2023-05-08 15:51:06'),
	(15,6,3,'deal','open','📋 Сделка №3',NULL,'2023-05-08 16:10:59'),
	(16,6,4,'deal','open','📋 Сделка №4',NULL,'2023-05-08 16:49:21'),
	(17,2,5,'deal','open','📋 Сделка №5',NULL,'2023-05-08 16:52:50'),
	(18,6,6,'deal','open','📋 Сделка №6',NULL,'2023-05-08 23:05:20'),
	(19,6,7,'deal','open','📋 Сделка №7',NULL,'2023-05-08 23:12:47'),
	(20,6,8,'deal','open','📋 Сделка №8',NULL,'2023-05-08 23:29:41'),
	(21,1,9,'deal','open','📋 Сделка №9',NULL,'2023-05-09 07:34:53'),
	(22,6,10,'deal','open','📋 Сделка №10',NULL,'2023-05-09 07:45:12'),
	(23,6,11,'deal','open','📋 Сделка №11',NULL,'2023-05-09 07:48:23'),
	(24,2,12,'deal','open','📋 Сделка №12',NULL,'2023-05-09 10:02:28'),
	(25,6,13,'deal','open','📋 Сделка №13',NULL,'2023-05-09 11:57:34'),
	(26,3,14,'deal','open','📋 Сделка №14',NULL,'2023-05-09 12:04:12'),
	(27,1,0,'support','answered','Проблемы со сделкой','2023-05-17 10:38:30','2023-05-09 12:06:08'),
	(28,3,14,'deal','open','📋 Сделка №14',NULL,'2023-05-09 14:30:21'),
	(29,6,15,'deal','open','📋 Сделка №15',NULL,'2023-05-09 19:31:00'),
	(30,6,16,'deal','open','📋 Сделка №16',NULL,'2023-05-09 19:41:17'),
	(31,6,17,'deal','open','📋 Сделка №17',NULL,'2023-05-09 23:46:24'),
	(32,1,0,'support','answered','Проблемы со сделкой','2023-05-13 11:34:46','2023-05-12 10:46:01'),
	(33,1,0,'support','answered','Проблемы со сделкой','2023-05-16 21:28:18','2023-05-12 10:46:44'),
	(34,7,26,'deal','open','📋 Сделка №26',NULL,'2023-05-12 11:09:15'),
	(35,7,0,'support','answered','Сотрудничество','2023-05-28 19:43:01','2023-05-12 11:25:26'),
	(36,7,28,'deal','open','📋 Сделка №28',NULL,'2023-05-12 13:06:11'),
	(37,6,29,'deal','open','📋 Сделка №29',NULL,'2023-05-12 13:08:33'),
	(38,1,30,'deal','open','📋 Сделка №30',NULL,'2023-05-12 13:46:47'),
	(39,2,31,'deal','open','📋 Сделка №31',NULL,'2023-05-12 16:37:07'),
	(40,1,32,'deal','open','📋 Сделка №32',NULL,'2023-05-12 19:02:22'),
	(41,8,33,'deal','open','📋 Сделка №33',NULL,'2023-05-12 20:25:14'),
	(42,9,34,'deal','open','📋 Сделка №34',NULL,'2023-05-12 20:46:41'),
	(43,9,0,'support','answered','Идея','2023-05-13 11:34:38','2023-05-12 20:50:19'),
	(44,2,36,'deal','open','📋 Сделка №36',NULL,'2023-05-12 22:40:18'),
	(45,9,0,'support','answered','Сотрудничество','2023-05-13 11:24:16','2023-05-13 11:12:13'),
	(46,1,37,'deal','open','📋 Сделка №37',NULL,'2023-05-13 14:16:15'),
	(47,1,0,'support','answered','Идея','2023-05-15 13:40:39','2023-05-13 15:46:24'),
	(48,1,38,'deal','open','📋 Сделка №38',NULL,'2023-05-14 12:34:47'),
	(49,10,40,'deal','open','📋 Сделка №40',NULL,'2023-05-15 23:13:20'),
	(50,1,0,'support','answered','Проблемы со сделкой','2023-05-16 01:19:00','2023-05-16 00:38:35'),
	(51,6,43,'deal','open','📋 Сделка №43',NULL,'2023-05-16 15:18:53'),
	(52,2,42,'deal','open','📋 Сделка №42',NULL,'2023-05-16 15:29:02'),
	(53,1,44,'deal','open','📋 Сделка №44',NULL,'2023-05-16 16:54:52'),
	(54,4,45,'deal','open','📋 Сделка №45',NULL,'2023-05-16 22:11:02'),
	(55,3,46,'deal','open','📋 Сделка №46',NULL,'2023-05-18 15:38:54'),
	(56,1,47,'deal','open','📋 Сделка №47',NULL,'2023-05-18 15:43:39'),
	(57,11,48,'deal','open','📋 Сделка №48',NULL,'2023-05-18 15:44:11'),
	(58,1,49,'deal','open','📋 Сделка №49',NULL,'2023-05-18 15:53:09'),
	(59,3,50,'deal','open','📋 Сделка №50',NULL,'2023-05-18 16:04:46'),
	(60,4,51,'deal','open','📋 Сделка №51',NULL,'2023-05-18 16:25:52'),
	(61,3,52,'deal','open','📋 Сделка №52',NULL,'2023-05-18 17:51:53'),
	(62,1,0,'support','open','Проблемы со сделкой',NULL,'2023-05-28 20:45:45');

/*!40000 ALTER TABLE `dialogs` ENABLE KEYS */;
UNLOCK TABLES;


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
) ENGINE=InnoDB AUTO_INCREMENT=106 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;

INSERT INTO `messages` (`id`, `user_id`, `dialog_id`, `text`, `attach`, `content_type`, `updated_at`, `created_at`)
VALUES
	(1,2,12,'Скриншот оплаты','{\"data\": \"AgACAgIAAxkBAAIPlGRY0dMl7WX-tjGSs07vBY-vwQABkQACBssxG7rNwErnbKX32BwEZQEAAwIAA3gAAy8E\"}','photo',NULL,'2023-05-08 13:41:25'),
	(2,6,13,'Оплатил сберкотом11','{\"data\": \"AgACAgIAAxkBAAIPqWRY5AABMHblKjDEUBtqNadTujE_YAACdMYxGwABxslKkQbCWVUfh-MBAAMCAAN5AAMvBA\"}','photo','2023-05-18 16:10:55','2023-05-08 14:58:58'),
	(3,2,14,'Здарова отец12412424','{}','text','2023-05-18 16:42:10','2023-05-08 15:51:06'),
	(4,6,18,'ТАК Я ОПЛАТИЛ!!!!!!!!!! ГДЕ ДЕНЬГИ','{\"data\": \"AgACAgIAAxkBAAIQB2RZVmPMer2Y2-tcbcwCeZC763syAAImxjEbAAHG0UpTSl0-X6CbiQEAAwIAA3kAAy8E\"}','text',NULL,'2023-05-08 23:07:01'),
	(5,6,20,'121921','{\"data\": \"AgACAgIAAxkBAAIQF2RZW8gtbbd9zLWNvHAIU6_p3i0CAAImxjEbAAHG0UpTSl0-X6CbiQEAAwIAA3kAAy8E\"}','text',NULL,'2023-05-08 23:30:03'),
	(6,1,21,'контент тайп не указал боже мой да што же такое','{\"data\": \"AgACAgIAAxkBAAIQNGRZz1uJljX0SPcAAS3vxgw1rLytKQACJsgxG7fu0Urn2hCV0rlnMAEAAwIAA3kAAy8E\"}','photo',NULL,'2023-05-09 07:43:10'),
	(7,6,22,'Вот деньги','{\"data\": \"AgACAgIAAxkBAAIQSGRZ0Abbi5jtcxK4bJJSdwGxIpoBAALfxjEbAAHG0Uqil6emYV3skgEAAwIAA3kAAy8E\"}','photo',NULL,'2023-05-09 07:46:00'),
	(8,2,24,'Empty','{\"data\": \"AgACAgIAAxkBAAIQjWRZ8A7yhzFcXniyWHSsVh0p5l9oAAI8xzEbus3QSkpeyo6GtKPbAQADAgADbQADLwQ\"}','photo',NULL,'2023-05-09 10:02:40'),
	(9,6,25,'Оплатил!','{\"data\": \"AgACAgIAAxkBAAIQtWRaCyfWXN92HXs_T2vWfoXqLuxVAAIYyDEbAAHG0UpTRhGGS8TgaQEAAwIAA3kAAy8E\"}','photo',NULL,'2023-05-09 11:58:17'),
	(10,1,27,'Вдыхфхв','{}','text',NULL,'2023-05-09 12:06:08'),
	(11,6,25,'йзцщщв1201у1','{\"data\": \"AgACAgIAAxkBAAIRIGRaTCqk4XeXtL9u7_JbHNk3rMzaAAISyTEbAAHG2UqzDmZRbVGgLQEAAwIAA3gAAy8E\"}','photo',NULL,'2023-05-09 16:36:06'),
	(12,6,25,'шоэтотакое????????','{\"data\": \"AgACAgIAAxkBAAIRKGRaTGsUi5cKu_UkfhCy0vWrpjVEAAIVyTEbAAHG2UpDqDAIm0Ro9QEAAwIAA3gAAy8E\"}','photo',NULL,'2023-05-09 16:36:45'),
	(13,6,25,'120412dqopw','{\"data\": \"AgACAgIAAxkBAAIRMGRaTaEWsTi6pCb3xLMlawx1TvN_AAIayTEbAAHG2UpBq0h3EdBJ1QEAAwIAA3gAAy8E\"}','photo',NULL,'2023-05-09 16:41:56'),
	(14,1,25,'тест','{}','text',NULL,'2023-05-09 18:01:41'),
	(15,1,25,'текстqwd','{}','text',NULL,'2023-05-09 18:04:58'),
	(16,1,25,'qwd','{}','text',NULL,'2023-05-09 18:05:11'),
	(17,1,25,'124124','{}','text',NULL,'2023-05-09 18:05:50'),
	(18,1,25,'qwdqwdqw','{}','text',NULL,'2023-05-09 18:06:12'),
	(19,1,25,'qwdqdw','{}','text',NULL,'2023-05-09 18:06:40'),
	(20,1,25,'qwdq','{}','text',NULL,'2023-05-09 18:07:27'),
	(21,1,25,'12414','{}','text',NULL,'2023-05-09 18:14:33'),
	(22,1,25,'qwdq','{}','text',NULL,'2023-05-09 18:14:53'),
	(23,1,25,'qqwdqw','{}','text',NULL,'2023-05-09 18:15:24'),
	(24,1,25,'124124','{}','text',NULL,'2023-05-09 18:17:36'),
	(25,1,25,'qwdqwd','{}','text',NULL,'2023-05-09 18:24:19'),
	(26,1,25,'qwd','{}','text',NULL,'2023-05-09 18:25:51'),
	(27,1,25,'qpwdkqpowd','{}','text',NULL,'2023-05-09 18:26:10'),
	(28,1,25,'qwdpoqw','{\"data\": \"AgACAgIAAxkBAAIRZmRaZiRJkkVXwmOfmqIytTB1uvnbAAIoxzEbJpvYSpLeIQaxBmhgAQADAgADeAADLwQ\"}','photo',NULL,'2023-05-09 18:26:31'),
	(29,1,25,'qwdqwd','{}','text',NULL,'2023-05-09 18:31:07'),
	(30,1,25,'х1з2щлу1щзу-012в1','{}','text',NULL,'2023-05-09 18:37:29'),
	(31,1,25,'i love you bqpwokqopwdkqpwdo','{\"data\": \"BQACAgIAAxkBAAIRcmRaafZYgm1wmcKavQKsTde1MsG7AAJ0LAACJpvYSvt4W1okcROgLwQ\"}','document',NULL,'2023-05-09 18:42:49'),
	(32,1,25,'хйхцухйух','{}','text',NULL,'2023-05-09 18:43:48'),
	(33,1,25,'test1020412','{}','text',NULL,'2023-05-09 19:08:57'),
	(34,6,25,'12-412-040-','{}','text',NULL,'2023-05-09 19:09:12'),
	(35,1,25,'qwdp21','{}','text',NULL,'2023-05-09 19:27:18'),
	(36,6,25,'test','{}','text',NULL,'2023-05-09 19:27:37'),
	(37,1,25,'Sisisnd','{}','text',NULL,'2023-05-09 19:29:03'),
	(38,6,25,'qwdqd','{}','text',NULL,'2023-05-09 19:29:08'),
	(39,1,29,'Укажите, пожалуйста,  от кого был перевод','{}','text',NULL,'2023-05-09 19:31:43'),
	(40,6,29,'Зверев Павел Алексееви','{}','text',NULL,'2023-05-09 19:31:58'),
	(41,6,29,'Вы отправили меньше чем нужно','{}','text',NULL,'2023-05-09 19:32:27'),
	(42,1,29,'Это ваши проблемы','{}','text',NULL,'2023-05-09 19:33:20'),
	(43,6,30,'qpwod12-0d12','{}','text',NULL,'2023-05-09 19:41:45'),
	(44,1,30,'Пожалуйста, можете ещё прикрепить фото чека?','{}','text',NULL,'2023-05-09 19:42:15'),
	(45,6,30,'Конечно, держите','{\"data\": \"AgACAgIAAxkBAAIR02Rad_S0AAJnW5y6NHM3lG16iytXAAJyxTEbilLZSjJIBAw-bQ-9AQADAgADeAADLwQ\"}','photo',NULL,'2023-05-09 19:42:31'),
	(46,1,30,'ещо раз','{}','text',NULL,'2023-05-09 19:44:02'),
	(47,6,30,'ну лана на','{\"data\": \"AgACAgIAAxkBAAIR22RaeFx1LHeLtoqA89KO9RMjM9gSAAJ2xTEbilLZSqj0VnG3y2yLAQADAgADeAADLwQ\"}','photo',NULL,'2023-05-09 19:44:16'),
	(48,1,30,'po12ke','{}','text',NULL,'2023-05-09 19:49:40'),
	(49,6,30,'qwdpoqkw','{}','text',NULL,'2023-05-09 19:51:36'),
	(50,1,30,'У вас всё ок?','{}','text',NULL,'2023-05-09 19:52:38'),
	(51,6,30,'нет ты чё мыш','{}','text',NULL,'2023-05-09 19:52:51'),
	(52,6,30,'ГДЕ МОИ ДЕНГИ???ГДЕ МОИ ДЕНГИ???ГДЕ МОИ ДЕНГИ???ГДЕ МОИ ДЕНГИ???','{}','text',NULL,'2023-05-09 19:53:04'),
	(53,1,30,'Что у тебя случилось','{}','text',NULL,'2023-05-09 20:00:10'),
	(54,6,30,'хз','{}','text',NULL,'2023-05-09 20:00:21'),
	(55,1,31,'Здравсвуйте! Прикрепите скриншот оплаты.','{}','text',NULL,'2023-05-09 23:47:03'),
	(56,6,31,'Вот вам скринкот…','{\"data\": \"AgACAgIAAxkBAAISL2RasV7iSiFZgxfkzthbtGtRqBEAA1PHMRuKUtlKiT2gCBrCZhoBAAMCAAN5AAMvBA\"}','photo',NULL,'2023-05-09 23:47:28'),
	(57,6,31,'Кот недоволен…','{\"data\": \"AgACAgIAAxkBAAISNWRasgHii_YmPkbfab5cHd3CeH7zAAJUxzEbilLZSgQBJEa7rJWBAQADAgADeQADLwQ\"}','photo',NULL,'2023-05-09 23:50:11'),
	(58,6,31,'Оры','{}','text',NULL,'2023-05-09 23:57:17'),
	(59,1,31,'lkpaocqpwcq','{}','text',NULL,'2023-05-09 23:57:34'),
	(60,1,12,'привет! как сделка?','{}','text',NULL,'2023-05-12 07:58:19'),
	(61,2,12,'приве! +- не очень','{}','text',NULL,'2023-05-12 07:58:37'),
	(62,1,33,'1241212o4p1','{}','text',NULL,'2023-05-12 10:46:44'),
	(63,7,9,'Test','{\"data\": \"AgACAgIAAxkBAAIc_mRd9DxOaZwSVP9p4_0UmnwKGJoVAAJCwzEbuODwShk0r5eNuszAAQADAgADeQADLwQ\"}','photo',NULL,'2023-05-12 11:09:34'),
	(64,1,9,'Здравствуйте! Укажите имя получателя.','{}','text',NULL,'2023-05-12 11:11:27'),
	(65,7,9,'Имя получателя: Вививив','{}','text',NULL,'2023-05-12 11:11:39'),
	(66,7,5,'Влвщащаьаь','{\"data\": \"AgACAgIAAxkBAAIdC2Rd9NGOICNPzna8S-tmkX4d1KqpAAJCwzEbuODwShk0r5eNuszAAQADAgADeQADLwQ\"}','photo','2023-05-12 11:22:59','2023-05-12 11:12:04'),
	(67,7,35,'Привет, у меня есть 5 рублей','{}','text',NULL,'2023-05-12 11:25:26'),
	(68,1,11,'сорри но мы сливаем тебя','{}','text',NULL,'2023-05-12 11:28:29'),
	(69,1,11,'виталя','{\"data\": \"AgACAgIAAxkBAAIdM2Rd-LnFOt8dvJu1wozIgCrJifxLAAK-xDEbxT7xSppH1ilRXA9TAQADAgADbQADLwQ\"}','photo',NULL,'2023-05-12 11:28:43'),
	(70,7,36,'Чек','{\"data\": \"AgACAgIAAxkBAAIdUWReD7H8LjO5yTFYzNLd9a_a7RT-AALKwzEbuODwSqPZw0n_VGl7AQADAgADeQADLwQ\"}','photo',NULL,'2023-05-12 13:06:43'),
	(71,1,41,'прости но я тебя скаманул лол','{}','text',NULL,'2023-05-12 20:26:55'),
	(72,1,42,'ты гей','{}','text',NULL,'2023-05-12 20:47:52'),
	(73,1,42,'а ещё писька\n\nспасибо тебе огромное!','{}','text',NULL,'2023-05-12 20:48:30'),
	(74,9,42,'С вас 200 гривен','{}','text',NULL,'2023-05-12 20:49:02'),
	(75,9,43,'С вас еще 200 гривен','{}','text',NULL,'2023-05-12 20:50:19'),
	(76,1,43,'pqwkdpqowkd','{}','text',NULL,'2023-05-13 11:10:49'),
	(77,1,43,'qwopdkqopwdk','{}','text',NULL,'2023-05-13 11:11:26'),
	(78,9,45,'Сам ты qwopdkqopwdk','{}','text',NULL,'2023-05-13 11:12:13'),
	(79,1,43,'вот тебе!!!','{\"data\": \"AgACAgIAAxkBAAIfJ2RfRmWz_SIZQce9IKBN5YL3kzMtAAJ9xzEbxT75ShcrbvGeJAFnAQADAgADeAADLwQ\"}','photo',NULL,'2023-05-13 11:12:24'),
	(80,1,45,':cc','{}','text',NULL,'2023-05-13 11:12:41'),
	(81,1,27,'192491','{\"data\": \"AgACAgIAAxkBAAIfM2RfRruU_QfhVMj_Z7Q_ia2pXRCuAAJ9xzEbxT75ShcrbvGeJAFnAQADAgADeAADLwQ\"}','photo',NULL,'2023-05-13 11:13:49'),
	(82,1,46,'хей','{}','text',NULL,'2023-05-13 14:16:21'),
	(83,1,46,'test','{\"data\": \"AgACAgIAAxkBAAIfoWRfcZJIIgpO_gZQz-uv7J6Te3xaAAKYyDEbxT75SmhMrAcq5Z7QAQADAgADeAADLwQ\"}','photo',NULL,'2023-05-13 14:16:44'),
	(84,1,47,'Ошьдязвзв','{}','text',NULL,'2023-05-13 15:46:24'),
	(85,1,47,'Плахой мальчек','{}','text',NULL,'2023-05-13 15:47:15'),
	(86,1,36,'але брат ты че там','{}','text',NULL,'2023-05-15 14:00:18'),
	(87,7,36,'Я сплю(','{}','text',NULL,'2023-05-15 14:00:41'),
	(88,1,49,'Мда','{}','text',NULL,'2023-05-15 23:15:01'),
	(89,10,49,'Empty','{\"data\": \"AgACAgIAAxkBAAIgJWRikwABkIYInDlNlmCtiq4wWZhyTQACQsgxG4FfGEt_KtA-8f4StgEAAwIAA3gAAy8E\"}','photo',NULL,'2023-05-15 23:16:02'),
	(90,1,50,'йцвзщйцлвзщйлц','{}','text',NULL,'2023-05-16 00:38:35'),
	(91,6,51,'Я оплатил, вот чек','{\"data\": \"AgACAgIAAxkBAAIgv2RjdXScSKvQTNGSO4XLl-ipSkQgAAIyyTEb5hogS771WPYsdBZ4AQADAgADeQADLwQ\"}','photo',NULL,'2023-05-16 15:22:18'),
	(92,1,51,'qwoidqowi oiqwoidqwoi','{}','text',NULL,'2023-05-16 15:23:17'),
	(93,6,51,'Быдыдвьм','{\"data\": \"AgACAgIAAxkBAAIgzWRjdet3DjLcBD0dVTBDEGbtjwIOAAKhxjEb-Z8ZSyAzEq4bhFD2AQADAgADeQADLwQ\"}','photo',NULL,'2023-05-16 15:24:14'),
	(94,3,57,'Пришлите скриншот','{}','text',NULL,'2023-05-18 15:45:18'),
	(95,11,57,'Empty','{\"data\": \"AgACAgIAAxkBAAIkemRmHfUHygUL-vsm4otRFmex8R-bAAImxzEbNDgxS_bnHW9pR00jAQADAgADeQADLwQ\"}','photo',NULL,'2023-05-18 15:45:46'),
	(96,3,55,'вава','{}','text',NULL,'2023-05-18 15:49:40'),
	(97,1,58,'test,','{\"data\": \"AgACAgIAAxkBAAIkrmRmH8x1_x219qqpER-xNtxm9vizAAIHyTEb4xwwS71UIa6AZZDWAQADAgADbQADLwQ\"}','photo',NULL,'2023-05-18 15:53:35'),
	(98,3,60,'После оплаты прикрепите чек','{}','text',NULL,'2023-05-18 16:27:47'),
	(99,4,60,'Empty','{\"data\": \"BQACAgIAAxkBAAIk_2RmKFykWQcmQpYjrawZGv427OhRAALDLwACLGUwS7bsm--G1TxaLwQ\"}','document',NULL,'2023-05-18 16:30:15'),
	(100,3,60,'Прикрепите скриншот','{}','text',NULL,'2023-05-18 16:32:16'),
	(101,4,60,'Empty','{\"data\": \"AgACAgIAAxkBAAIlC2RmKOj8Wb0o09eW_DcaCwABn2kLIAACTskxGyxlMEsfUfYoX53GjQEAAwIAA3kAAy8E\"}','photo',NULL,'2023-05-18 16:32:28'),
	(102,3,60,'Ожидается подтверждению сети, средства поступят на кошелёк в течение нескольких минут','{}','text',NULL,'2023-05-18 16:41:47'),
	(103,3,61,'dfgadsfghsdfghdg','{}','text',NULL,'2023-05-18 17:52:27'),
	(104,1,35,'hey!','{}','text',NULL,'2023-05-18 18:17:21'),
	(105,1,62,'124901294','{}','text',NULL,'2023-05-28 20:45:45');

/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table pages
# ------------------------------------------------------------

CREATE TABLE `pages` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `slug` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `page_title` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `page_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `document` json DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `created_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `pages` WRITE;
/*!40000 ALTER TABLE `pages` DISABLE KEYS */;

INSERT INTO `pages` (`id`, `user_id`, `slug`, `page_title`, `page_content`, `document`, `updated_at`, `created_at`)
VALUES
	(1,1,'faq','FAQ','❗️Этот раздел редактируется в административной панели\\.\n\nСтраницы \\-\\> Faq \\-\\> Изменить текст','null','2023-05-28 20:30:09','2023-05-01 09:41:55'),
	(2,1,'agreement','Условия предоставления сервиса','Прочтите соглашение','null','2023-05-28 20:44:11','2023-05-01 09:41:55'),
	(3,1,'admin_note','Заметки для админов/менеджеров','Бан пользователя:\n— /ban логин/@логин/телеграм айди\n\nВыдать админку:\n— /set\\_admin огин/@логин/телеграм айди','null','2023-05-28 17:37:14','2023-05-01 09:41:55');

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
  `is_active` tinyint(1) NOT NULL DEFAULT '0',
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `created_at` timestamp NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `pairs` WRITE;
/*!40000 ALTER TABLE `pairs` DISABLE KEYS */;

INSERT INTO `pairs` (`id`, `user_id`, `from_name`, `from_handler_name`, `from_country_code`, `min_from_amount`, `max_from_amount`, `from_type`, `to_name`, `to_handler_name`, `to_country_code`, `to_type`, `to_requisites_comment`, `handler_direction`, `proxy_asset`, `spread`, `price_handler`, `handler_inverted`, `is_active`, `updated_at`, `created_at`)
VALUES
	(1,0,'RUB','SBERRUB','ru',100,100000,'fiat','EUR','WISEEUR','de','fiat','-','in','USDT',10,'cryptoexchage',0,1,'2023-05-16 14:24:09','2023-04-26 11:17:27'),
	(2,0,'EUR','WISEEUR','de',100,10000,'fiat','RUB','SBERRUB','ru','fiat','-','out','USDT',2,'cryptoexchage',0,0,'2023-05-13 09:57:08','2023-04-26 11:17:27'),
	(5,0,'RUB','SBERRUB','de',100,10000,'fiat','AED','CASHAED','ru','fiat','-','in','USDT',2,'cryptoexchage',0,1,'2023-05-16 14:20:09','2023-04-26 11:17:27'),
	(14,0,'RUB','EMPTY','RU',1000,100000,'crypto','USDT','EMPTY','RU','fiat','-','EMPTY','USDT',2,'cryptoexchage',0,0,'2023-05-16 20:23:35','2023-05-16 19:17:12'),
	(15,0,'USDT','EMPTY','RU',100,10000,'fiat','CNY','EMPTY','cn','fiat','уКаЖиТе НоМеР сТрАховочки','EMPTY','USDT',1,'cryptoexchage',0,1,'2023-05-16 22:01:22','2023-05-16 19:27:52'),
	(16,0,'RUB','EMPTY','RU',10000,100000,'fiat','BTC','EMPTY','usdt','crypto','-','EMPTY','USDT',1,'cryptoexchage',0,1,'2023-05-16 20:52:07','2023-05-16 20:25:08'),
	(17,0,'RUB','SBERRUB','RU',5000,100000,'fiat','USDT','USDTTRC20','usdt','crypto','-','EMPTY','USDT',1,'cryptoexchage',0,1,'2023-05-16 21:42:34','2023-05-16 21:38:16'),
	(18,0,'RUB','TRX','ru',5000,100000,'fiat','TRX','SBERRUB','trx','crypto','-','EMPTY','USDT',1,'cryptoexchage',1,1,'2023-05-17 10:35:22','2023-05-16 22:02:02');

/*!40000 ALTER TABLE `pairs` ENABLE KEYS */;
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



# Dump of table users
# ------------------------------------------------------------

CREATE TABLE `users` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `telegram_id` bigint NOT NULL,
  `referer_id` int DEFAULT '0',
  `language_code` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'ru',
  `username` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'username_is_empty',
  `is_admin` int NOT NULL DEFAULT '0',
  `is_agreement` tinyint(1) NOT NULL DEFAULT '0',
  `is_banned` tinyint(1) NOT NULL DEFAULT '0',
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `created_at` timestamp NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;

INSERT INTO `users` (`id`, `telegram_id`, `referer_id`, `language_code`, `username`, `is_admin`, `is_agreement`, `is_banned`, `updated_at`, `created_at`)
VALUES
	(1,1450360842,0,'ru','paulfake',1,1,0,'2023-05-28 20:44:27','2023-04-25 15:05:18'),
	(2,1776127555,0,'ru','mr_x0r',0,1,0,'2023-05-09 13:35:43','2023-04-26 17:02:17'),
	(3,5698719743,0,'ru','ZergTrust',1,1,0,'2023-05-09 13:35:44','2023-04-28 11:56:54'),
	(4,37913419,0,'ru','MrGreen4you',1,1,0,'2023-05-12 10:14:05','2023-04-28 12:10:34'),
	(5,812027680,0,'ru','mrslera',1,1,0,'2023-05-12 18:50:58','2023-04-28 12:12:25'),
	(6,1620022975,0,'ru','ibatenka',1,1,0,'2023-05-16 16:00:37','2023-05-08 14:55:46'),
	(7,5343576955,0,'ru','mr_osminolog',0,1,0,'2023-05-15 13:59:43','2023-05-12 11:08:42'),
	(8,567350571,0,'ru','KirSchmunk',0,1,0,'2023-05-12 20:23:13','2023-05-12 20:22:38'),
	(9,397039103,0,'ru','arturkogut',0,1,0,'2023-05-12 20:53:44','2023-05-12 20:45:04'),
	(10,409074651,0,'ru','MiyukiMori',0,1,0,'2023-05-15 23:12:16','2023-05-15 23:12:13'),
	(11,391711549,0,'ru','Trust5001',0,1,0,'2023-05-18 15:43:24','2023-05-18 15:43:18');

/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
