-- MySQL Schema for Task Management System

-- Django built-in user table
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `taskmanager_category` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `color` varchar(7) NOT NULL DEFAULT '#007bff',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `taskmanager_task` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `description` text,
  `status` varchar(20) NOT NULL DEFAULT 'pending',
  `priority` varchar(20) NOT NULL DEFAULT 'medium',
  `due_date` date DEFAULT NULL,
  `category_id` bigint DEFAULT NULL,
  `assigned_to_id` bigint DEFAULT NULL,
  `created_by_id` bigint DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `taskmanager_task_category_id_5d4e3c2f_fk` (`category_id`),
  KEY `taskmanager_task_assigned_to_id_7a8b6c5d_fk` (`assigned_to_id`),
  KEY `taskmanager_task_created_by_id_9e8d7c6b_fk` (`created_by_id`),
  CONSTRAINT `taskmanager_task_category_id_5d4e3c2f_fk` FOREIGN KEY (`category_id`) REFERENCES `taskmanager_category` (`id`) ON DELETE SET NULL,
  CONSTRAINT `taskmanager_task_assigned_to_id_7a8b6c5d_fk` FOREIGN KEY (`assigned_to_id`) REFERENCES `auth_user` (`id`) ON DELETE SET NULL,
  CONSTRAINT `taskmanager_task_created_by_id_9e8d7c6b_fk` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;