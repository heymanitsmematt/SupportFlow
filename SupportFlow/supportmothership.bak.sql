CREATE DATABASE  IF NOT EXISTS `supportknowledgebase` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `supportknowledgebase`;
-- MySQL dump 10.13  Distrib 5.6.17, for Win32 (x86)
--
-- Host: localhost    Database: supportknowledgebase
-- ------------------------------------------------------
-- Server version	5.6.20

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `app_emailtrollermodel`
--

DROP TABLE IF EXISTS `app_emailtrollermodel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_emailtrollermodel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `last_ticket_received` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_emailtrollermodel`
--

LOCK TABLES `app_emailtrollermodel` WRITE;
/*!40000 ALTER TABLE `app_emailtrollermodel` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_emailtrollermodel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_employeemaster`
--

DROP TABLE IF EXISTS `app_employeemaster`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_employeemaster` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(200) NOT NULL,
  `last_name` varchar(200) NOT NULL,
  `email` varchar(200) NOT NULL,
  `phone_ext` int(11) DEFAULT NULL,
  `phone_cell` int(11) DEFAULT NULL,
  `mosolegacy` varchar(5) DEFAULT NULL,
  `position` varchar(200) DEFAULT NULL,
  `hiredate` datetime DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `app_employeemaster_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_id_ef38b289` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_employeemaster`
--

LOCK TABLES `app_employeemaster` WRITE;
/*!40000 ALTER TABLE `app_employeemaster` DISABLE KEYS */;
INSERT INTO `app_employeemaster` VALUES (1,'','','',NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `app_employeemaster` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_node_1`
--

DROP TABLE IF EXISTS `app_node_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_node_1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `node_name` varchar(100) NOT NULL,
  `node_description` varchar(200) NOT NULL,
  `image_folder` varchar(100) DEFAULT NULL,
  `details` varchar(5000) DEFAULT NULL,
  `pdf_path` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`,`node_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_node_1`
--

LOCK TABLES `app_node_1` WRITE;
/*!40000 ALTER TABLE `app_node_1` DISABLE KEYS */;
INSERT INTO `app_node_1` VALUES (1,'Modules','The primary modules which comprize the main Conexion software','Node_1/Modules','The family of modules that comprise the Conexion software, including Membership Management, Point of Sale, Agreement Writer, Scheduler, Check in, and others.',NULL),(2,'Hardware','Standard hardware used in the Conexion environment','Node_1/Hardware','Is HE EATING BABABYYYY FFFAAOOOODDDDD?!!?!?!?!',NULL),(3,'Keycard Application','The keycard application used to record visits afterhours or at an unmanned terminal','Node_1/Keycard Application',NULL,NULL);
/*!40000 ALTER TABLE `app_node_1` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_node_1_parent`
--

DROP TABLE IF EXISTS `app_node_1_parent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_node_1_parent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `node_1_id` int(11) NOT NULL,
  `parent_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `node_1_id` (`node_1_id`,`parent_id`),
  KEY `app_node_1_parent_b6993bc3` (`node_1_id`),
  KEY `app_node_1_parent_410d0aac` (`parent_id`),
  CONSTRAINT `node_1_id_refs_id_548ce94f` FOREIGN KEY (`node_1_id`) REFERENCES `app_node_1` (`id`),
  CONSTRAINT `parent_id_refs_id_de1d07bf` FOREIGN KEY (`parent_id`) REFERENCES `app_parent` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_node_1_parent`
--

LOCK TABLES `app_node_1_parent` WRITE;
/*!40000 ALTER TABLE `app_node_1_parent` DISABLE KEYS */;
INSERT INTO `app_node_1_parent` VALUES (1,1,1),(2,2,1),(3,3,1);
/*!40000 ALTER TABLE `app_node_1_parent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_node_2`
--

DROP TABLE IF EXISTS `app_node_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_node_2` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `node_name` varchar(100) NOT NULL,
  `node_description` varchar(100) NOT NULL,
  `image_folder` varchar(100) DEFAULT NULL,
  `details` varchar(5000) DEFAULT NULL,
  `pdf_path` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`,`node_name`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_node_2`
--

LOCK TABLES `app_node_2` WRITE;
/*!40000 ALTER TABLE `app_node_2` DISABLE KEYS */;
INSERT INTO `app_node_2` VALUES (1,'Membership Management','The primary module used to manage member data, generate reports, and manage billing','Node_2/Membership Management','Billing\n	A demonstration of the billing process and what the various steps entail.\n	Descriptions of the various reports generated during the billing process.\n\nBilling Settings\n\nRollback - (Note: do not do without supervisor approval)','C:\\users\\mwillis\\desktop\\pdf.pdf'),(2,'Point of Sale','The point of sale module, used to process transactions, manage inventory, and run sales reports.','Node_2/Point of Sale','hi.\n\n\nhello yourself.',NULL),(3,'Agreement Writer','The wizard used to sign members up to memberships and sign members up to service contracts.','Node_2/Agreement Writer','hi',NULL),(4,'Punchclock','The module used to manage employee hours, including reporting.','Node_2/punchclock','PUNCH\n\n\n\nME\n\n\nIN THE \n\n                            CLOOOCCCKKKKK\n\n    ',NULL),(5,'Printers','The commonly used receipt and document printers and their configurations and troubleshooting steps.','Node_2/printers',NULL,NULL),(6,'Handkey Scanner','The handkey scanner used in checkin and configured in Membership Management.','Node_2/handkey scanner',NULL,NULL),(7,'Barcode Scanners','The barcode scanners used in POS and Checkin.','Node_2/barcode scanner',NULL,NULL),(8,'Door Components','Door hardware components including RFID readers and locking mechanisms.','Node_2/door components',NULL,NULL);
/*!40000 ALTER TABLE `app_node_2` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_node_2_parent`
--

DROP TABLE IF EXISTS `app_node_2_parent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_node_2_parent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `node_2_id` int(11) NOT NULL,
  `node_1_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `node_2_id` (`node_2_id`,`node_1_id`),
  KEY `app_node_2_parent_d76d38b7` (`node_2_id`),
  KEY `app_node_2_parent_b6993bc3` (`node_1_id`),
  CONSTRAINT `node_1_id_refs_id_3f0cadde` FOREIGN KEY (`node_1_id`) REFERENCES `app_node_1` (`id`),
  CONSTRAINT `node_2_id_refs_id_d20a31cb` FOREIGN KEY (`node_2_id`) REFERENCES `app_node_2` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_node_2_parent`
--

LOCK TABLES `app_node_2_parent` WRITE;
/*!40000 ALTER TABLE `app_node_2_parent` DISABLE KEYS */;
INSERT INTO `app_node_2_parent` VALUES (1,1,1),(2,2,1),(3,3,1),(4,4,1),(5,5,2),(6,6,2),(7,7,2),(8,8,2);
/*!40000 ALTER TABLE `app_node_2_parent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_node_3`
--

DROP TABLE IF EXISTS `app_node_3`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_node_3` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `node_name` varchar(100) NOT NULL,
  `node_description` varchar(100) NOT NULL,
  `image_folder` varchar(100) DEFAULT NULL,
  `details` varchar(5000) DEFAULT NULL,
  `pdf_path` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`,`node_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_node_3`
--

LOCK TABLES `app_node_3` WRITE;
/*!40000 ALTER TABLE `app_node_3` DISABLE KEYS */;
INSERT INTO `app_node_3` VALUES (1,'Billing Tutorial','General billing examples and tutorials.','Node_3/billing tutorial','kevin is a real cool guy\n\n\n       Paul used to be. \n\nMATTHEW WILL ALWAYS BE!',NULL),(2,'Reports','Examples of general reporting done in Memebership Management and tutorials.','Node_3/reports','Sean is a real cool dood.',NULL),(3,'Ledger Management','Records of invoices, payments, and adjustments from member transactions.','Node_3/ledger management','oh hi.',NULL);
/*!40000 ALTER TABLE `app_node_3` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_node_3_parent`
--

DROP TABLE IF EXISTS `app_node_3_parent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_node_3_parent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `node_3_id` int(11) NOT NULL,
  `node_2_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `node_3_id` (`node_3_id`,`node_2_id`),
  KEY `app_node_3_parent_8391a7ff` (`node_3_id`),
  KEY `app_node_3_parent_d76d38b7` (`node_2_id`),
  CONSTRAINT `node_2_id_refs_id_3e98abc1` FOREIGN KEY (`node_2_id`) REFERENCES `app_node_2` (`id`),
  CONSTRAINT `node_3_id_refs_id_e0cd2c5d` FOREIGN KEY (`node_3_id`) REFERENCES `app_node_3` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_node_3_parent`
--

LOCK TABLES `app_node_3_parent` WRITE;
/*!40000 ALTER TABLE `app_node_3_parent` DISABLE KEYS */;
INSERT INTO `app_node_3_parent` VALUES (1,1,1),(2,2,1),(3,3,1);
/*!40000 ALTER TABLE `app_node_3_parent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_node_4`
--

DROP TABLE IF EXISTS `app_node_4`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_node_4` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `node_name` varchar(100) NOT NULL,
  `node_description` varchar(100) NOT NULL,
  `image_folder` varchar(100) DEFAULT NULL,
  `details` varchar(5000) DEFAULT NULL,
  `pdf_path` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`,`node_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_node_4`
--

LOCK TABLES `app_node_4` WRITE;
/*!40000 ALTER TABLE `app_node_4` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_node_4` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_node_4_parent`
--

DROP TABLE IF EXISTS `app_node_4_parent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_node_4_parent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `node_4_id` int(11) NOT NULL,
  `node_3_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `node_4_id` (`node_4_id`,`node_3_id`),
  KEY `app_node_4_parent_88f658b2` (`node_4_id`),
  KEY `app_node_4_parent_8391a7ff` (`node_3_id`),
  CONSTRAINT `node_3_id_refs_id_97ea327a` FOREIGN KEY (`node_3_id`) REFERENCES `app_node_3` (`id`),
  CONSTRAINT `node_4_id_refs_id_b1ab694d` FOREIGN KEY (`node_4_id`) REFERENCES `app_node_4` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_node_4_parent`
--

LOCK TABLES `app_node_4_parent` WRITE;
/*!40000 ALTER TABLE `app_node_4_parent` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_node_4_parent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_node_5`
--

DROP TABLE IF EXISTS `app_node_5`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_node_5` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `node_name` varchar(100) NOT NULL,
  `node_description` varchar(100) NOT NULL,
  `image_folder` varchar(100) DEFAULT NULL,
  `details` varchar(5000) DEFAULT NULL,
  `pdf_path` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`,`node_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_node_5`
--

LOCK TABLES `app_node_5` WRITE;
/*!40000 ALTER TABLE `app_node_5` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_node_5` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_node_5_parent`
--

DROP TABLE IF EXISTS `app_node_5_parent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_node_5_parent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `node_5_id` int(11) NOT NULL,
  `node_3_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `node_5_id` (`node_5_id`,`node_3_id`),
  KEY `app_node_5_parent_340894f3` (`node_5_id`),
  KEY `app_node_5_parent_8391a7ff` (`node_3_id`),
  CONSTRAINT `node_3_id_refs_id_abbce287` FOREIGN KEY (`node_3_id`) REFERENCES `app_node_3` (`id`),
  CONSTRAINT `node_5_id_refs_id_c676e286` FOREIGN KEY (`node_5_id`) REFERENCES `app_node_5` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_node_5_parent`
--

LOCK TABLES `app_node_5_parent` WRITE;
/*!40000 ALTER TABLE `app_node_5_parent` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_node_5_parent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_parent`
--

DROP TABLE IF EXISTS `app_parent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_parent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_name` varchar(100) NOT NULL,
  `parent_description` varchar(200) NOT NULL,
  `image_folder` varchar(100) DEFAULT NULL,
  `details` varchar(5000) DEFAULT NULL,
  `pdf_path` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`,`parent_name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_parent`
--

LOCK TABLES `app_parent` WRITE;
/*!40000 ALTER TABLE `app_parent` DISABLE KEYS */;
INSERT INTO `app_parent` VALUES (1,'Conexion','Conexion Club Management Software hosted solution','Conexion/images','Select a main topic.',NULL);
/*!40000 ALTER TABLE `app_parent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_skills`
--

DROP TABLE IF EXISTS `app_skills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_skills` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(200) NOT NULL,
  `skill_score` double DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_skills`
--

LOCK TABLES `app_skills` WRITE;
/*!40000 ALTER TABLE `app_skills` DISABLE KEYS */;
/*!40000 ALTER TABLE `app_skills` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_ticket`
--

DROP TABLE IF EXISTS `app_ticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_ticket` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `netsuite_id` int(11) DEFAULT NULL,
  `customer` varchar(100) DEFAULT NULL,
  `client_id` varchar(50) DEFAULT NULL,
  `caller` varchar(100) DEFAULT NULL,
  `callback_phone` varchar(100) DEFAULT NULL,
  `netsuite_case_number` int(11) DEFAULT NULL,
  `case_type` varchar(100) DEFAULT NULL,
  `case_origin` varchar(100) DEFAULT NULL,
  `product` varchar(100) DEFAULT NULL,
  `module` varchar(100) DEFAULT NULL,
  `short_description` varchar(5000) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  `severity` varchar(25) DEFAULT NULL,
  `priority` varchar(25) DEFAULT NULL,
  `assigned_to` varchar(100) DEFAULT NULL,
  `escalated_to` varchar(100) DEFAULT NULL,
  `open_date` varchar(100) DEFAULT NULL,
  `opened_by` varchar(100) DEFAULT NULL,
  `first_call_resolution` longblob,
  `last_updated` varchar(100) DEFAULT NULL,
  `jira_issue` varchar(100) DEFAULT NULL,
  `most_recent_comment` varchar(10000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_ticket`
--

LOCK TABLES `app_ticket` WRITE;
/*!40000 ALTER TABLE `app_ticket` DISABLE KEYS */;
INSERT INTO `app_ticket` VALUES (1,1424795,'WOW! Work Out World','L1122',NULL,'732.477.5400',108701,'Support Case','E-mail','MoSo - MyClub','MyClub - Signup','Join On Line process\r\n appeared to complete and it created the member record but it did not create an agreement or an invoice','Tracked','S2','2 - High','Kimberly P Wood','','11/26/2014','Kimberly P\r\n Wood','','null','MOSO-8807',NULL),(2,1427520,'Mount Vernon Athletic Club','2029',NULL,'703.360.7300',108971,'Support Case','E-mail','MoSo - Application','Inventory','Inventory\r\n totals for MTVAC for November 2014','OnHold - Assigned to Customer','S4','4 - Low','Mathew Willis','Mathew Willis','12/8/2014',' ','','null','',NULL),(3,1429649,'Soldierfit','2020',NULL,'240.447.3705',109209,'Support Case','Phone','MoSo - Application','General Member','Member redirecting on\r\n load','Closed','S2','2 - High','Mathew Willis','','12/12/2014','Mathew Willis','','null','',NULL),(4,1423897,'Soldierfit','2020',NULL,'240.447.3705',108614,'Support Case','E-mail','MoSo - Application','Billing','Gift card billing issue','Tracked','S4','4\r\n - Low','Mathew Willis','','11/24/2014',' ','','null','MOSO-8409',NULL),(5,1432084,'Mount Vernon Athletic Club','2029',NULL,'703.360.7300',109388,'Support Case','E-mail','','','Inability to schedule PT with installment\r\n agreements (new issue?)','Active',' ','4 - Low','Shira L Hirschfeld','','12/18/2014',' ','','null','',NULL),(6,1412518,'Meridian Health','Meridian Health',NULL,'732.295.1778',107942,'Support Case','Phone','eClubLogic','eClub - App','api-test','OnHold\r\n - Customer Responded','S4','4 - Low','Mathew Willis','Mathew Willis','10/31/2014','Mathew Willis','F','null','MOSO-6168','test'),(21,1426253,'Akron General Hospital Lifestyle Center','L1158',NULL,'330.945.3186',108825,'Support Case','Phone','eClubLogic','eClub - App','Sporatic\r\n nonresponsive POS leading to double charges','Escalated - Open','S2','2 - High','Mathew Willis','Kumuzu Zaman','12/3/2014','Mathew Willis','','null','',NULL),(22,1432200,'Matrix Corporate Center','L1069',NULL,'203.312.1570',109400,'Support Case','Phone','Conexion','Billing','Billing Help','Closed','S4','4\r\n - Low','Kevin K Hunt','','12/18/2014','Kevin K Hunt','T','null','',NULL),(23,1401954,'Vive Health & Fitness',NULL,NULL,'(717) 994-8834',107474,'Support Case','Phone','MoSo - Application','Scheduler','Scheduler email reminders template\r\n not updating from text to html','Tracked','S4','4 - Low','Mathew Willis','','10/16/2014','Mathew Willis','','null','MOSO-8407',NULL),(24,1397983,'Active Sports Clubs / Club One',NULL,NULL,'415.288.1043',107202,'Support Case','E-mail','MoSo - Application','Agreements','Suspension didn\'t extend\r\n contract','Tracked','S4','4 - Low','Mathew Willis','','10/7/2014',' ','','null','MOSO-4879',NULL),(26,1432218,'Fitness Factory New Providence',NULL,NULL,'201.243.8422',109413,'Support Case','E-mail','Conexion','Membership Management','Request for Memtype PriceID\r\n Numbers','Closed','S4','4 - Low','Cory Pidgeon','','12/18/2014','Cory Pidgeon','T','null','',NULL),(27,1430493,'Spectrum Club Holding Company',NULL,NULL,'310.727.9366',109271,'Support Case','Other','MoSo - Application','Childcare','A designated guardian cannot\r\n check in a child to childcare without a childcare service item','Escalated - Open','S2','2 - High','Tara A Levitt','Christopher Mossman','12/15/2014','Tara A Levitt','','null','',NULL),(28,1432228,'Corporate Sports Unlimited - Go Fitness Center',NULL,NULL,'404.714.6348',109417,'Support Case','Phone','Conexion','Point Of Sale','MosoPay POS Error\r\n 25','Active','S2','4 - Low','Cory Pidgeon','','12/18/2014','Cory Pidgeon','','null','',NULL),(29,1428201,'Downtown Athletic Club',NULL,NULL,'541.484.4011 x272',109051,'Support Case','Phone','Conexion','Technical','installing CX on brand new computers','Active','S3','4\r\n - Low','Paul A Bikowski','','12/9/2014','Paul A Bikowski','','null','',NULL),(30,1385880,'World Health',NULL,NULL,'403.519.7845',106584,'Support Case','Phone','MoSo - Application','POS','Return Fee not being accounted for in payments','Escalated\r\n - Open','S2','2 - High','Shira L Hirschfeld','Christopher Mossman','9/18/2014','Shira L Hirschfeld','F','null','MOSO-9055','Type\r\n text and format it using the toolbar.'),(31,1432224,'Motionsoft',NULL,NULL,'123.456.7890',109415,'Implementation Case','E-mail','MoSo - Application','General Member','Requesting full backup of WAC production','Escalated\r\n - Open','S2','2 - High','Anita Carr','','12/18/2014','Anita Carr','','null','',NULL),(32,1432211,'Fitness Factory New Providence',NULL,NULL,'908.665.9500',109409,'Support Case','Phone','Conexion','Membership Management','New Agreement Price Training','Closed','S4','4 - Low','Kevin K Hunt','','12/18/2014','Kevin K Hunt','T','null','',NULL),(33,1431396,'Hunterdon Health & Wellness Center - Whitehouse',NULL,NULL,'908.534.7600 x 4',109333,'Support Case','Phone','eClubLogic','eClub - App','Dues increase','OnHold - Assigned to Customer','S4','4 - Low','Mathew Willis','Kevin Hunt','12/17/2014','Mathew Willis','','null','',NULL),(34,1431401,'Town Sports International',NULL,NULL,'212.246.6700 x1272',109335,'Support Case','Web','MoSo - Application','Activity Mgt','TSI - PRODUCTION - Session\r\n Alignment and Expiration Issues','Escalated - Resolved','S2','3 - Moderate','Seth Low','','12/17/2014',' ','','null','','Type\r\n text and format it using the toolbar.'),(35,1432338,'World Health',NULL,NULL,'403.519.7845',109422,'Support Case','Internal','MoSo - Application','System Config','Amount Due is off between WHE Pro &\r\n Sandbox','Tracked','S2','2 - High','Ahmad Abdel','','12/18/2014','Ahmad Abdel','','null','MOSO-9058','Type\r\n text and format it using the toolbar.'),(36,1432225,'Fitness Factory New Providence',NULL,NULL,'908.665.9500',109416,'Support Case','Phone','Conexion','Membership Management','Receipt Printer Setup','Closed','S3','4 - Low','Kevin K Hunt','','12/18/2014','Kevin K Hunt','F','null','',NULL),(37,1430615,'OAC - Duniway',NULL,NULL,'503.294.3366',109287,'Support Case','E-mail','eClubLogic','eClub - App','ThinPrint Install','OnHold\r\n - Assigned to Customer','S4','4 - Low','Kevin K Hunt','','12/16/2014',' ','','null','',NULL),(38,1429662,'Work Out World Moso Implementation',NULL,NULL,'800.829.4321',109216,'Support Case','Internal','MoSo - Application','Activity Mgt','Activity Management\r\n Assigning Incorrect Use Dates - Affecting Reporting','Tracked','S2','2 - High','Jonathan R Minogue','Christopher Mossman','12/12/2014','Jonathan\r\n R Minogue','','null','MOSO-8908` MOSO-8937','Type text and format it using the toolbar.'),(39,1431381,'WOW! Work Out World',NULL,NULL,'732.477.5400',109325,'Support Case','E-mail','MoSo - Application','System Config','SalesPerson and Lead Source fields\r\n are missing from Portal Configuration','Escalated - Open','S2','2 - High','Kimberly P Wood','','12/17/2014','Kimberly P Wood','','null','MOSO-8997','Type\r\n text and format it using the toolbar.'),(40,1432072,'Motionsoft',NULL,NULL,'123.456.7890',109386,'Prod Mgt/Dev Issue','Internal','MoSo - Application','Agreements','MTP 12-18-2014','Escalated\r\n - Resolved','S3','3 - Moderate','Dinesh Gunapalan','','12/18/2014','Dinesh Gunapalan','','null','','Type text and format\r\n it using the toolbar.'),(41,1432351,'Vive Health & Fitness',NULL,NULL,'717.994.8834',109433,'Support Case','E-mail','MoSo - Application','Agreements','Installment Access Item expired\r\n early','Escalated - Resolved','S3','3 - Moderate','Shira L Hirschfeld','Christopher Mossman','12/19/2014','Shira L Hirschfeld','','null','MOSO-6951','Type\r\n text and format it using the toolbar.'),(42,1411117,'Town Sports International',NULL,NULL,'212.246.6700 x1272',107845,'Support Case','Web','MoSo - MyClub','SCH - Class/Events','Members Unable to Register\r\n for GEX Core Free Classes Via MyClub','Active','S4','4 - Low','Seth Low','','10/29/2014',' ','','null','','Type\r\n text and format it using the toolbar.'),(43,1432353,'Motionsoft',NULL,NULL,'123.456.7890',109435,'Implementation Case','E-mail','MoSo - Application','General Member','Requesting read sql access to WAC\r\n production','Escalated - Resolved','S4','4 - Low','Anita Carr','','12/19/2014','Anita Carr','','null','','Type\r\n text and format it using the toolbar.'),(44,1432352,'Motionsoft',NULL,NULL,'123.456.7890',109434,'Implementation Case','E-mail','MoSo - Application','General Member','Requesting Read SQL access to Spectrum\r\n production','Escalated - Open','S4','4 - Low','Anita Carr','','12/19/2014','Anita Carr','','null','','Type\r\n text and format it using the toolbar.'),(45,1432350,'Motionsoft',NULL,NULL,'123.456.7890',109432,'Prod Mgt/Dev Issue','Internal','MoSo - Application','Agreements','Cancellation Issues','Escalated\r\n - Resolved','S2','2 - High','Dinesh Gunapalan','','12/19/2014','Dinesh Gunapalan','','null','','Type text and format it\r\n using the toolbar.'),(46,1431037,'Active Sports Clubs / Club One',NULL,NULL,'415.288.1043',109299,'Support Case','E-mail','MoSo - Application','General Member','Fwd~ Blue Highlight','Tracked','S3','3\r\n - Moderate','Shira L Hirschfeld','Dinesh Gunapalan','12/16/2014',' ','','null','MOSO-9076','Type text and format it using the toolbar.'),(47,1432204,'Conway Medical Center - Wellness Center',NULL,NULL,'843.347.1515',109403,'Support Case','Phone','eClubLogic','eClub - App','batch files are erroring\r\n out','Closed','S2','3 - Moderate','Paul A Bikowski','','12/18/2014','Paul A Bikowski','F','null','','Debbie\r\n called back today but I was not in yet. When I came into work I called her back and she said she was afraid to run the batch without me on the phone with her. We connected via fast support again and recreated the batch and then ran it.....and it worked! She\r\n was getting accepts and declines and no errors.'),(48,1431275,'Work Out World Moso Implementation',NULL,NULL,'800.829.4321',109320,'Support Case','E-mail','MoSo - Application','Activity Mgt','Activity in Scheduler\r\n not Appearing in Activity Management','Tracked','S2','2 - High','Jonathan R Minogue','Christopher Mossman','12/16/2014','Jonathan\r\n R Minogue','F','null','MOSO-9074` MOSO-8908','Added Jira ticket and linked to Jira ticket causing the inaccurate \'Use\' records.'),(49,1431529,'WOW! Work Out World',NULL,NULL,'908.783.8109',109354,'Support Case','E-mail','MoSo - Application','Agreements','The signature capture pads ae not\r\n working','Escalated - Open','S2','2 - High','Kimberly P Wood','','12/17/2014','Kimberly P Wood','','null','',''),(50,1432349,'Motionsoft',NULL,NULL,'123.456.7890',109431,'Prod Mgt/Dev Issue','Internal','MoSo - Application','Agreements','MPT 12-19-2014','Escalated\r\n - Open','S3','4 - Low','Dinesh Gunapalan','','12/19/2014','Dinesh Gunapalan','','null','','Type text and format it using\r\n the toolbar.'),(51,1430724,'Oakridge Athletic Club',NULL,NULL,'805.522.5454',109290,'Support Case','E-mail','MoSo - Application','Data Analytics','Incorrect Billing Statement','Escalated - Open','S3','3 - Moderate','Shira L Hirschfeld','Dinesh Gunapalan','12/16/2014',' ','','null','','Type\r\n text and format it using the toolbar.'),(52,1432565,'Motionsoft',NULL,NULL,'123.456.7890',109443,'Support Case','Internal','MoSo - Application','Data Analytics','Spectrum Current Backup','Escalated\r\n - Open','S2','2 - High','.Moso Dev Ops','','12/19/2014','Scott D Ferguson','','null','','Type text and format it using\r\n the toolbar.'),(53,1432344,'Fitness Factory Health Club - Edgewater',NULL,NULL,'201.456.2101',109427,'Support Case','Phone','Conexion','Technical','facilities on myclub only\r\n list one facility','Closed','S3','3 - Moderate','Cory Pidgeon','','12/18/2014','Paul A Bikowski','F','null','','Type\r\n text and format it using the toolbar.');
/*!40000 ALTER TABLE `app_ticket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_5f412f9a` (`group_id`),
  KEY `auth_group_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `group_id_refs_id_f4b32aac` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_6ba0f519` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_d043b34a` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add content type',4,'add_contenttype'),(11,'Can change content type',4,'change_contenttype'),(12,'Can delete content type',4,'delete_contenttype'),(13,'Can add session',5,'add_session'),(14,'Can change session',5,'change_session'),(15,'Can delete session',5,'delete_session'),(16,'Can add site',6,'add_site'),(17,'Can change site',6,'change_site'),(18,'Can delete site',6,'delete_site'),(19,'Can add employee master',7,'add_employeemaster'),(20,'Can change employee master',7,'change_employeemaster'),(21,'Can delete employee master',7,'delete_employeemaster'),(22,'Can add skills',8,'add_skills'),(23,'Can change skills',8,'change_skills'),(24,'Can delete skills',8,'delete_skills'),(25,'Can add parent',9,'add_parent'),(26,'Can change parent',9,'change_parent'),(27,'Can delete parent',9,'delete_parent'),(28,'Can add node_1',10,'add_node_1'),(29,'Can change node_1',10,'change_node_1'),(30,'Can delete node_1',10,'delete_node_1'),(31,'Can add node_2',11,'add_node_2'),(32,'Can change node_2',11,'change_node_2'),(33,'Can delete node_2',11,'delete_node_2'),(34,'Can add node_3',12,'add_node_3'),(35,'Can change node_3',12,'change_node_3'),(36,'Can delete node_3',12,'delete_node_3'),(37,'Can add node_4',13,'add_node_4'),(38,'Can change node_4',13,'change_node_4'),(39,'Can delete node_4',13,'delete_node_4'),(40,'Can add node_5',14,'add_node_5'),(41,'Can change node_5',14,'change_node_5'),(42,'Can delete node_5',14,'delete_node_5'),(43,'Can add log entry',15,'add_logentry'),(44,'Can change log entry',15,'change_logentry'),(45,'Can delete log entry',15,'delete_logentry'),(46,'Can add email troller model',16,'add_emailtrollermodel'),(47,'Can change email troller model',16,'change_emailtrollermodel'),(48,'Can delete email troller model',16,'delete_emailtrollermodel'),(49,'Can add ticket',17,'add_ticket'),(50,'Can change ticket',17,'change_ticket'),(51,'Can delete ticket',17,'delete_ticket');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$12000$IOhx0EwuBqVT$RV61w0I/MdcjUcKeRIuO1feLVT6ewnnY4w/eKyszC0Y=','2014-11-15 03:18:56',1,'mwillis','','','',1,1,'2014-09-18 14:21:49');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_6340c63c` (`user_id`),
  KEY `auth_user_groups_5f412f9a` (`group_id`),
  CONSTRAINT `group_id_refs_id_274b862c` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_id_refs_id_40c41112` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_6340c63c` (`user_id`),
  KEY `auth_user_user_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `permission_id_refs_id_35d9ac25` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_id_refs_id_4dc23c39` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_6340c63c` (`user_id`),
  KEY `django_admin_log_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_93d2d1f8` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_c0d12874` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'permission','auth','permission'),(2,'group','auth','group'),(3,'user','auth','user'),(4,'content type','contenttypes','contenttype'),(5,'session','sessions','session'),(6,'site','sites','site'),(7,'employee master','app','employeemaster'),(8,'skills','app','skills'),(9,'parent','app','parent'),(10,'node_1','app','node_1'),(11,'node_2','app','node_2'),(12,'node_3','app','node_3'),(13,'node_4','app','node_4'),(14,'node_5','app','node_5'),(15,'log entry','admin','logentry'),(16,'email troller model','app','emailtrollermodel'),(17,'ticket','app','ticket');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_b7b81f0c` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('95yz94a7ls7kz0y0yqimyqjjr84octhz','YTk4M2VhMmY2NWNhNjhlY2I3YWExMDBhMjZhZGFmMjZlOWVjZmJkNzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2014-10-08 02:14:03'),('clkyhed2varkiqhcdqd3t6x1di4s17a3','YTk4M2VhMmY2NWNhNjhlY2I3YWExMDBhMjZhZGFmMjZlOWVjZmJkNzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2014-11-29 03:18:57'),('y716rtl4xeoo1pdzcvjorywvkyeofy0x','YTk4M2VhMmY2NWNhNjhlY2I3YWExMDBhMjZhZGFmMjZlOWVjZmJkNzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2014-10-23 16:40:30');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-12-19 11:45:09
