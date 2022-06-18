-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 12, 2022 at 08:13 PM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `my_notes`
--

-- --------------------------------------------------------

--
-- Table structure for table `tb_note`
--

CREATE TABLE `tb_note` (
  `noteId` int(5) NOT NULL,
  `title` varchar(80) NOT NULL,
  `notebookText` longtext NOT NULL,
  `isFavourite` int(1) NOT NULL DEFAULT 0,
  `isSecure` int(1) NOT NULL DEFAULT 0,
  `createdAt` datetime NOT NULL DEFAULT current_timestamp(),
  `lastUpdateAt` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `user_id` int(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `tb_user`
--

CREATE TABLE `tb_user` (
  `user_id` int(3) NOT NULL,
  `name` varchar(35) DEFAULT NULL,
  `emailId` varchar(150) DEFAULT NULL,
  `phoneNumber` varchar(15) DEFAULT NULL,
  `deviceToken` varchar(100) DEFAULT NULL,
  `authToken` varchar(100) DEFAULT NULL,
  `createdAt` datetime NOT NULL DEFAULT current_timestamp(),
  `countryCode` int(11) NOT NULL,
  `otpCode` int(11) NOT NULL,
  `isPhoneVerified` int(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tb_user`
--

INSERT INTO `tb_user` (`user_id`, `name`, `emailId`, `phoneNumber`, `deviceToken`, `authToken`, `createdAt`, `countryCode`, `otpCode`, `isPhoneVerified`) VALUES
(17, 'Mandeep Singh', 'demo@yopmail.com', '9988776655', 'abcdefghijlmnpqrstuvwxyz', NULL, '2022-06-12 22:57:13', 91, 1111, 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tb_note`
--
ALTER TABLE `tb_note`
  ADD PRIMARY KEY (`noteId`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `tb_user`
--
ALTER TABLE `tb_user`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `emailId` (`emailId`,`phoneNumber`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tb_note`
--
ALTER TABLE `tb_note`
  MODIFY `noteId` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `tb_user`
--
ALTER TABLE `tb_user`
  MODIFY `user_id` int(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `tb_note`
--
ALTER TABLE `tb_note`
  ADD CONSTRAINT `tb_note_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `tb_user` (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
