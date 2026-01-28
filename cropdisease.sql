/*
 Navicat Premium Data Transfer

 Source Server         : 林枫
 Source Server Type    : MySQL
 Source Server Version : 90000 (9.0.0)
 Source Host           : localhost:3306
 Source Schema         : cropdisease

 Target Server Type    : MySQL
 Target Server Version : 90000 (9.0.0)
 File Encoding         : 65001

 Date: 14/01/2025 16:29:41
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for camerarecords
-- ----------------------------
DROP TABLE IF EXISTS `camerarecords`;
CREATE TABLE `camerarecords`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `weight` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `conf` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `start_time` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `out_video` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `kind` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 34 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of camerarecords
-- ----------------------------
INSERT INTO `camerarecords` VALUES (33, 'rice_best.pt', '0.45', 'admin', '2025-01-14 16:22:31', 'http://localhost:9999/files/d7846c7eba244350bdebe55e09c200e3_output.mp4', 'rice');

-- ----------------------------
-- Table structure for imgrecords
-- ----------------------------
DROP TABLE IF EXISTS `imgrecords`;
CREATE TABLE `imgrecords`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `input_img` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `out_img` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `confidence` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `all_time` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `conf` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `weight` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `start_time` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `label` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `kind` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 146 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of imgrecords
-- ----------------------------
INSERT INTO `imgrecords` VALUES (134, 'http://localhost:9999/files/15f11b07430545558f7fe3ce5f1914e5_corn.jpg', 'http://localhost:9999/files/89953f261f42498086f2ed71d1d31ef7_result.jpg', '[\"70.56%\"]', '0.581秒', '0.39', 'corn_best.pt', 'admin', '2025-01-14 16:19:41', '[\"blight\\uff08\\u75ab\\u75c5\\uff09\"]', 'corn');
INSERT INTO `imgrecords` VALUES (135, 'http://localhost:9999/files/90e9224106d04a8ebc588f37156c38ef_corn1.jpg', 'http://localhost:9999/files/9452be66442e44f3b321f71fe5177050_result.jpg', '[\"98.24%\"]', '0.167秒', '0.39', 'corn_best.pt', 'admin', '2025-01-14 16:19:50', '[\"common_rust\\uff08\\u666e\\u901a\\u9508\\u75c5\\uff09\"]', 'corn');
INSERT INTO `imgrecords` VALUES (136, 'http://localhost:9999/files/e1303da6b4f14faa9636d38d6e72dafd_corn2.jpg', 'http://localhost:9999/files/6fab7365369d4877bda3644446f152b8_result.jpg', '[\"50.49%\"]', '0.238秒', '0.39', 'corn_best.pt', 'admin', '2025-01-14 16:19:54', '[\"common_rust\\uff08\\u666e\\u901a\\u9508\\u75c5\\uff09\"]', 'corn');
INSERT INTO `imgrecords` VALUES (137, 'http://localhost:9999/files/42b5dfb612ba4539851008dd447d0115_rice.png', 'http://localhost:9999/files/242e9a07e05b4bcc91d4a8e36c808456_result.jpg', '[\"76.76%\", \"55.66%\", \"55.47%\", \"55.18%\", \"54.88%\"]', '0.168秒', '0.51', 'rice_best.pt', 'admin', '2025-01-14 16:20:02', '[\"Rice_Blast\\uff08\\u7a3b\\u761f\\u75c5\\uff09\", \"Rice_Blast\\uff08\\u7a3b\\u761f\\u75c5\\uff09\", \"Rice_Blast\\uff08\\u7a3b\\u761f\\u75c5\\uff09\", \"Rice_Blast\\uff08\\u7a3b\\u761f\\u75c5\\uff09\", \"Rice_Blast\\uff08\\u7a3b\\u761f\\u75c5\\uff09\"]', 'rice');
INSERT INTO `imgrecords` VALUES (138, 'http://localhost:9999/files/bdccb0163b5c4f9d9a83bfa6b4a2e391_rice4.jpg', 'http://localhost:9999/files/ffcc3a22b15643ffa0f8885eebe3371a_result.jpg', '[\"80.42%\"]', '0.491秒', '0.51', 'rice_best.pt', 'admin', '2025-01-14 16:20:11', '[\"Rice_Blast\\uff08\\u7a3b\\u761f\\u75c5\\uff09\"]', 'rice');
INSERT INTO `imgrecords` VALUES (139, 'http://localhost:9999/files/bdccb0163b5c4f9d9a83bfa6b4a2e391_rice4.jpg', 'http://localhost:9999/files/908a2dfcd2ea47e8a5b1b2d28eeec336_result.jpg', '[\"80.42%\", \"50.10%\"]', '0.200秒', '0.2', 'rice_best.pt', 'admin', '2025-01-14 16:20:19', '[\"Rice_Blast\\uff08\\u7a3b\\u761f\\u75c5\\uff09\", \"Rice_Blast\\uff08\\u7a3b\\u761f\\u75c5\\uff09\"]', 'rice');
INSERT INTO `imgrecords` VALUES (140, 'http://localhost:9999/files/b8d712c6bb6041608d86e323a47efeaf_stawberry1.jpg', 'http://localhost:9999/files/b5eeebc7c0094ede842a7b754579f37b_result.jpg', '[\"87.11%\"]', '0.172秒', '0.44', 'strawberry_best.pt', 'admin', '2025-01-14 16:20:34', '[\"Angular Leafspot\\uff08\\u89d2\\u6591\\u75c5\\uff09\"]', 'strawberry');
INSERT INTO `imgrecords` VALUES (141, 'http://localhost:9999/files/53ea2091afe74d108d5c490efbf53c3b_stawberry3.jpg', 'http://localhost:9999/files/29036f7b8f8847a1924cc3c04e6cd938_result.jpg', '[\"93.12%\"]', '0.201秒', '0.44', 'strawberry_best.pt', 'admin', '2025-01-14 16:20:39', '[\" Anthracnose Fruit Rot\\uff08\\u70ad\\u75bd\\u679c\\u8150\\u75c5\\uff09\"]', 'strawberry');
INSERT INTO `imgrecords` VALUES (142, 'http://localhost:9999/files/c33c8a9fbd644c1b9c16d52aa25a1aef_stawberry4.jpg', 'http://localhost:9999/files/2c8e8745ffc34de39b87ea41d5737f6e_result.jpg', '[\"96.19%\", \"95.02%\"]', '0.177秒', '0.44', 'strawberry_best.pt', 'admin', '2025-01-14 16:20:43', '[\"Blossom Blight\\uff08\\u82b1\\u67af\\u75c5\\uff09\", \"Blossom Blight\\uff08\\u82b1\\u67af\\u75c5\\uff09\"]', 'strawberry');
INSERT INTO `imgrecords` VALUES (143, 'http://localhost:9999/files/6e2837ffb2b24915829233c9bbcc336d_stawberry5.jpg', 'http://localhost:9999/files/8ddbfb805a164b0fa09c476ecb0bee5b_result.jpg', '[\"89.01%\", \"52.15%\", \"49.12%\"]', '0.189秒', '0.44', 'strawberry_best.pt', 'admin', '2025-01-14 16:20:47', '[\"Gray Mold\\uff08\\u7070\\u9709\\u75c5\\uff09\", \"Gray Mold\\uff08\\u7070\\u9709\\u75c5\\uff09\", \"Gray Mold\\uff08\\u7070\\u9709\\u75c5\\uff09\"]', 'strawberry');
INSERT INTO `imgrecords` VALUES (144, 'http://localhost:9999/files/f2bb0fe927734a5e88a1c1e4cca8bea0_tomato1.jpg', 'http://localhost:9999/files/09400803083f4587a06d71ae6e1a50d2_result.jpg', '[\"84.96%\", \"79.64%\", \"77.59%\", \"50.59%\", \"46.58%\"]', '0.251秒', '0.44', 'tomato_best.pt', 'admin', '2025-01-14 16:20:55', '[\"Late Blight\\uff08\\u665a\\u75ab\\u75c5\\uff09\", \"Late Blight\\uff08\\u665a\\u75ab\\u75c5\\uff09\", \"Late Blight\\uff08\\u665a\\u75ab\\u75c5\\uff09\", \"Late Blight\\uff08\\u665a\\u75ab\\u75c5\\uff09\", \"Late Blight\\uff08\\u665a\\u75ab\\u75c5\\uff09\"]', 'tomato');
INSERT INTO `imgrecords` VALUES (145, 'http://localhost:9999/files/b8e0fbdfe77e4348827fb5d01855d20f_tomato4.jpg', 'http://localhost:9999/files/f7661c9a02174c36993012d534583524_result.jpg', '[\"96.14%\", \"86.52%\", \"84.57%\", \"81.45%\", \"71.24%\", \"50.29%\"]', '0.169秒', '0.44', 'tomato_best.pt', 'admin', '2025-01-14 16:20:59', '[\"Leaf Miner\\uff08\\u6f5c\\u53f6\\u75c5\\uff09\", \"Healthy\\uff08\\u5065\\u5eb7\\uff09\", \"Healthy\\uff08\\u5065\\u5eb7\\uff09\", \"Leaf Miner\\uff08\\u6f5c\\u53f6\\u75c5\\uff09\", \"Healthy\\uff08\\u5065\\u5eb7\\uff09\", \"Healthy\\uff08\\u5065\\u5eb7\\uff09\"]', 'tomato');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `sex` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `tel` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `role` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `time` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = 'Table \'.\\demo\\user\' is marked as crashed and should be repaired' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, 'admin', 'admin', '张三', '男', '123@qq.com', '1234567889', 'admin', 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif', NULL);
INSERT INTO `user` VALUES (2, '123', '123', '张三', '男', '123@qq.com', '1234567889', 'common', 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif', NULL);

-- ----------------------------
-- Table structure for videorecords
-- ----------------------------
DROP TABLE IF EXISTS `videorecords`;
CREATE TABLE `videorecords`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `input_video` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `out_video` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `start_time` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `conf` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `weight` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `kind` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 60 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of videorecords
-- ----------------------------
INSERT INTO `videorecords` VALUES (59, 'http://localhost:9999/files/2959be5a3711409ba0d9ba23275b4acd_QQ2025114-14418-HD.mp4', 'http://localhost:9999/files/f11c80bc1b2944538fad29cabd835586_output.mp4', 'admin', '2025-01-14 16:21:41', '0.41', 'corn_best.pt', 'corn');

SET FOREIGN_KEY_CHECKS = 1;
