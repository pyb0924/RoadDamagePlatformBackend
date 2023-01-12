DROP TABLE IF EXISTS `event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event` (
  `event_id` bigint NOT NULL,
  `type` bigint NOT NULL,
  `longitude` float NOT NULL,
  `latitude` float NOT NULL,
  `position` varchar(45) NOT NULL,
  `status` int NOT NULL,
  PRIMARY KEY (`event_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `event`
--

LOCK TABLES `event` WRITE;
INSERT INTO `event` VALUES (1589544875072819200,1,1.1,1.1,'东川路800号',4),(1589892725715636224,0,20.2,20.2,'东川路2号',2);

UNLOCK TABLES;

--
-- Table structure for table `event_user`
--

DROP TABLE IF EXISTS `event_user`;

CREATE TABLE `event_user` (
  `idevent_user` int NOT NULL AUTO_INCREMENT,
  `event_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`idevent_user`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `event_user`
--

LOCK TABLES `event_user` WRITE;

INSERT INTO `event_user` VALUES (1,1589892725715636224,1589892725715636255);

UNLOCK TABLES;

--
-- Table structure for table `img`
--

DROP TABLE IF EXISTS `img`;

CREATE TABLE `img` (
  `img_id` bigint NOT NULL,
  `log_id` bigint NOT NULL,
  `event_id` bigint NOT NULL,
  PRIMARY KEY (`img_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `img`
--

LOCK TABLES `img` WRITE;

INSERT INTO `img` VALUES (1589544875064430592,1589544875072819200,1589544875072819200),(1589544875072819200,1589544875072819200,1589544875072819200),(1589892725698859008,1589892725715636224,1589892725715636224),(1589892725711441920,1589892725715636224,1589892725715636224),(1590179930493292544,1590179930535235584,1589544875072819200);


--
-- Table structure for table `log`
--

DROP TABLE IF EXISTS `log`;

CREATE TABLE `log` (
  `log_id` bigint NOT NULL,
  `event_id` bigint NOT NULL,
  `datetime` datetime NOT NULL,
  `user` bigint NOT NULL,
  `new_status` int NOT NULL,
  `old_status` int DEFAULT NULL,
  `notes` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`log_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `log`
--

LOCK TABLES `log` WRITE;

INSERT INTO `log` VALUES (1589544875072819200,1589544875072819200,'2022-11-07 17:06:45',987654321,1,NULL,'test'),(1589892725715636224,1589892725715636224,'2022-11-08 16:08:59',987456321,1,NULL,'测试'),(1589895288066281472,1589892725715636224,'2022-11-08 16:19:10',123456789,2,1,'测试'),(1589899140517728256,1589892725715636224,'2022-11-08 16:34:28',123,3,2,'测试'),(1589906029775294464,1589892725715636224,'2022-11-08 17:01:51',132132,4,3,'321321'),(1590179930535235584,1589544875072819200,'2022-11-09 11:10:14',35432135,4,3,'654324357'),(1590294685715402752,1589892725715636224,'2022-11-09 18:46:13',0,2,4,'过热三个人色');

-- Dump completed on 2022-11-20  9:30:33
