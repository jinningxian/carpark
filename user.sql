-- MySQL Script generated by MySQL Workbench
-- Wed Feb 23 14:57:09 2022
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema assignment
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `assignment` ;

-- -----------------------------------------------------
-- Schema assignment
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `assignment` DEFAULT CHARACTER SET utf8 ;
USE `assignment` ;

-- -----------------------------------------------------
-- Table `assignment`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `assignment`.`user` ;

CREATE TABLE IF NOT EXISTS `assignment`.`user` (
  `email` VARCHAR(256) NOT NULL,
  `password` VARCHAR(32) NOT NULL,
  `first_name` VARCHAR(256) NOT NULL,
  `last_name` VARCHAR(256) NOT NULL,
  `contact_num` VARCHAR(32) NULL,
  PRIMARY KEY (`email`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
