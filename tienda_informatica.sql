-- phpMyAdmin SQL Dump
-- version 5.2.2deb1+deb13u1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 13-04-2026 a las 12:04:29
-- Versión del servidor: 11.8.6-MariaDB-0+deb13u1 from Debian
-- Versión de PHP: 8.4.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `tienda_informatica`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_venta`
--

CREATE TABLE `detalle_venta` (
  `id` int(11) NOT NULL,
  `id_venta` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio` decimal(10,2) NOT NULL
) ;

--
-- Volcado de datos para la tabla `detalle_venta`
--

INSERT INTO `detalle_venta` (`id`, `id_venta`, `id_producto`, `cantidad`, `precio`) VALUES
(1, 1, 1, 1, 400.00),
(2, 1, 3, 2, 900.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto`
--

CREATE TABLE `producto` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `marca` varchar(50) DEFAULT NULL,
  `tipo` enum('laptop','telefono') NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `stock` int(11) NOT NULL,
  `imagen` varchar(255) DEFAULT NULL,
  `descripcion` text DEFAULT NULL
) ;

--
-- Volcado de datos para la tabla `producto`
--

INSERT INTO `producto` (`id`, `nombre`, `marca`, `tipo`, `precio`, `stock`, `imagen`, `descripcion`) VALUES
(1, 'SAMSUMG GALAXY S23', 'SAMSUNG', 'telefono', 900.00, 26, 'img/samsungGalaxyS23.png', 'pantalla Dynamic AMOLED 2X de 6.1 pulgadas con tasa de refresco de 120Hz, resolución FHD+ y vidrio Gorilla Glass Victus 2, el Galaxy S23 está potenciado por un procesador Snapdragon 8 Gen 2 for Galaxy, una variante del chip de Qualcomm que corre a 3.36GHz, junto con 8GB de RAM y hasta 512GB de almacenamiento interno'),
(2, 'ASUS Chromebook CX1500CKA-NJ0446', 'ASUS', 'laptop', 400.00, 11, 'img/asus.webp', 'El ASUS Chromebook CX1500CKA-NJ0446 está diseñado para ayudarte a ser productivo y divertirte, durante todo el día y dondequiera que estés. Este portátil cuenta con una CPU Intel® de dos núcleos y conectividad Wi-Fi 6 superrápida de doble banda, así como una excelente portabilidad y una autonomía hasta de 11 horas. El diseño de esta serie maximiza el tamaño de la pantalla en un chasis muy compacto, lo que facilita el trabajo multitarea y ofrece una experiencia de entretenimiento más envolvente. El ASUS Chromebook CX1500CKA-NJ0446 te permite acceder a las mejores aplicaciones de trabajo y entretenimiento de Google Play2. Con un rendimiento rápido, sólida seguridad y prácticas funciones'),
(3, 'XIAOMI 13 PRO', 'XIAOMI ', 'telefono', 300.00, 41, 'img/xiaomi 13 pro.avif', 'El Xiaomi 13 Pro es un smartphone de alta gama que cuenta con una pantalla OLED de 6.73 pulgadas, un procesador Snapdragon 8 Gen 2, 12GB de RAM y 256GB o 512GB de almacenamiento interno12. Su cámara trasera es triple, con tres sensores de 50MP cada uno2. Su batería tiene una capacidad de 4820 mAh2'),
(4, 'iPhone 15 Plus', 'Apple', 'telefono', 900.00, 4, 'img/iphone15.png', 'Pantalla Super Retina XDR; Pantalla OLED de 6,7 pulgadas (17 cm) en diagonal; Resolución de 2.796 por 1.290 píxeles a 460 p/p; La pantalla del iPhone 15 Plus tiene esquinas redondeadas que rematan el diseño curvo del dispositivo'),
(5, 'Lenovo ThinkPad E14', 'Lenovo', 'laptop', 850.00, 84, 'img/lenovo.webp', 'Diseñado para el rendimiento profesional diario, la laptop Lenovo ThinkPad E14 viene equipada con potentes procesadores Intel® Core™ de 13.ª generación, ideal para multitareas, con una amplia memoria y almacenamiento rápido, opciones de seguridad estables y una atractiva pantalla de 14\" (35,56 cm), hasta WUXGA+ (2240x1400).'),
(6, 'PcCom Revolt 4060 Ultra 7', 'PcCom ', 'laptop', 1200.00, 62, 'img/pccom.webp', 'Diseñado para ofrecer un rendimiento excepcional a usuarios profesionales y frikis de los videojuegos. Con su poderoso procesador Intel Core Ultra 7 155H y una robusta tarjeta gráfica, este modelo redefine las expectativas de lo que un portátil puede hacer.</p>');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `fullname` varchar(100) DEFAULT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `role` enum('admin','user') DEFAULT 'user'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id`, `username`, `password`, `fullname`, `correo`, `role`) VALUES
(1, 'admin', 'hash_admin', 'Administrador', 'admin@email.com', 'admin'),
(2, 'juan', '$2b$12$wJ8Qe9v7KqVQ6Y0p3vZ1r.OZzQGz8X0lFqY6XQkKX7zP0ZzQx8J8K', 'Juan Pérez', 'juan@email.com', 'user'),
(3, 'pp', 'scrypt:32768:8:1$gpMjzaP8SqR56Mjm$73e368b623122d59f47f09d3165c8d8683b181b9268dde749a97b20b96591965afb5635b92922b36d7895bb7813113fda9e5f4033386e6e11f1e9ea0ff36e659', 'pp', 'pp', 'user'),
(4, 'xxx', 'scrypt:32768:8:1$OvZ5u1qQjFoGJJlR$1a6b3a08e796070464320aa190c35a6175300a54b60bc3de85d307696b2ee8f41e8cbf05009628bda4d3e7a322a8432e36038a7db6f24ad4fb0df2db9abbf0c9', 'xxx', 'xxx', 'user');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `venta`
--

CREATE TABLE `venta` (
  `id` int(11) NOT NULL,
  `fecha` datetime DEFAULT current_timestamp(),
  `id_usuario` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Volcado de datos para la tabla `venta`
--

INSERT INTO `venta` (`id`, `fecha`, `id_usuario`) VALUES
(1, '2026-03-18 09:38:32', 2);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `detalle_venta`
--
ALTER TABLE `detalle_venta`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_venta` (`id_venta`),
  ADD KEY `id_producto` (`id_producto`);

--
-- Indices de la tabla `producto`
--
ALTER TABLE `producto`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indices de la tabla `venta`
--
ALTER TABLE `venta`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `detalle_venta`
--
ALTER TABLE `detalle_venta`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `producto`
--
ALTER TABLE `producto`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `venta`
--
ALTER TABLE `venta`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `detalle_venta`
--
ALTER TABLE `detalle_venta`
  ADD CONSTRAINT `detalle_venta_ibfk_1` FOREIGN KEY (`id_venta`) REFERENCES `venta` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `detalle_venta_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id`);

--
-- Filtros para la tabla `venta`
--
ALTER TABLE `venta`
  ADD CONSTRAINT `venta_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
