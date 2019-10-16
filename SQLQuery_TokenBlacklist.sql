USE BIZMAN
GO

IF OBJECT_ID('BIZMAN.dbo.token_blacklist', 'U') IS NOT NULL
  DROP TABLE token_blacklist; 
GO
CREATE TABLE token_blacklist(
   id INT IDENTITY(1,1) PRIMARY KEY,
   jti NVARCHAR(36) NOT NULL,
   token_type  NVARCHAR(10) NOT NULL,
   user_identity  NVARCHAR(50) NOT NULL,
   revoked TINYINT NOT NULL,
   expires DATETIME NOT NULL,
);