CREATE TABLE GIT_COMMIT
  (
		GIT_COMMIT_SYSTEM_NAME VARCHAR(200) NULL,
		GIT_COMMIT_BRANCH_NAME VARCHAR(200) NULL,
		GIT_COMMIT_ID NUMERIC(19,0) NOT NULL,
		GIT_COMMIT_HASH VARCHAR(200) NULL,
		GIT_COMMIT_DATE VARCHAR(200) NULL,
		GIT_COMMIT_AUTHOR VARCHAR(200) NULL,
		GIT_COMMIT_MESSAGE VARCHAR(800) NULL,
		CONSTRAINT GIT_COMMIT_PK PRIMARY KEY (GIT_COMMIT_ID)
	);

CREATE TABLE RALLY_UNIT
	(
		RALLY_UNIT_TYPE VARCHAR(200) NULL,
		GIT_COMMIT_ID NUMERIC(19,0) NOT NULL,
		RALLY_UNIT_ID NUMERIC(19,0) NOT NULL,
		RALLY_UNIT_NUMBER VARCHAR(200) NULL,
		CONSTRAINT RALLY_UNIT_PK PRIMARY KEY (RALLY_UNIT_ID)
	);
	
CREATE TABLE SRC_FILE
	(
		SRC_FILE_ID NUMERIC(19,0) NOT NULL,
		SRC_FILE_NAME VARCHAR(200) NULL,
		GIT_COMMIT_ID NUMERIC(19,0) NOT NULL,
		CONSTRAINT SRC_FILE_PK PRIMARY KEY (SRC_FILE_ID)
	);	

CREATE TABLE SEQ_NUMBER
	(
		SEQ_NUMBER_TYPE VARCHAR(200) NULL,
		SEQ_NUMBER_VALUE NUMERIC(19,0) NULL
	);

INSERT INTO SEQ_NUMBER values('GIT_COMMIT', '0');
INSERT INTO SEQ_NUMBER values('RALLY_UNIT', '0');
INSERT INTO SEQ_NUMBER values('SRC_FILE', '0');
	
commit;