-- to excute in sqlite
--   sqlite> .read create_tables.sql

-- Creating tables
-- Turning loggin on

-- .log create_tables.log

-- MAGNITUDE TABLE
-- Deleting table
DROP TABLE IF EXISTS MAGNITUDE;

-- Creating table
CREATE TABLE MAGNITUDE(
	MG_ID CHARACTER(1) NOT NULL,
	MG_CONTENT VARCHAR(64) NOT NULL,
	mg_weight smallint,
	symbol varchar(5) );

-- QUALIFIER TABLE
-- Deleting table
DROP TABLE IF EXISTS EDU_QUAL;

-- Creating table
CREATE TABLE EDU_QUAL(
	MQ_ID char(1) NOT NULL,
	MQ_QUAL varchar(64) NOT NULL,
	qual_weight smallint ,
	symbol varchar(5),
 PRIMARY KEY (MQ_ID ASC));

-- COUNTRY TABLE
-- Deleting table
DROP TABLE IF EXISTS COUNTRY;

-- Creating table
CREATE TABLE COUNTRY(
	CO_CODE int NOT NULL,
	CO_LONG_NAME varchar(60) NOT NULL,
	CO_SHORT_NAME varchar(60) ,
	CO_ABR varchar(6) ,
	CO_ISO_NUM int ,
	CO_ISO_2LETTER char(2) ,
	CO_SHORT_NAME_FR varchar(60) ,
	CO_SHORT_NAME_SP varchar(60) ,
	CO_SHORT_NAME_RU nvarchar(60) ,
	CO_SHORT_NAME_CH nvarchar(60) ,
	CO_SHORT_NAME_AR nvarchar(60) ,
	COUNTRY_YEAR int ,
	OECD_STAT tinyint ,
	MAP_SHORT_NAME varchar(60) ,
	MAP_SHORT_NAME_FR varchar(60) ,
	MAP_SHORT_NAME_SP varchar(60) ,
    PRIMARY KEY (CO_CODE ASC ));

-- REGIONS TABLE
-- Deleting table
DROP TABLE IF EXISTS REGIONS;
-- Creating table
CREATE TABLE REGIONS(
	CO_CODE INT NOT NULL CHECK (CO_CODE>= 0),
	ADM_CODE INT NOT NULL,
    ADM_NAME TEXT NOT NULL,
PRIMARY KEY (CO_CODE ASC,ADM_CODE ASC ));

-- EDU_METER_AID TABLE
-- Deleting table
DROP TABLE IF EXISTS EDU_METER_AID;

-- Creating table
CREATE TABLE EDU_METER_AID(
	EMC_ID int(10) NOT NULL,    -- Numeric coding scheme.
	AC varchar(100),            -- Alphanumeric codeing scheme.
	LABEL_INT_EN varchar(2048) ,
	LABEL_INT_FR varchar(2048) ,
	LABEL_EXT_EN varchar(2048) ,
	LABEL_EXT_FR varchar(2048) ,
    PRIMARY KEY (EMC_ID ASC));

-- EDU_METER97_REP TABLE
-- Deleting table
DROP TABLE IF EXISTS EDU_METER97_REP;

-- Creating table
CREATE TABLE EDU_METER97_REP(
	EMC_ID int(10) NOT NULL,
	CO_CODE int(10) NOT NULL,
    ADM_CODE int(10) NOT NULL, 
	EMCO_YEAR int(4) NOT NULL,
	EAG_AGE int(3) ,    -- not sure what is this : in our case NULL.
	ST_ID int(5) ,      -- SOURCE_TITLE : exported: in our case 1.
	ABE_ID char(1) ,    -- EC_AB_EXPENDITURE: A - Actual : B - Budget: in our case NULL.
	MQ_ID char(1) ,     -- EDU_QUAL: already have the create script.
	MG_ID char(1) ,     -- MAGNITUDE: already have the create script.
	EM_FIG float ,
	EC_TD_ID decimal(3, 0) NOT NULL, -- EC_TYPE_DATA: exported.
	NOTEYESNO char(1) ,              -- in out case NULL.
PRIMARY KEY (EMC_ID ASC,CO_CODE ASC,ADM_CODE ASC, EMCO_YEAR ASC));

-- EDU_METER97_OBS TABLE
-- Deleting table
DROP TABLE IF EXISTS EDU_METER97_OBS;

-- Creating table
CREATE TABLE EDU_METER97_OBS(
	EMC_ID int(10) NOT NULL,
	CO_CODE int(10) NOT NULL,
    ADM_CODE int(10) NOT NULL, 
	EMCO_YEAR int(4) NOT NULL,
	EAG_AGE int(3) ,    -- not sure what is this : in our case NULL.
	ST_ID int(5) ,      -- SOURCE_TITLE : exported: in our case 1.
	ABE_ID char(1) ,    -- EC_AB_EXPENDITURE: A - Actual : B - Budget: in our case NULL.
	MQ_ID char(1) ,     -- EDU_QUAL: already have the create script.
	MG_ID char(1) ,     -- MAGNITUDE: already have the create script.
	EM_FIG float ,
	EC_TD_ID decimal(3, 0) NOT NULL, -- EC_TYPE_DATA: exported.
	NOTEYESNO char(1) ,              -- in out case NULL.
PRIMARY KEY (EMC_ID ASC,CO_CODE ASC,ADM_CODE ASC, EMCO_YEAR ASC));

-- EDU_METER97_EST TABLE
-- Deleting table
DROP TABLE IF EXISTS EDU_METER97_EST;

-- Creating table
CREATE TABLE EDU_METER97_EST(
	EMC_ID int(10) NOT NULL,
	CO_CODE int(10) NOT NULL,
    ADM_CODE int(10) NOT NULL, 
	EMCO_YEAR int(4) NOT NULL,
	EAG_AGE int(3) ,    -- not sure what is this : in our case NULL.
	ST_ID int(5) ,      -- SOURCE_TITLE : exported: in our case 1.
	ABE_ID char(1) ,    -- EC_AB_EXPENDITURE: A - Actual : B - Budget: in our case NULL.
	MQ_ID char(1) ,     -- EDU_QUAL: already have the create script.
	MG_ID char(1) ,     -- MAGNITUDE: already have the create script.
	EM_FIG float ,
	EC_TD_ID decimal(3, 0) NOT NULL, -- EC_TYPE_DATA: exported.
	NOTEYESNO char(1) ,              -- in out case NULL.
PRIMARY KEY (EMC_ID ASC,CO_CODE ASC,ADM_CODE ASC, EMCO_YEAR ASC));


-- EDU_METER97_NonNumeric_REP TABLE
-- Deleting table
DROP TABLE IF EXISTS EDU_METER97_NonNumeric_REP;

-- Creating table
CREATE TABLE EDU_METER97_NonNumeric_REP(
	EMC_ID decimal(19, 0) NOT NULL,
	CO_CODE decimal(6, 0) NOT NULL, 
	EMCO_YEAR decimal(4, 0) NOT NULL,
	EM_Data nvarchar(4000) ,  -- Non numeric data associated with an EMC_ID comment for example.
	EC_TD_ID decimal(3, 0) NOT NULL,
	NOTEYESNO char(1),
 PRIMARY KEY (EMC_ID ASC,CO_CODE ASC,EMCO_YEAR ASC,	EC_TD_ID ASC));

-- EDU_METER97_NonNumeric_OBS TABLE
-- Deleting table
DROP TABLE IF EXISTS EDU_METER97_NonNumeric_OBS;

-- Creating table
CREATE TABLE EDU_METER97_NonNumeric_OBS(
	EMC_ID decimal(19, 0) NOT NULL,
	CO_CODE decimal(6, 0) NOT NULL, 
	EMCO_YEAR decimal(4, 0) NOT NULL,
	EM_Data nvarchar(4000) ,  -- Non numeric data associated with an EMC_ID comment for example.
	EC_TD_ID decimal(3, 0) NOT NULL,
	NOTEYESNO char(1),
 PRIMARY KEY (EMC_ID ASC,CO_CODE ASC,EMCO_YEAR ASC,	EC_TD_ID ASC));

-- EDU_METER97_NonNumeric_EST TABLE
-- Deleting table
DROP TABLE IF EXISTS EDU_METER97_NonNumeric_EST;

-- Creating table
CREATE TABLE EDU_METER97_NonNumeric_EST(
	EMC_ID decimal(19, 0) NOT NULL,
	CO_CODE decimal(6, 0) NOT NULL, 
	EMCO_YEAR decimal(4, 0) NOT NULL,
	EM_Data nvarchar(4000) ,  -- Non numeric data associated with an EMC_ID comment for example.
	EC_TD_ID decimal(3, 0) NOT NULL,
	NOTEYESNO char(1),
 PRIMARY KEY (EMC_ID ASC,CO_CODE ASC,EMCO_YEAR ASC,	EC_TD_ID ASC));

-- RM_Mapping TABLE
-- Deleting table
DROP TABLE IF EXISTS RM_Mapping;
-- Creating table
CREATE TABLE RM_Mapping(
	EMC_ID decimal(19, 0) NOT NULL,
	Tab nvarchar(50)  NOT NULL, -- Sheet name in the questionnaire.
	RM_TABLE  nvarchar(50) NOT NULL, -- Table name and number in the Questionniare
	Col int(10) ,                    -- Col number.
    AC varchar(100),            -- Alphanumeric codeing scheme.
    EXL_REF varchar(10),      -- EXCEL cell address. Firtst cell in the column.
    CUR_YEAR int(2));          -- 0 implies current year, 1 next year, -1 implied previous.

-- RM_Mapping_NonNumeric TABLE
-- Deleting table
DROP TABLE IF EXISTS RM_Mapping_NonNumeric;
-- Creating table
CREATE TABLE RM_Mapping_NonNumeric(
	Tab nvarchar(50)  NOT NULL, -- Sheet name in the questionnaire.
	RM_TABLE  nvarchar(50) NOT NULL, -- Table name and number in the Questionniare
    AC varchar(100),            -- Alphanumeric codeing scheme.
    EXL_REF varchar(10));      -- EXCEL cell address. Firtst cell in the column.

-- EDU_INCLUSION_REP TABLE
-- Deleting table
DROP TABLE IF EXISTS EDU_INCLUSION_REP;
-- Creating table
CREATE TABLE EDU_INCLUSION_REP(
       CO_CODE decimal(6, 0) NOT NULL,
       EMCO_YEAR decimal(4, 0) NOT NULL,
       ADM_CODE INT NOT NULL,
       EMC_ID decimal(6, 0) NOT NULL,
       DESC_INCLU varchar(32),  -- Where the inlcusion code XC and XR exist.
       EC_TD_ID decimal(3, 0) NOT NULL,
PRIMARY KEY ( CO_CODE ASC,  EMCO_YEAR ASC,    EMC_ID ASC, ADM_CODE ASC));


-- EDU_INCLUSION_OBS TABLE
-- Deleting table
DROP TABLE IF EXISTS EDU_INCLUSION_OBS;
-- Creating table
CREATE TABLE EDU_INCLUSION_OBS(
       CO_CODE decimal(6, 0) NOT NULL,
       EMCO_YEAR decimal(4, 0) NOT NULL,
       ADM_CODE INT NOT NULL,
       EMC_ID decimal(6, 0) NOT NULL,
       DESC_INCLU varchar(32),  -- Where the inlcusion code XC and XR exist.
       EC_TD_ID decimal(3, 0) NOT NULL,
PRIMARY KEY ( CO_CODE ASC,  EMCO_YEAR ASC,    EMC_ID ASC, ADM_CODE ASC));

-- EDU_INCLUSION_EST TABLE
-- Deleting table
DROP TABLE IF EXISTS EDU_INCLUSION_EST;
-- Creating table
CREATE TABLE EDU_INCLUSION_EST(
       CO_CODE decimal(6, 0) NOT NULL,
       EMCO_YEAR decimal(4, 0) NOT NULL,
       ADM_CODE INT NOT NULL,
       EMC_ID decimal(6, 0) NOT NULL,
       DESC_INCLU varchar(32),  -- Where the inlcusion code XC and XR exist.
       EC_TD_ID decimal(3, 0) NOT NULL,
PRIMARY KEY ( CO_CODE ASC,  EMCO_YEAR ASC,    EMC_ID ASC, ADM_CODE ASC));

-- EDU_COMMENT_TABLE_REP TABLE
-- Deleting table
DROP TABLE IF EXISTS EDU_COMMENT_TABLE_REP;
-- Creating table
CREATE TABLE EDU_COMMENT_TABLE_REP(
       CO_CODE int NOT NULL,
       EMCO_YEAR smallint NOT NULL,
       WT_NAME varchar(10) NOT NULL, -- Table name.
       COM_DATA varchar(1000) NOT NULL, -- Comment holder.
PRIMARY KEY ( CO_CODE ASC, EMCO_YEAR ASC, WT_NAME ASC));

-- EDU_COMMENT_TABLE_OBS TABLE
-- Deleting table
DROP TABLE IF EXISTS EDU_COMMENT_TABLE_OBS;
-- Creating table
CREATE TABLE EDU_COMMENT_TABLE_OBS(
       CO_CODE int NOT NULL,
       EMCO_YEAR smallint NOT NULL,
       WT_NAME varchar(10) NOT NULL, -- Table name.
       COM_DATA varchar(1000) NOT NULL, -- Comment holder.
PRIMARY KEY ( CO_CODE ASC, EMCO_YEAR ASC, WT_NAME ASC));

-- EDU_COMMENT_TABLE_EST TABLE
-- Deleting table
DROP TABLE IF EXISTS EDU_COMMENT_TABLE_EST;
-- Creating table
CREATE TABLE EDU_COMMENT_TABLE_EST(
       CO_CODE int NOT NULL,
       EMCO_YEAR smallint NOT NULL,
       WT_NAME varchar(10) NOT NULL, -- Table name.
       COM_DATA varchar(1000) NOT NULL, -- Comment holder.
PRIMARY KEY ( CO_CODE ASC, EMCO_YEAR ASC, WT_NAME ASC));


---- EDU_FTN_ASSO97_REP TABLE
---- Deleting table
DROP TABLE IF EXISTS EDU_FTN97_REP;
---- Creating table
CREATE TABLE EDU_FTN97_REP(
	CO_CODE int  NOT NULL,
    ADM_CODE int NOT NULL,
	EMCO_YEAR int NOT NULL,
	EMC_ID int   NOT NULL,
	FTN_CODE int  NOT NULL,
	FTN_DATA varchar(1500),
	NTABLE decimal(2, 0) NOT NULL, -- Table numbe is 1.1, 1.2, ...
	QUESTNAME char(1) NOT NULL,
	USERNAME varchar(255),
	DATE_ADDED DATETIME DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY (CO_CODE ASC, ADM_CODE ASC,  EMCO_YEAR ASC, EMC_ID ASC ));


---- EDU_FTN_ASSO97_OBS TABLE
---- Deleting table
DROP TABLE IF EXISTS EDU_FTN97_OBS;
---- Creating table
CREATE TABLE EDU_FTN97_OBS(
	CO_CODE int  NOT NULL,
    ADM_CODE int NOT NULL,
	EMCO_YEAR int NOT NULL,
	EMC_ID int   NOT NULL,
	FTN_CODE int  NOT NULL,
	FTN_DATA varchar(1500),
	NTABLE decimal(2, 0) NOT NULL, -- Table numbe is 1.1, 1.2, ...
	QUESTNAME char(1) NOT NULL,
	USERNAME varchar(255),
	DATE_ADDED datetime DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY (CO_CODE ASC, ADM_CODE ASC,  EMCO_YEAR ASC, EMC_ID ASC ));

---- EDU_FTN_ASSO97_EST TABLE
---- Deleting table
DROP TABLE IF EXISTS EDU_FTN97_EST;
---- Creating table
CREATE TABLE EDU_FTN97_EST(
	CO_CODE int  NOT NULL,
    ADM_CODE int NOT NULL,
	EMCO_YEAR int NOT NULL,
	EMC_ID int   NOT NULL,
	FTN_CODE int  NOT NULL,
	FTN_DATA varchar(1500),
	NTABLE decimal(2, 0) NOT NULL, -- Table numbe is 1.1, 1.2, ...
	QUESTNAME char(1) NOT NULL,
	USERNAME varchar(255),
	DATE_ADDED datetime DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY (CO_CODE ASC, ADM_CODE ASC,  EMCO_YEAR ASC, EMC_ID ASC ));

-- -- EDU_FTN_ASSO97_OBS TABLE
-- -- Deleting table
-- DROP TABLE IF EXISTS EDU_FTN_ASSO97_OBS
-- -- Creating table
-- CREATE TABLE EDU_FTN_ASSO97_OBS(
-- 	EF_ID decimal(6, 0) NOT NULL,
-- 	CO_CODE int NOT NULL,
-- 	EMC_ID int NOT NULL,
-- 	EMCO_YEAR int NOT NULL,
-- 	EC_TD_ID int NOT NULL,
-- 	USERNAME varchar(255) ,
-- 	DATE_ADDED datetime ,
--  PRIMARY KEY (EF_ID ASC, CO_CODE ASC, EMC_ID ASC, EMCO_YEAR ASC,EC_TD_ID ASC))

-- -- EDU_FTN97_2004 TABLE
-- -- Deleting table
-- DROP TABLE IF EXISTS EDU_FTN97_2004
-- -- Creating table
-- CREATE TABLE EDU_FTN97_2004(
-- 	CatCode smallint ,
-- 	SubCatCode smallint ,
-- 	EF_ID decimal(6, 0) NOT NULL,
-- 	EF_FTN nvarchar(500) ,
-- 	EF_FTN_FR nvarchar(500) ,
-- 	EF_FTN_SP nvarchar(500) ,
-- 	FootEstFlag tinyint NOT NULL,
-- 	EF_FTN_RU nvarchar(500) ,
-- 	EF_FTN_AR nvarchar(500) ,
--     PRIMARY KEY (EF_ID ASC))
