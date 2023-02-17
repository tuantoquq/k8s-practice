-- MySQL dump 10.13  Distrib 8.0.32, for Linux (x86_64)
--
-- Host: localhost    Database: MasterController
-- ------------------------------------------------------
-- Server version	8.0.32-0ubuntu0.20.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Audit`
--

DROP TABLE IF EXISTS `Audit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Audit` (
  `Id` int NOT NULL,
  `ActionId` int NOT NULL,
  `ActionAt` datetime NOT NULL,
  `UserId` int NOT NULL,
  `MinerId` int NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `fk_Audit_1_idx` (`UserId`),
  KEY `fk_Audit_2_idx` (`MinerId`),
  CONSTRAINT `fk_Audit_1` FOREIGN KEY (`UserId`) REFERENCES `User` (`Id`),
  CONSTRAINT `fk_Audit_2` FOREIGN KEY (`MinerId`) REFERENCES `Miner` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Audit`
--

LOCK TABLES `Audit` WRITE;
/*!40000 ALTER TABLE `Audit` DISABLE KEYS */;
INSERT INTO `Audit` VALUES (1,0,'2023-01-01 00:00:00',326726,1),(661767,0,'2023-02-03 00:00:00',326726,344972);
/*!40000 ALTER TABLE `Audit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Miner`
--

DROP TABLE IF EXISTS `Miner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Miner` (
  `Id` int NOT NULL,
  `DefineUserId` int NOT NULL,
  `UserCanUse` varchar(4000) NOT NULL,
  `CreateAt` datetime NOT NULL,
  `UpdateAt` datetime NOT NULL,
  `Name` varchar(45) NOT NULL,
  `Schedule` varchar(45) NOT NULL,
  `Formula` varchar(4000) NOT NULL,
  `IsActive` tinyint NOT NULL,
  `InputTables` varchar(4000) DEFAULT NULL,
  `RecursiveRange` int DEFAULT NULL,
  `GetInputs` varchar(4000) DEFAULT NULL,
  `IsSuccess` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `fk_Miner_1_idx` (`DefineUserId`),
  CONSTRAINT `fk_Miner_1` FOREIGN KEY (`DefineUserId`) REFERENCES `User` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Miner`
--

LOCK TABLES `Miner` WRITE;
/*!40000 ALTER TABLE `Miner` DISABLE KEYS */;
INSERT INTO `Miner` VALUES (1,326726,'','2023-01-01 00:00:00','2023-01-01 00:00:00','OBV','0 0 * * *','dsasc',1,NULL,NULL,NULL,NULL),(344972,326726,'','2023-02-03 00:00:00','2023-02-03 00:00:00','Duong1','0 0 * * *','print(haha)',1,NULL,NULL,NULL,NULL),(572315,1,'all','2023-02-06 00:00:00','2023-02-06 00:00:00','OBV','0 0 * * *','print(\'OBV update\')',0,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `Miner` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User`
--

DROP TABLE IF EXISTS `User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `User` (
  `Id` int NOT NULL,
  `Name` varchar(45) NOT NULL,
  `Username` varchar(45) NOT NULL,
  `Password` varchar(2000) NOT NULL,
  `Role` int NOT NULL,
  `IsActive` tinyint NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User`
--

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
INSERT INTO `User` VALUES (1,'Duong','Admin','$2b$12$eJUvkDwkO6kSDQsjg1Wr2Oh1gLLYXdQBQAPn6THp5hH0GMBobPgVm',0,1),(326726,'Duongdt','duongdt','$2b$12$yLA3vsypbFloC8DVhkpr6eolyeMClxF.BAq98SJNjFXGd3o.3I4WG',1,1),(394893,'Duonggg','Duonggg','$2b$12$eJUvkDwkO6kSDQsjg1Wr2Oh1gLLYXdQBQAPn6THp5hH0GMBobPgVm',1,1),(422888,'duongne','1235','$2b$12$s5cFx4FXpVmXOmpMiRGmTeFIfWbFPUx/4NnjOgL45UGRsahspuZey',1,1);
/*!40000 ALTER TABLE `User` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-02-06 17:45:33
