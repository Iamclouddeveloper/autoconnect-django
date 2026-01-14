-- MySQL dump 10.13  Distrib 8.0.44, for Linux (x86_64)
--
-- Host: localhost    Database: autoconnect
-- ------------------------------------------------------
-- Server version	8.0.44-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_group_id_b120cbf9` (`group_id`),
  KEY `auth_group_permissions_permission_id_84c5c92e` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  KEY `auth_permission_content_type_id_2f476e4b` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',3,'add_permission'),(6,'Can change permission',3,'change_permission'),(7,'Can delete permission',3,'delete_permission'),(8,'Can view permission',3,'view_permission'),(9,'Can add group',2,'add_group'),(10,'Can change group',2,'change_group'),(11,'Can delete group',2,'delete_group'),(12,'Can view group',2,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add user',6,'add_user'),(22,'Can change user',6,'change_user'),(23,'Can delete user',6,'delete_user'),(24,'Can view user',6,'view_user'),(25,'Can add vehicle',7,'add_vehicle'),(26,'Can change vehicle',7,'change_vehicle'),(27,'Can delete vehicle',7,'delete_vehicle'),(28,'Can view vehicle',7,'view_vehicle'),(29,'Can add email queue',8,'add_emailqueue'),(30,'Can change email queue',8,'change_emailqueue'),(31,'Can delete email queue',8,'delete_emailqueue'),(32,'Can view email queue',8,'view_emailqueue'),(33,'Can add e xample',9,'add_example'),(34,'Can change e xample',9,'change_example'),(35,'Can delete e xample',9,'delete_example'),(36,'Can view e xample',9,'view_example'),(37,'Can add trip',10,'add_trip'),(38,'Can change trip',10,'change_trip'),(39,'Can delete trip',10,'delete_trip'),(40,'Can view trip',10,'view_trip');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_user_id_6a12ed8b` (`user_id`),
  KEY `auth_user_groups_group_id_97559544` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_user_id_a95ead1b` (`user_id`),
  KEY `auth_user_user_permissions_permission_id_1fbb5f2c` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_b2c_trip`
--

DROP TABLE IF EXISTS `customer_b2c_trip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer_b2c_trip` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `start` varchar(255) NOT NULL,
  `end` varchar(255) NOT NULL,
  `estimated_distance` double NOT NULL,
  `actual_distance` double DEFAULT NULL,
  `duration_text` varchar(100) NOT NULL,
  `odometer_start` double NOT NULL,
  `odometer_end` double DEFAULT NULL,
  `latest_reading` double DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `tracking_token` varchar(40) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  `vehicle_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tracking_token` (`tracking_token`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_b2c_trip`
--

LOCK TABLES `customer_b2c_trip` WRITE;
/*!40000 ALTER TABLE `customer_b2c_trip` DISABLE KEYS */;
INSERT INTO `customer_b2c_trip` VALUES (1,'London','derby',129.47,130,'2 hours 42 mins',600,730,730,0,'b1bebe2c099846318a878d0ca2b7714f','2026-01-14 11:47:16.542915',9,10),(12,'221 Baker Street, London NW1 6XE','45 High Street, Oxford OX1 4AP',71.42,68,'1 hour 18 mins',2450,2518,2518,0,'a91f4c2d8b6e4f9e9a42c6d1bfa83210','2025-11-10 09:22:11.000000',3,28),(13,'10 Downing Street, London SW1A 2AA','18 Castle Street, Windsor SL4 1PW',46.1,43,'52 mins',2518,2561,2561,0,'c3b87f9e2d1b4a4ea8c59b12d0f7a921','2025-12-10 11:47:36.000000',3,29),(14,'14 King Street, Manchester M2 6AG','27 Station Road, Bolton BL2 1AB',30.65,28,'41 mins',17890,17918,17918,0,'e4d19c7b53f741d89a7f9e0b91fa5c44','2025-10-01 08:15:09.000000',3,30),(15,'88 Queen Street, Leeds LS1 2DF','3 Park Lane, Bradford BD5 0HT',24.8,22,'33 mins',17918,17940,17940,0,'7a2e8c4bdfbc4b66a9b4f41b2a04a310','2026-01-01 10:34:52.000000',3,31),(16,'5 Mill Road, Cambridge CB1 2AB','41 Market Place, Ely CB7 4NP',22.55,21,'29 mins',9340,9361,9361,0,'fbc49d4a9c0d4c58b01c8d9986d2b123','2026-01-11 13:09:41.000000',3,28),(17,'72 George Street, Edinburgh EH2 2LR','9 High Street, Stirling FK8 1EQ',47.3,44,'48 mins',9361,9405,9405,0,'b7d5e39a4a3c4f6abf189a2c6e8f4129','2026-01-10 09:02:18.000000',3,29),(18,'16 Broad Street, Bristol BS1 2HF','33 Fore Street, Taunton TA1 1JH',64.9,62,'1 hour 6 mins',50210,50272,50272,0,'9d23af1c74c944e29c4bcb38fa4d19e6','2026-01-12 11:55:07.000000',3,30),(19,'2 Victoria Road, Reading RG1 1ES','91 London Road, Slough SL3 7RL',35.2,33,'36 mins',50272,50305,50305,0,'4f8c3d6b5a3a4fa8a921f2b8e63d10a2','2026-01-02 14:28:59.000000',3,31),(20,'19 Market Street, Nottingham NG1 6HX','7 High Street, Loughborough LE11 2PY',23.9,22,'27 mins',12860,12882,12882,0,'a0c5f2b67f1848b1b4deafdc8b29e9f4','2026-01-13 09:11:44.000000',3,28),(21,'6 North Street, York YO1 6JD','54 New Road, Harrogate HG1 1SP',44.75,42,'45 mins',12882,12924,12924,0,'d61b8e2a5f934c4bb2bafc3a9b4d771c','2026-01-13 12:46:21.000000',3,29),(23,'London','derby',129.47,NULL,'2 hours 42 mins',6784,NULL,NULL,1,'6cabd330b1294841a35250ed57ebb175','2026-01-14 13:53:35.267683',23,58);
/*!40000 ALTER TABLE `customer_b2c_trip` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(2,'auth','group'),(3,'auth','permission'),(4,'contenttypes','contenttype'),(5,'sessions','session'),(6,'customer_b2c','user'),(7,'customer_b2c','vehicle'),(8,'customer_b2c','emailqueue'),(9,'customer_b2c','example'),(10,'customer_b2c','trip');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-12-21 10:26:51.602977'),(2,'contenttypes','0002_remove_content_type_name','2025-12-21 10:26:51.631960'),(3,'auth','0001_initial','2025-12-21 10:26:51.737789'),(4,'auth','0002_alter_permission_name_max_length','2025-12-21 10:26:51.753908'),(5,'auth','0003_alter_user_email_max_length','2025-12-21 10:26:51.756900'),(6,'auth','0004_alter_user_username_opts','2025-12-21 10:26:51.759888'),(7,'auth','0005_alter_user_last_login_null','2025-12-21 10:26:51.762422'),(8,'auth','0006_require_contenttypes_0002','2025-12-21 10:26:51.762885'),(9,'auth','0007_alter_validators_add_error_messages','2025-12-21 10:26:51.765649'),(10,'auth','0008_alter_user_username_max_length','2025-12-21 10:26:51.768154'),(11,'auth','0009_alter_user_last_name_max_length','2025-12-21 10:26:51.770602'),(12,'auth','0010_alter_group_name_max_length','2025-12-21 10:26:51.787741'),(13,'auth','0011_update_proxy_permissions','2025-12-21 10:26:51.791078'),(14,'auth','0012_alter_user_first_name_max_length','2025-12-21 10:26:51.794121'),(15,'customer_b2c','0001_initial','2025-12-21 10:26:51.922867'),(16,'admin','0001_initial','2025-12-21 10:26:52.017694'),(17,'admin','0002_logentry_remove_auto_add','2025-12-21 10:26:52.021318'),(18,'admin','0003_logentry_add_action_flag_choices','2025-12-21 10:26:52.024795'),(19,'sessions','0001_initial','2025-12-21 10:26:52.045850'),(20,'customer_b2c','0002_alter_user_username','2025-12-22 03:57:02.560146'),(21,'customer_b2c','0003_user_is_blocked_user_role','2025-12-23 10:30:45.494343'),(22,'customer_b2c','0004_vehicle','2025-12-30 15:34:44.874365'),(23,'customer_b2c','0005_user_pending_email','2025-12-30 15:34:53.990002'),(24,'customer_b2c','0006_vehicle_mot_expiry_date_vehicle_mot_status_and_more','2025-12-31 05:31:02.980270'),(25,'customer_b2c','0002_trip','2026-01-14 14:38:02.791538');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('mrx2t9wbuk4bncsclfblxcv8861im9w9','.eJxVjDkOwjAUBe_iGlk2dhJ_SvqcIfqbSQDZUpYKcXeIlALaNzPvZQbc1nHYFp2HSczFgDn9boT80LIDuWO5Vcu1rPNEdlfsQRfbV9Hn9XD_DkZcxm8dcwOMTYriuuTFQYpB2nMipKCsgMwQg4dOibLDxjGn3HLIGryAz-b9AfGiOKQ:1vYe6e:d-Gd1qDkbdScxS2ffU5qwHO9praPdpaMj6HidEUm70M','2026-01-08 05:41:48.810433'),('58wkccjnhpn5sybmxe20k8mghg6kecnu','.eJxVjM0OwiAQhN-FsyH8FGE9evcZyC5spWpoUtqT8d2lSQ96mmS-b-YtIm5riVvjJU5ZXIQVp9-OMD257iA_sN5nmea6LhPJXZEHbfI2Z35dD_fvoGArfQ0j4Bl0YGOUT5ZYJzf0dNln6AlBeRq9goyMpKwLxjLCoEk7RZTE5wvomjgs:1vYeNi:VIV9hTMsj0ox7ksUpwHUE15Jn7tFGDkgOSIFh5QnMb8','2026-01-08 05:59:26.876718'),('g7fcbu9cpisljhssu8wfxlk1oy65twe4','.eJxVjM0OwiAQhN-FsyH8FGE9evcZyC5spWpoUtqT8d2lSQ96mmS-b-YtIm5riVvjJU5ZXIQVp9-OMD257iA_sN5nmea6LhPJXZEHbfI2Z35dD_fvoGArfQ0j4Bl0YGOUT5ZYJzf0dNln6AlBeRq9goyMpKwLxjLCoEk7RZTE5wvomjgs:1vbG7k:qMvQdrsppZP8FPtzpJwzARHOGVGVCpe0bQ5OrJ1HGBo','2026-01-15 10:41:44.743076'),('puen4iyuotemd0f2lftfw3xl9tcq7n8h','.eJxVjM0OwiAQhN-FsyH8FGE9evcZyC5spWpoUtqT8d2lSQ96mmS-b-YtIm5riVvjJU5ZXIQVp9-OMD257iA_sN5nmea6LhPJXZEHbfI2Z35dD_fvoGArfQ0j4Bl0YGOUT5ZYJzf0dNln6AlBeRq9goyMpKwLxjLCoEk7RZTE5wvomjgs:1vfzfe:05S0_Jy4xhTberUkFgFQAZj6cj_UaoT_R5Jj6-jOFQU','2026-01-28 12:08:18.895992'),('qad2fu9pz8mrupo0cs01gh9r5422dgzo','.eJxVjDkOwjAUBe_iGlk2dhJ_SvqcIfqbSQDZUpYKcXeIlALaNzPvZQbc1nHYFp2HSczFgDn9boT80LIDuWO5Vcu1rPNEdlfsQRfbV9Hn9XD_DkZcxm8dcwOMTYriuuTFQYpB2nMipKCsgMwQg4dOibLDxjGn3HLIGryAz-b9AfGiOKQ:1vbcIh:-gT34t4MYXpFup-cW4lNZARbh0zWAWHwCuWWYQr1ILM','2026-01-16 10:22:31.196845'),('j3a6wg9fh5d5ax87ah9473vf0mk9y20x','.eJxVjM0OwiAQhN-FsyH8FGE9evcZyC5spWpoUtqT8d2lSQ96mmS-b-YtIm5riVvjJU5ZXIQVp9-OMD257iA_sN5nmea6LhPJXZEHbfI2Z35dD_fvoGArfQ0j4Bl0YGOUT5ZYJzf0dNln6AlBeRq9goyMpKwLxjLCoEk7RZTE5wvomjgs:1vb0DN:md-oXduH2yGiaLx5iKAb0ddXcecRHmTE7rYLW9vuYmk','2026-01-14 17:42:29.191315'),('ceyp8mvlemicltfeoubberq4p8do4s2b','.eJxVjM0OwiAQhN-FsyH8FGE9evcZyC5spWpoUtqT8d2lSQ96mmS-b-YtIm5riVvjJU5ZXIQVp9-OMD257iA_sN5nmea6LhPJXZEHbfI2Z35dD_fvoGArfQ0j4Bl0YGOUT5ZYJzf0dNln6AlBeRq9goyMpKwLxjLCoEk7RZTE5wvomjgs:1vadqq:n6jAISCwx_2uedjDmAz1V1AlfSWz5VgccJieJ7ZaauE','2026-01-13 17:49:44.793421'),('5fwcqlyi4setr3f7dt9a6tudm1ys297u','eyJjYXB0Y2hhIjo4LCJjYXB0Y2hhX3EiOiIyICsgNiJ9:1vdY8Z:2CQqzCJfZ9l4AAafs0yowWxfBBj9Co6NIHCbM1Y3p0E','2026-01-21 18:20:03.504084'),('p1v72f8xaqp3k636lji5ye5ml2sdci71','.eJxVjM0OwiAQhN-FsyH8FGE9evcZyC5spWpoUtqT8d2lSQ96mmS-b-YtIm5riVvjJU5ZXIQVp9-OMD257iA_sN5nmea6LhPJXZEHbfI2Z35dD_fvoGArfQ0j4Bl0YGOUT5ZYJzf0dNln6AlBeRq9goyMpKwLxjLCoEk7RZTE5wvomjgs:1vbG8R:hsgB_PVU3SM3V-ut4vQSRAAM6XyzgOzBWegCVv6roVg','2026-01-15 10:42:27.811743'),('26jvlzjxwhghirqa4h6lok4dprcjrsqt','.eJxVjM0OwiAQhN-FsyH8FGE9evcZyC5spWpoUtqT8d2lSQ96mmS-b-YtIm5riVvjJU5ZXIQVp9-OMD257iA_sN5nmea6LhPJXZEHbfI2Z35dD_fvoGArfQ0j4Bl0YGOUT5ZYJzf0dNln6AlBeRq9goyMpKwLxjLCoEk7RZTE5wvomjgs:1vbGG5:88hkMf4MMvoq-Ri1_VLu93p3xz8BCRvLDQv2c87F3PY','2026-01-15 10:50:21.509387'),('4pftnlhd31vb9d1bgjnal92hzik240up','.eJxVjEsOgzAMRO_idRUlhBDMsvueAdmOaWgrQHxWVe9ekNiwGmnem_mC0LRKJmiqG7S0rbndFp3bPkEDHi4dk7x1OEB60fAcjYzDOvdsDsWcdDGPMennfrqXg0xL3tfYIVXoai0KG8WzOgnlniHFhHtibSN30WIiJbY-1IVXwtKxC5ZZ4PcHfio74A:1vg1V4:QstuErf55dkKJTnikcnR3n9UC-MObJiKQ6pJYPx5WyE','2026-01-28 14:05:30.616530'),('lfifoiixlxymyerjjjrd3fd6tgdapat5','.eJxVjDsOwjAQBe-yNbL8WWI7JT1niNZrGwdQEsVOhbg7REqT9s3M-wDT0rgQ9EpfYKCtlWGraR3GCD1oDacxEL_StJP4pOkxC56nto5B7Io4aBX3Oab37XBPB4Vq-dfJh077K3XGJTbKZxcVk5POUTYZs7VSSlQadWcVEktjVbLIjgMjWgnfH7FEOyU:1vfOQf:Ill4kjJ16BYpSbuPJpSncPEjTuYVunuAOZ-MLBsuvBk','2026-01-26 20:22:21.693603'),('x2f9mqv77zb84viz0yi1rr1jkm77bbo0','eyJjYXB0Y2hhIjo2LCJjYXB0Y2hhX3EiOiIxICsgNSJ9:1vdYLs:gRdXLlzWELCq3sGkemWQ2e96s5ZiobtaTG13TYorvW8','2026-01-21 18:33:48.201461'),('u5wshtn3flh4u0ujph6ctiyqo1zsqfqs','eyJjYXB0Y2hhIjozLCJjYXB0Y2hhX3EiOiIxICsgMiJ9:1vdnM0:9mEMP3pK2hRZMfGDy0-QkNlZvPbIO05KO4zqWMVFnhg','2026-01-22 10:34:56.697006'),('tlw1y06y1e6s3ua6p7thgfxudsjt5000','eyJjYXB0Y2hhIjoxMX0:1vfcD3:B0D8vhtqtG1kktxSlRZ9Iqm9o88GHMnICWBH8pYRSE4','2026-01-27 11:05:13.763418'),('lr7fg4rz69b5lwk6vwc0hotv8xt22ncw','.eJxVjDsOwjAQBe_iGlnrD4mXkj5nsHa9Ng6gRIqTCnF3iJQC2jcz76UibWuNW8tLHEVdlHXq9DsypUeediJ3mm6zTvO0LiPrXdEHbXqYJT-vh_t3UKnVb-09knMGXTFkrHjDZ0awgQEEO_CAAsUEDpZtotRJHwh6RJtKcQ5FvT_f1Ddp:1vg0Dl:Fiqzu6pHOnqBczTLDN_L3kgJyWMnpR9AnHjeMMz9vEI','2026-01-28 12:43:33.310585'),('juux8yobfhqmb349dudwsys8q3szatjy','.eJxVjLEOgzAMRP_FcxUlhDSYsXu_AdmOaWgrqCBMVf-9ILEwnXTv3X1B6FMkE7TOX6CjteRuXXTuhgQteDh1TPLScQfpSeNjMjKNZR7Y7Io56GLuU9L37XBPB5mWvK2xR7qia7SqbBTP6iTUW4YUE26JjY3cR4uJlNj60FReCWvHLlhmgd8foRE8Dg:1vfgOD:gbk4ybhZnx8qm9i6Q-BWXfUZM1tFjjyFNUmOyCS5URU','2026-01-27 15:33:01.244776');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `email_queue`
--

DROP TABLE IF EXISTS `email_queue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `email_queue` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `to_email` varchar(254) NOT NULL,
  `subject` varchar(200) NOT NULL,
  `template_name` varchar(100) NOT NULL,
  `context` json NOT NULL,
  `status` varchar(10) NOT NULL,
  `error` longtext,
  `created_at` datetime(6) NOT NULL,
  `sent_at` datetime(6) DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `email_queue`
--

LOCK TABLES `email_queue` WRITE;
/*!40000 ALTER TABLE `email_queue` DISABLE KEYS */;
INSERT INTO `email_queue` VALUES (9,'ultimateriyas1799@gmail.com','MOT Reminder – MU54GGO','vehicle_reminder_email.html','{\"vrn\": \"MU54GGO\", \"username\": \"mohamed\", \"expiry_date\": \"Jan 15, 2026\", \"reminder_type\": \"MOT\"}','sent',NULL,'2026-01-01 18:36:01.782564','2026-01-01 18:38:03.463716',1),(10,'ultimateriyas1799@gmail.com','TAX Reminder – MU54GGO','vehicle_reminder_email.html','{\"vrn\": \"MU54GGO\", \"username\": \"mohamed\", \"expiry_date\": \"Jan 03, 2026\", \"reminder_type\": \"TAX\"}','sent',NULL,'2026-01-01 18:36:01.788955','2026-01-01 18:38:04.467242',1),(11,'ultimateriyas1799@gmail.com','TAX Reminder – YE73NGV','vehicle_reminder_email.html','{\"vrn\": \"YE73NGV\", \"username\": \"mohamed\", \"expiry_date\": \"Jan 02, 2026\", \"reminder_type\": \"TAX\"}','sent',NULL,'2026-01-01 18:36:01.793636','2026-01-01 18:38:05.498897',1),(12,'shanmugavelu.pv@gmail.com','MOT Reminder – FG09GHX','vehicle_reminder_email.html','{\"vrn\": \"FG09GHX\", \"username\": \"shanmuga\", \"expiry_date\": \"Jan 15, 2026\", \"reminder_type\": \"MOT\"}','sent',NULL,'2026-01-01 18:36:01.798430','2026-01-01 18:38:07.167419',3),(13,'shanmugavelu.pv@gmail.com','MOT Reminder – FG17CFE','vehicle_reminder_email.html','{\"vrn\": \"FG17CFE\", \"username\": \"shanmuga\", \"expiry_date\": \"Jan 11, 2026\", \"reminder_type\": \"MOT\"}','sent',NULL,'2026-01-09 18:36:01.918638','2026-01-09 18:38:01.921678',3);
/*!40000 ALTER TABLE `email_queue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `temp_user_registration`
--

DROP TABLE IF EXISTS `temp_user_registration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `temp_user_registration` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(80) NOT NULL,
  `email` varchar(80) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `temp_user_registration`
--

LOCK TABLES `temp_user_registration` WRITE;
/*!40000 ALTER TABLE `temp_user_registration` DISABLE KEYS */;
/*!40000 ALTER TABLE `temp_user_registration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_registration`
--

DROP TABLE IF EXISTS `user_registration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_registration` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `username` varchar(80) NOT NULL,
  `email` varchar(80) NOT NULL,
  `password` varchar(255) NOT NULL,
  `registration_date` date NOT NULL,
  `registration_time` time(6) NOT NULL,
  `profile_photo` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_registration`
--

LOCK TABLES `user_registration` WRITE;
/*!40000 ALTER TABLE `user_registration` DISABLE KEYS */;
INSERT INTO `user_registration` VALUES (1,'riyas','mohamedriyas.py@gmail.com','pbkdf2_sha256$1200000$lwbkobenE2WvNGhOQzF4U9$Q72+1mpY4ejktfLPjqf+qO+Sl/vwy3x+l7/vx3NT4/8=','2025-12-21','10:49:24.743764',''),(2,'shanmugavelu','shanmugavelu.pv@gmail.com','pbkdf2_sha256$1200000$v5y78GF7PlCH7HWOe8c2lG$DoV6Xf2IDAPJ5QMPWLHQdDakTv7wT+CB3Kg/7QG+DPQ=','2025-12-21','10:51:19.521684','');
/*!40000 ALTER TABLE `user_registration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_tbl`
--

DROP TABLE IF EXISTS `user_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_tbl` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `username` varchar(150) NOT NULL,
  `email` varchar(191) NOT NULL,
  `profile_photo` varchar(100) DEFAULT NULL,
  `is_blocked` tinyint(1) NOT NULL,
  `role` varchar(20) NOT NULL,
  `pending_email` varchar(254) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=MyISAM AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_tbl`
--

LOCK TABLES `user_tbl` WRITE;
/*!40000 ALTER TABLE `user_tbl` DISABLE KEYS */;
INSERT INTO `user_tbl` VALUES (1,'pbkdf2_sha256$1200000$rT5KpdCjaRMW2hbz0jEgdZ$ZZWWyGDqFl0dFxzxCb48ub3BF07AuuaVn9fXJ2C43WU=','2026-01-08 16:17:30.720364',0,'','',0,1,'2025-12-21 10:27:29.440030','mohamed','ultimateriyas1799@gmail.com','',0,'user','ultimateriyas1766@gmail.com'),(9,'pbkdf2_sha256$1200000$rT5KpdCjaRMW2hbz0jEgdZ$ZZWWyGDqFl0dFxzxCb48ub3BF07AuuaVn9fXJ2C43WU=','2026-01-14 12:07:16.057857',0,'','',1,1,'2025-12-22 23:29:00.972000','riyas','mohamedriyas.py@gmail.com','',0,'sub_admin',NULL),(3,'pbkdf2_sha256$1200000$XdXgUW5OTT1oMdkseQKVq4$lQy7JFXOYY7QRFsp0l4Uw5Cgs/CZuTyVcPgSBMtmWT0=','2026-01-14 12:08:18.893253',1,'','',1,1,'2025-12-22 10:29:00.061411','shanmuga','shanmugavelu.pv@gmail.com','profile_photos/IMG_0277.png',0,'super_admin',NULL),(8,'pbkdf2_sha256$1200000$XdXgUW5OTT1oMdkseQKVq4$lQy7JFXOYY7QRFsp0l4Uw5Cgs/CZuTyVcPgSBMtmWT0=','2025-12-26 17:13:14.783527',0,'','',0,1,'2025-11-22 10:29:00.061411','mohamedriyas','mohamed.riyas@renix.co.uk','',0,'super_admin',NULL),(10,'pbkdf2_sha256$1200000$rT5KpdCjaRMW2hbz0jEgdZ$ZZWWyGDqFl0dFxzxCb48ub3BF07AuuaVn9fXJ2C43WU=','2025-12-28 09:00:44.429847',0,'Arjun','Sharma',0,1,'2025-12-28 09:00:44.429847','arjun.sharma','arjun.sharma.temp@gmail.com',NULL,0,'user',NULL),(11,'pbkdf2_sha256$1200000$rT5KpdCjaRMW2hbz0jEgdZ$ZZWWyGDqFl0dFxzxCb48ub3BF07AuuaVn9fXJ2C43WU=','2025-12-27 08:30:12.123456',0,'Mohammed','Fahad',0,1,'2025-12-27 08:30:12.123456','mohammed.fahad','mohammed.fahad.temp@gmail.com',NULL,0,'user',NULL),(12,'pbkdf2_sha256$1200000$rT5KpdCjaRMW2hbz0jEgdZ$ZZWWyGDqFl0dFxzxCb48ub3BF07AuuaVn9fXJ2C43WU=','2025-12-26 10:15:55.654321',0,'Rohit','Verma',0,1,'2025-12-26 10:15:55.654321','rohit.verma','rohit.verma.temp@gmail.com',NULL,0,'user',NULL),(13,'pbkdf2_sha256$1200000$rT5KpdCjaRMW2hbz0jEgdZ$ZZWWyGDqFl0dFxzxCb48ub3BF07AuuaVn9fXJ2C43WU=','2025-12-25 14:05:00.000111',0,'Ananya','Iyer',0,1,'2025-12-25 14:05:00.000111','ananya.iyer','ananya.iyer.temp@gmail.com',NULL,0,'user',NULL),(14,'pbkdf2_sha256$1200000$rT5KpdCjaRMW2hbz0jEgdZ$ZZWWyGDqFl0dFxzxCb48ub3BF07AuuaVn9fXJ2C43WU=','2025-12-24 18:20:45.888999',0,'Karthik','Raman',0,1,'2025-12-24 18:20:45.888999','karthik.raman','karthik.raman.temp@gmail.com',NULL,0,'user',NULL),(15,'pbkdf2_sha256$1200000$rT5KpdCjaRMW2hbz0jEgdZ$ZZWWyGDqFl0dFxzxCb48ub3BF07AuuaVn9fXJ2C43WU=','2025-12-23 11:11:11.111111',0,'Amit','Patel',0,1,'2025-12-23 11:11:11.111111','amit.patel','amit.patel.temp@gmail.com',NULL,0,'user',NULL),(16,'pbkdf2_sha256$1200000$rT5KpdCjaRMW2hbz0jEgdZ$ZZWWyGDqFl0dFxzxCb48ub3BF07AuuaVn9fXJ2C43WU=','2025-12-22 09:09:09.999999',0,'Sneha','Nair',0,1,'2025-12-22 09:09:09.999999','sneha.nair','sneha.nair.temp@gmail.com',NULL,0,'user',NULL),(17,'pbkdf2_sha256$1200000$rT5KpdCjaRMW2hbz0jEgdZ$ZZWWyGDqFl0dFxzxCb48ub3BF07AuuaVn9fXJ2C43WU=','2025-12-21 20:00:00.123123',0,'Rahul','Mehta',0,1,'2025-12-21 20:00:00.123123','rahul.mehta','rahul.mehta.temp@gmail.com',NULL,0,'user',NULL),(18,'pbkdf2_sha256$1200000$rT5KpdCjaRMW2hbz0jEgdZ$ZZWWyGDqFl0dFxzxCb48ub3BF07AuuaVn9fXJ2C43WU=','2025-12-20 07:45:30.456456',0,'Pooja','Singh',0,1,'2025-12-20 07:45:30.456456','pooja.singh','pooja.singh.temp@gmail.com',NULL,0,'user',NULL),(19,'pbkdf2_sha256$1200000$rT5KpdCjaRMW2hbz0jEgdZ$ZZWWyGDqFl0dFxzxCb48ub3BF07AuuaVn9fXJ2C43WU=','2025-12-19 16:59:59.999000',0,'Vikram','Malhotra',0,1,'2025-12-19 16:59:59.999000','vikram.malhotra','vikram.malhotra.temp@gmail.com',NULL,0,'user',NULL),(20,'pbkdf2_sha256$1200000$oWCinZJ1ErWKRcKBRtpfYk$CkczpvKLyinq6tgFEOFPuyYotlDjFiLMFxUMuTULx7s=',NULL,0,'','',0,0,'2026-01-03 17:38:04.078741','geetha','geetha_shanmuga@yahoo.co.in','',0,'user',NULL),(22,'pbkdf2_sha256$1200000$3CeNcxSM5r4Ez9Bl8Sv1OF$cmXt0Wo4P6fsqUXGxkZnX9ZS0EbQx1iAFN41GRXx+iQ=','2026-01-12 20:14:58.321785',0,'','',0,1,'2026-01-12 20:11:15.763198','Nigel','nrj-auto_ngx@use.startmail.com','',0,'user',NULL),(23,'pbkdf2_sha256$1200000$Ol8VWyoyaMuSay17UkS0gB$r2+okCrv9aoYvdT3cDOJGyULHB0oGIoOi5j3NpM9Q98=','2026-01-14 12:43:33.306730',0,'','',0,1,'2026-01-14 12:42:51.217789','reddragon','reddragonak2003@gmail.com','',0,'user',NULL);
/*!40000 ALTER TABLE `user_tbl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_tbl_groups`
--

DROP TABLE IF EXISTS `user_tbl_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_tbl_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_tbl_groups_user_id_group_id_82dbed47_uniq` (`user_id`,`group_id`),
  KEY `user_tbl_groups_user_id_728ffbf3` (`user_id`),
  KEY `user_tbl_groups_group_id_a9653c7c` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_tbl_groups`
--

LOCK TABLES `user_tbl_groups` WRITE;
/*!40000 ALTER TABLE `user_tbl_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_tbl_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_tbl_user_permissions`
--

DROP TABLE IF EXISTS `user_tbl_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_tbl_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_tbl_user_permissions_user_id_permission_id_c69d1935_uniq` (`user_id`,`permission_id`),
  KEY `user_tbl_user_permissions_user_id_29bb216a` (`user_id`),
  KEY `user_tbl_user_permissions_permission_id_8cb7f84c` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_tbl_user_permissions`
--

LOCK TABLES `user_tbl_user_permissions` WRITE;
/*!40000 ALTER TABLE `user_tbl_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_tbl_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vehicle_registration`
--

DROP TABLE IF EXISTS `vehicle_registration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vehicle_registration` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `vrn` varchar(20) NOT NULL,
  `make` varchar(100) DEFAULT NULL,
  `model` varchar(100) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  `mot_expiry_date` date DEFAULT NULL,
  `mot_status` varchar(20) DEFAULT NULL,
  `tax_due_date` date DEFAULT NULL,
  `tax_status` varchar(20) DEFAULT NULL,
  `api_error` varchar(100) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `last_checked_at` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `vehicle_registration_user_id_vrn_ed330e30_uniq` (`user_id`,`vrn`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicle_registration`
--

LOCK TABLES `vehicle_registration` WRITE;
/*!40000 ALTER TABLE `vehicle_registration` DISABLE KEYS */;
INSERT INTO `vehicle_registration` VALUES (9,'V111ELU','MERCEDES-BENZ','GLS','2025-12-31 05:32:38.240907',9,'2024-05-18','Not valid','2024-06-01','Untaxed',NULL,1,'2026-01-13 18:23:03.299025'),(10,'V777ELU','MERCEDES-BENZ','GLS','2025-12-31 09:17:02.897094',9,'2026-07-31','Valid','2026-11-01','Taxed',NULL,1,'2026-01-13 18:23:04.291925'),(12,'FG19NZZ','VOLKSWAGEN','GOLF','2025-12-31 09:21:18.667522',9,'2026-03-30','Valid','2026-03-01','Taxed',NULL,1,'2026-01-13 18:23:05.575784'),(13,'FV19MOA','SKODA','KODIAQ','2025-12-31 11:08:07.905494',9,'2026-05-19','Valid','2026-05-01','Taxed',NULL,1,'2026-01-13 18:23:06.599975'),(14,'FL16ZSV','VOLKSWAGEN','GOLF','2025-12-31 11:08:53.734076',9,'2026-03-18','Valid','2026-06-01','Taxed',NULL,1,'2026-01-13 18:23:07.423928'),(16,'MU54GGO','MINI','COOPER S','2025-12-31 11:13:48.767900',9,'2026-04-10','Valid','2026-09-01','Taxed',NULL,1,'2026-01-13 18:23:08.703021'),(18,'MF67LSD','CITROEN','C3','2025-12-31 11:22:55.416724',9,'2026-10-11','Valid','2026-11-01','Taxed',NULL,1,'2026-01-13 18:23:09.544569'),(20,'YE73NGV','NISSAN','LEAF','2025-12-31 13:33:53.704750',9,'2026-09-29','No MOT required','2026-05-01','Taxed',NULL,1,'2026-01-13 18:23:10.567959'),(21,'V777ELU','MERCEDES-BENZ','GLS','2025-12-31 13:42:11.952745',1,'2026-07-31','Valid','2026-11-01','Taxed',NULL,1,'2026-01-13 18:23:11.497407'),(25,'MU54GGO','MINI','COOPER S','2025-12-31 15:50:44.085029',1,'2026-04-10','Valid','2026-09-01','Taxed',NULL,1,'2026-01-13 18:23:12.307845'),(26,'YE73NGV','NISSAN','LEAF','2025-12-31 16:47:35.947750',1,'2026-09-29','No MOT required','2026-05-01','Taxed',NULL,1,'2026-01-13 18:23:13.624330'),(27,'YE25KFG','RENAULT','SYMBIOZ TECHNO ESPT ALPN HEV A','2026-01-01 05:46:52.554907',1,'2028-03-30','No MOT required','2026-04-01','Taxed',NULL,1,'2026-01-13 18:23:14.607587'),(28,'V111ELU','MERCEDES-BENZ','GLS','2026-01-01 10:43:09.612817',3,'2024-05-18','Not valid','2024-06-01','Untaxed',NULL,1,'2026-01-13 18:23:15.952154'),(29,'V777ELU','MERCEDES-BENZ','GLS','2026-01-01 10:51:01.262021',3,'2026-07-31','Valid','2026-11-01','Taxed',NULL,1,'2026-01-13 18:23:16.802557'),(30,'FV19MOA','SKODA','KODIAQ','2026-01-01 10:51:12.030030',3,'2026-05-19','Valid','2026-05-01','Taxed',NULL,1,'2026-01-13 18:23:18.122487'),(31,'FG19NZZ','VOLKSWAGEN','GOLF','2026-01-01 10:51:23.009041',3,'2026-03-30','Valid','2026-03-01','Taxed',NULL,1,'2026-01-13 18:23:18.958109'),(32,'AB18DAD','SKODA','KODIAQ','2026-01-01 10:51:58.635977',3,'2026-07-04','Valid','2026-08-01','Taxed',NULL,1,'2026-01-13 18:23:20.077244'),(33,'YE73NGV','NISSAN','LEAF','2026-01-01 10:52:32.636807',3,'2026-09-29','No MOT required','2026-05-01','Taxed',NULL,1,'2026-01-13 18:23:21.015618'),(34,'YE74SDO','LAND ROVER','DEFENDER HDTP XDYN HSE DMHEV A','2026-01-01 10:53:10.318784',3,'2027-11-18','No MOT required','2026-11-01','Taxed',NULL,1,'2026-01-13 18:23:21.874133'),(36,'FG09GHX','PEUGEOT','207','2026-01-02 13:36:18.816770',3,'2027-01-15','Valid','2027-01-01','Taxed',NULL,1,'2026-01-13 18:23:22.906306'),(42,'YE25KFG','ASTON MARTIN','DB5','2026-01-02 18:17:12.506406',9,'2028-03-30','No MOT required','2026-04-01','Taxed',NULL,1,'2026-01-13 18:23:23.797890'),(43,'FG19NZZ','VOLKSWAGEN','GOLF','2026-01-08 14:28:28.952558',1,'2026-03-30','Valid','2026-03-01','Taxed',NULL,1,'2026-01-13 18:23:25.250325'),(46,'B1','ASTON MARTIN','DB5','2026-01-08 16:18:33.400322',1,NULL,'No results returned','2027-02-01','Taxed',NULL,1,'2026-01-13 18:23:26.097522'),(49,'GH15ACE','MINI','COUNTRYMAN EXCLUSIVE C MHEV A','2026-01-09 14:24:33.492848',3,'2027-04-23','No MOT required','2026-05-01','Taxed',NULL,1,'2026-01-13 18:23:27.246740'),(50,'FG11NZZ','BMW','520','2026-01-09 15:06:43.641547',3,'2025-12-18','Not valid','2025-10-01','Untaxed',NULL,1,'2026-01-13 18:23:28.375473'),(51,'FG17CFE','VOLKSWAGEN','PASSAT','2026-01-09 16:50:27.592499',3,'2027-01-11','Valid','2027-01-01','Taxed',NULL,1,'2026-01-13 18:23:29.659401'),(52,'FG17CFE','VOLKSWAGEN','PASSAT','2026-01-12 20:15:11.783007',22,'2027-01-11','Valid','2027-01-01','Taxed',NULL,1,'2026-01-13 18:23:30.422922'),(53,'FG66EYC','BMW','520','2026-01-13 15:13:36.685269',3,'2026-08-24','Valid','2026-10-01','Taxed',NULL,1,'2026-01-13 18:23:31.296361'),(55,'JCB2','MERCEDES-BENZ','S500 L AMG LN PRM+EXC MHEV4M A','2026-01-13 15:30:57.445717',3,'2027-09-29','No MOT required','2026-02-01','Taxed',NULL,1,'2026-01-13 18:23:32.201886'),(56,'JCB1','BENTLEY','S1 CONTINENTAL','2026-01-13 15:31:20.745180',3,NULL,'No results returned','2026-07-01','Taxed',NULL,1,'2026-01-13 18:23:33.427359'),(58,'JCB2','MERCEDES-BENZ','S500 L AMG LN PRM+EXC MHEV4M A','2026-01-14 12:44:29.632148',23,'2027-09-29','No MOT required','2026-02-01','Taxed',NULL,1,NULL);
/*!40000 ALTER TABLE `vehicle_registration` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-14 14:50:16
