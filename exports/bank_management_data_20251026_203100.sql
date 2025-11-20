-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: bank_management
-- ------------------------------------------------------
-- Server version	8.0.43

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
-- Dumping data for table `account`
--

LOCK TABLES `account` WRITE;
/*!40000 ALTER TABLE `account` DISABLE KEYS */;
INSERT INTO `account` VALUES ('A001',15000.00,'Downtown Branch'),('A002',22000.00,'West Side Branch'),('A003',18500.00,'North Branch'),('A004',12000.00,'South Branch'),('A005',25000.00,'Central Branch'),('A006',19500.00,'East Branch'),('A007',16000.00,'Metro Branch'),('A008',28000.00,'Coastal Branch'),('A009',21000.00,'Uptown Branch'),('A010',24500.00,'Valley Branch');
/*!40000 ALTER TABLE `account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `accounts`
--

LOCK TABLES `accounts` WRITE;
/*!40000 ALTER TABLE `accounts` DISABLE KEYS */;
INSERT INTO `accounts` VALUES (1,1,'Savings',1001000.00,'active','2025-10-26 14:41:50'),(2,1,'Fixed Deposit',500000000.00,'active','2025-10-26 14:50:09');
/*!40000 ALTER TABLE `accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `atm_transactions`
--

LOCK TABLES `atm_transactions` WRITE;
/*!40000 ALTER TABLE `atm_transactions` DISABLE KEYS */;
/*!40000 ALTER TABLE `atm_transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `beneficiaries`
--

LOCK TABLES `beneficiaries` WRITE;
/*!40000 ALTER TABLE `beneficiaries` DISABLE KEYS */;
INSERT INTO `beneficiaries` VALUES (1,1,1,'abc','1234567','canara bank','urfhuyg','friend','2025-10-26 14:57:17');
/*!40000 ALTER TABLE `beneficiaries` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `borrower`
--

LOCK TABLES `borrower` WRITE;
/*!40000 ALTER TABLE `borrower` DISABLE KEYS */;
INSERT INTO `borrower` VALUES ('C001','L001'),('C002','L002'),('C003','L003'),('C004','L004'),('C005','L005'),('C006','L006'),('C007','L007'),('C008','L008'),('C009','L009'),('C010','L010');
/*!40000 ALTER TABLE `borrower` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `branch`
--

LOCK TABLES `branch` WRITE;
/*!40000 ALTER TABLE `branch` DISABLE KEYS */;
INSERT INTO `branch` VALUES ('Central Branch','Phoenix',2900000.00),('Coastal Branch','San Diego',4100000.00),('Downtown Branch','New York',5000000.00),('East Branch','Philadelphia',3500000.00),('Metro Branch','San Antonio',2700000.00),('North Branch','Chicago',3800000.00),('South Branch','Houston',3200000.00),('Uptown Branch','Dallas',3300000.00),('Valley Branch','San Jose',3900000.00),('West Side Branch','Los Angeles',4500000.00);
/*!40000 ALTER TABLE `branch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `branches`
--

LOCK TABLES `branches` WRITE;
/*!40000 ALTER TABLE `branches` DISABLE KEYS */;
INSERT INTO `branches` VALUES (1,'Main Branch','BR001','123 Main Street','Bangalore','Karnataka','1234567890','main.branch@bank.com',NULL,'2025-10-26 14:53:42');
/*!40000 ALTER TABLE `branches` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `credit_cards`
--

LOCK TABLES `credit_cards` WRITE;
/*!40000 ALTER TABLE `credit_cards` DISABLE KEYS */;
INSERT INTO `credit_cards` VALUES (1,1,'7539989347027708','Silver','2030-10-25',200000.00,0.00,'active','2025-10-26 14:55:17');
/*!40000 ALTER TABLE `credit_cards` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES ('C001','John Smith','123 Main Street','New York'),('C002','Emily Johnson','456 Oak Avenue','Los Angeles'),('C003','Michael Brown','789 Pine Road','Chicago'),('C004','Sarah Davis','321 Elm Street','Houston'),('C005','David Wilson','654 Maple Drive','Phoenix'),('C006','Jennifer Martinez','987 Cedar Lane','Philadelphia'),('C007','Robert Anderson','147 Birch Court','San Antonio'),('C008','Lisa Taylor','258 Walnut Place','San Diego'),('C009','James Thomas','369 Spruce Way','Dallas'),('C010','Mary Jackson','741 Ash Boulevard','San Jose');
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,'abc','1234 avenue street','1234567867','aaa@gmail.com','1234','2025-10-26 14:41:10');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `depositor`
--

LOCK TABLES `depositor` WRITE;
/*!40000 ALTER TABLE `depositor` DISABLE KEYS */;
INSERT INTO `depositor` VALUES ('C001','A001'),('C002','A002'),('C003','A003'),('C004','A004'),('C005','A005'),('C006','A006'),('C007','A007'),('C008','A008'),('C009','A009'),('C010','A010');
/*!40000 ALTER TABLE `depositor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `employee`
--

LOCK TABLES `employee` WRITE;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
INSERT INTO `employee` VALUES ('E001','William Clark','555-0101','2020-01-15','Downtown Branch'),('E002','Patricia Lewis','555-0102','2019-03-22','West Side Branch'),('E003','Christopher Walker','555-0103','2021-06-10','North Branch'),('E004','Barbara Hall','555-0104','2018-09-05','South Branch'),('E005','Daniel Allen','555-0105','2022-02-14','Central Branch'),('E006','Nancy Young','555-0106','2020-11-30','East Branch'),('E007','Matthew King','555-0107','2019-07-18','Metro Branch'),('E008','Susan Wright','555-0108','2021-04-25','Coastal Branch'),('E009','Joseph Lopez','555-0109','2020-08-12','Uptown Branch'),('E010','Jessica Hill','555-0110','2022-01-08','Valley Branch');
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `employees`
--

LOCK TABLES `employees` WRITE;
/*!40000 ALTER TABLE `employees` DISABLE KEYS */;
/*!40000 ALTER TABLE `employees` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `fixed_deposits`
--

LOCK TABLES `fixed_deposits` WRITE;
/*!40000 ALTER TABLE `fixed_deposits` DISABLE KEYS */;
INSERT INTO `fixed_deposits` VALUES (1,1,1000.00,6.00,12,'2025-10-26','2026-10-21','active','2025-10-26 14:55:36');
/*!40000 ALTER TABLE `fixed_deposits` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `loan`
--

LOCK TABLES `loan` WRITE;
/*!40000 ALTER TABLE `loan` DISABLE KEYS */;
INSERT INTO `loan` VALUES ('L001',250000.00,'Downtown Branch'),('L002',180000.00,'West Side Branch'),('L003',320000.00,'North Branch'),('L004',150000.00,'South Branch'),('L005',200000.00,'Central Branch'),('L006',275000.00,'East Branch'),('L007',190000.00,'Metro Branch'),('L008',310000.00,'Coastal Branch'),('L009',225000.00,'Uptown Branch'),('L010',285000.00,'Valley Branch');
/*!40000 ALTER TABLE `loan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `loans`
--

LOCK TABLES `loans` WRITE;
/*!40000 ALTER TABLE `loans` DISABLE KEYS */;
INSERT INTO `loans` VALUES (3,1,1,'Home',100000.00,8.50,6,'2025-10-26','2026-04-24','pending',NULL,'2025-10-26 14:54:22');
/*!40000 ALTER TABLE `loans` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `notifications`
--

LOCK TABLES `notifications` WRITE;
/*!40000 ALTER TABLE `notifications` DISABLE KEYS */;
/*!40000 ALTER TABLE `notifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `payment`
--

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
INSERT INTO `payment` VALUES ('P001','L001','2024-01-15',2500.00),('P002','L002','2024-02-10',1800.00),('P003','L003','2024-03-05',3200.00),('P004','L004','2024-04-12',1500.00),('P005','L005','2024-05-20',2000.00),('P006','L006','2024-06-18',2750.00),('P007','L007','2024-07-22',1900.00),('P008','L008','2024-08-14',3100.00),('P009','L009','2024-09-08',2250.00),('P010','L010','2024-10-01',2850.00);
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` VALUES (1,1,'deposit',1000000.00,'Initial deposit','2025-10-26 14:41:50'),(2,1,'deposit',1000.00,'i want to deposit this amount','2025-10-26 14:44:57'),(3,2,'deposit',500000000.00,'Initial deposit','2025-10-26 14:50:09');
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-26 20:31:01
