-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 12, 2024 at 02:09 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `finalproj`
--

-- --------------------------------------------------------

--
-- Table structure for table `path_info`
--

CREATE TABLE `path_info` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  `photo` varchar(255) DEFAULT NULL,
  `date_uploaded` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `path_info`
--

INSERT INTO `path_info` (`id`, `user_id`, `location`, `status`, `photo`, `date_uploaded`) VALUES
(1, NULL, 'Coliat, Ibaan, Batangas', 'Closed', 'D:/Pictures/449345174_25968442179469162_6962026000072799512_n.png', '2024-11-29 12:54:26'),
(4, NULL, 'Quilo, Ibaan, Batangas', 'Closed', 'D:/Pictures/449345174_25968442179469162_6962026000072799512_n.png', '2024-12-01 10:56:15'),
(5, NULL, 'Bago, Ibaan, Batangas', 'Closed', 'D:/Pictures/432488592_936881215106158_1906874163671835773_n.jpg', '2024-12-01 10:56:24'),
(6, NULL, 'Sabang, Ibaan, Batangas', 'Under Maintenance', 'D:/Pictures/459532485_1061105685385714_4457560107485823778_n.jpg', '2024-12-01 10:56:55'),
(7, NULL, 'Poblacion, Ibaan, Batangas', 'Closed', 'D:/Pictures/462577451_1032289238909100_2523837986019933962_n.png', '2024-12-01 10:57:25'),
(8, NULL, 'Talaibon, Ibaan, Batangas', 'Closed', 'D:/Pictures/Wallpaper/1i918gwz1gl61.png', '2024-12-01 10:58:16');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`) VALUES
(1, 'Brent Draniel Aclan', 'brentaclan@gmail.com', 'c39e52d3a2ed84ddcede6c24a9ba8904c2af747e6fea0b8c094794f807f6d3d2'),
(3, 'John Pathfinder', 'pathfinder@yahoo.com', 'a0af9f865bf637e6736817f4ce552e4cdf7b8c36ea75bc254c1d1f0af744b5bf'),
(5, 'Christian Josh Javier', 'cjj@gmail.com', 'af7961f5d4f758b0626a1ec1cf934ac09880e37c76488297b62acaff231995ab'),
(6, 'Jiro Dino Carag', 'dinonuggets@gmail.com', '8fbefc95205d5645b24823f75d1935b607af6fd3ff792b14d74db9241c43c884'),
(8, 'Brent Draniel Aclan', 'okokok@gmail.com', 'c39e52d3a2ed84ddcede6c24a9ba8904c2af747e6fea0b8c094794f807f6d3d2'),
(21, 'John Doe', 'johndoe@gmail.com', '5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `path_info`
--
ALTER TABLE `path_info`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `path_info`
--
ALTER TABLE `path_info`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `path_info`
--
ALTER TABLE `path_info`
  ADD CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `path_info_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
