CREATE TABLE last_sync_snapshot (id INTEGER PRIMARY KEY	,isdir TINYINT	,size INT ,fileversion	INT	,sha1 VARCHAR(42)	,svrparentid VARCHAR(260)	COLLATE NOCASE	,svrid VARCHAR(260) 	COLLATE NOCASE	,localpath		VARCHAR(260)	COLLATE NOCASE	,localname		VARCHAR(260)	COLLATE NOCASE	,local_mtime	DATETIME						,local_ctime	DATETIME						,opver			INT				DEFAULT		-1	);