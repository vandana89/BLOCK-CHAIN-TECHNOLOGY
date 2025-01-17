/*
SQLyog Enterprise - MySQL GUI v6.56
MySQL - 5.5.5-10.4.21-MariaDB : Database - charity
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`charity` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `charity`;

/*Table structure for table `charityinformation` */

DROP TABLE IF EXISTS `charityinformation`;

CREATE TABLE `charityinformation` (
  `Slno` int(100) NOT NULL AUTO_INCREMENT,
  `Charityname` varchar(200) DEFAULT NULL,
  `Charityemail` varchar(200) DEFAULT NULL,
  `Charitypassword` varchar(200) DEFAULT NULL,
  `Charityaddress` varchar(200) DEFAULT NULL,
  `Charitycontact` varchar(200) DEFAULT NULL,
  `status` varchar(200) DEFAULT NULL,
  `previous_hash` varchar(200) DEFAULT NULL,
  `present_hash` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`Slno`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

/*Data for the table `charityinformation` */

insert  into `charityinformation`(`Slno`,`Charityname`,`Charityemail`,`Charitypassword`,`Charityaddress`,`Charitycontact`,`status`) values (1,'homealone','homealone@gmail.com','1234','kadapa','4587256987','pending');

/*Table structure for table `donation` */

DROP TABLE IF EXISTS `donation`;

CREATE TABLE `donation` (
  `Slno` int(200) NOT NULL AUTO_INCREMENT,
  `Charityname` varchar(200) DEFAULT NULL,
  `Charityemail` varchar(200) DEFAULT NULL,
  `Charityaddress` varchar(200) DEFAULT NULL,
  `Useremail` varchar(200) DEFAULT NULL,
  `status` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`Slno`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

/*Data for the table `donation` */

insert  into `donation`(`Slno`,`Charityname`,`Charityemail`,`Charityaddress`,`Useremail`,`status`) values (1,'homealone','homealone@gmail.com','kadapa','kumar@gmail.com','accept');

/*Table structure for table `transactiondetails` */

DROP TABLE IF EXISTS `transactiondetails`;

CREATE TABLE `transactiondetails` (
  `Id` int(200) NOT NULL AUTO_INCREMENT,
  `Charityemail` varchar(200) DEFAULT NULL,
  `CharityaccountNumber` varchar(200) DEFAULT NULL,
  `charityifsccode` varchar(200) DEFAULT NULL,
  `Userename` varchar(200) DEFAULT NULL,
  `usercardnumber` varchar(200) DEFAULT NULL,
  `expiredate` varchar(200) DEFAULT NULL,
  `cvv` varchar(200) DEFAULT NULL,
  `amount` varchar(200) DEFAULT NULL,
  `status` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

/*Data for the table `transactiondetails` */

insert  into `transactiondetails`(`Id`,`Charityemail`,`CharityaccountNumber`,`charityifsccode`,`Userename`,`usercardnumber`,`expiredate`,`cvv`,`amount`,`status`) values (1,'homealone@gmail.com','1245689758','IDINp906',NULL,NULL,NULL,NULL,NULL,'pending'),(2,'homealone@gmail.com','1245689758','IDINp906','KUMAR VALLAPUDI','84578546985','12/06','125','5000',NULL);

/*Table structure for table `userinformation` */

DROP TABLE IF EXISTS `userinformation`;

CREATE TABLE `userinformation` (
  `Id` int(200) NOT NULL AUTO_INCREMENT,
  `Username` varchar(200) DEFAULT NULL,
  `useremail` varchar(200) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  `age` varchar(200) DEFAULT NULL,
  `contact` varchar(200) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  `Status` varchar(200) DEFAULT NULL,
  `previous_hash` varchar(200) DEFAULT NULL,
  `present_hash` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

/*Data for the table `userinformation` */

insert  into `userinformation`(`Id`,`Username`,`useremail`,`password`,`age`,`contact`,`address`,`Status`) values (1,'kumar','kumar@gmail.com','1234','25','4587256987','kadapa','pending');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
