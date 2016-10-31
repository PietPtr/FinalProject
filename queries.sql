-- For resetting the database
DROP TABLE IF EXISTS Accounts;
DROP TABLE IF EXISTS Cards;
DROP TABLE IF EXISTS Food;
DROP TABLE IF EXISTS Matches;
DROP TABLE IF EXISTS Orders;

CREATE TABLE `Accounts` (
	`AID`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`Balance`	INTEGER,
	`Active`	INTEGER,
	`Payed`	INTEGER
);

CREATE TABLE `Cards` (
	`CID`	INTEGER,
	`Identifier`	NUMERIC,
	PRIMARY KEY(`CID`)
);

CREATE TABLE `Food` (
	`FID`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`Name`	TEXT,
	`Description`	TEXT,
	`Price`	NUMERIC
);

CREATE TABLE `Matches` (
	`CID`	INTEGER,
	`AID`	INTEGER
);

CREATE TABLE `Orders` (
	`Order_ID`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`CID`	INTEGER,
	`FID`	INTEGER,
	`Done`	INTEGER
);

--For inserting new foods
INSERT INTO Food (Name, Description, Price)
VALUES ([some name], [some description], [some price]);

-- For inserting new orders
INSERT INTO Orders (CID, FID, Done)
VALUES ((
  SELECT Cards.CID
  FROM Cards
  WHERE Cards.Identifier = [the scanned thing]),
  [some food ID], 0);

-- For finishing Orders
UPDATE Orders
SET Done = 1
WHERE Orders.Order_ID = [order thats finished];

-- For updating Balance
UPDATE Accounts
SET Balance = (
  SELECT total(Food.Price)
  FROM Food, Orders, Matches, Accounts
  WHERE Food.FID = Orders.FID
  AND Orders.CID = Matches.CID
  AND Matches.AID = Accounts.AID
  AND Accounts.Active = 1
  )
WHERE Cards.Identifier = [card of paying customer];

-- For creating Accounts
INSERT INTO Accounts (Balance, Active, Payed)
VALUES (0, 1, 0);

-- For adding Cards
INSERT INTO Cards (Identifier)
VALUES ([the serial of an approved card]);

-- For matching Cards + Accounts
INSERT INTO Matches (CID, AID)
VALUES ([some card id], [some account id]);

-- For Checkout
UPDATE Accounts
SET Accounts.Payed = 1
  WHERE Cards.Identifier = [the thing thats scanned]
  AND Cards.CID = Matches.CID
  AND Matches.AID = Accounts.AID
  AND Accounts.Active = 1;

-- For deactivating Accounts
UPDATE Accounts
SET Accounts.Active = 0
  WHERE Accounts.Payed = 1;
