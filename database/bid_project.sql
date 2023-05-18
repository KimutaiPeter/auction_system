-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jul 23, 2022 at 08:00 AM
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
-- Database: `bid_project`
--

-- --------------------------------------------------------

--
-- Table structure for table `product_table`
--

CREATE TABLE `product_table` (
  `product_id` int(255) NOT NULL,
  `product_name` varchar(255) NOT NULL,
  `product_market_price` int(255) NOT NULL,
  `product_selling_price` int(255) NOT NULL DEFAULT 0,
  `product_type` varchar(255) NOT NULL,
  `winning_user_id` varchar(11) NOT NULL,
  `time_set_to_start` datetime NOT NULL,
  `time_set_forward` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `product_table`
--

INSERT INTO `product_table` (`product_id`, `product_name`, `product_market_price`, `product_selling_price`, `product_type`, `winning_user_id`, `time_set_to_start`, `time_set_forward`) VALUES
(1, 'Land (Muthaiga)', 10000000, 10011000, 'passive', '6', '2022-07-21 16:45:39', '2022-07-21 23:06:34'),
(3, 'Fried Food', 100, 47100, 'live', '6', '2022-07-21 21:54:57', '2022-07-22 11:09:06'),
(4, 'Watch', 20000, 31000, 'passive', '6', '2022-07-21 23:08:29', '2022-07-22 11:09:49'),
(5, 'Cow', 10000, 76000, 'live', '5', '2022-07-22 17:59:00', '2022-07-22 11:17:05'),
(6, 'Land Runda', 10000000, 10008000, 'passive', '5', '2022-07-22 11:05:45', '2022-07-24 18:06:00'),
(7, 'Some item', 1000, 6000, 'live', '6', '2022-07-23 00:50:41', '2022-07-23 00:51:29'),
(8, 'Fried dd', 1000, 15000, 'live', '6', '2022-07-23 00:57:39', '2022-07-23 01:00:55');

-- --------------------------------------------------------

--
-- Table structure for table `users_one`
--

CREATE TABLE `users_one` (
  `user_id` int(255) NOT NULL,
  `user_name` varchar(255) NOT NULL,
  `user_password` varchar(1000) NOT NULL,
  `Role` varchar(60) NOT NULL DEFAULT 'Client'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users_one`
--

INSERT INTO `users_one` (`user_id`, `user_name`, `user_password`, `Role`) VALUES
(1, 'Boss', '123', 'Admin'),
(5, 'Peter', '123', 'Client'),
(6, 'Someone', '123', 'Client'),
(7, 'Druzu', '12345', 'Client');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `product_table`
--
ALTER TABLE `product_table`
  ADD PRIMARY KEY (`product_id`);

--
-- Indexes for table `users_one`
--
ALTER TABLE `users_one`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `product_table`
--
ALTER TABLE `product_table`
  MODIFY `product_id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `users_one`
--
ALTER TABLE `users_one`
  MODIFY `user_id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
