import sqlite3

# SQLite DB Name
DB_Name =  "ccdb.db"

# SQLite DB Table Schema
TableSchema="""
drop table if exists cloudifin_testHosts;
create table cloudifin_testHosts (
  ID_cloud text,
  Service text,
  Host text,
  Zone text,
  Status text,
  State text,
  Updated text
);
drop table if exists cloudifin_testFlavor;
create table cloudifin_testFlavor (
  ID text,
  Name text,
  RAM text,
  Disk text,
  Ephemeral text,
  VCPUs text,
  IsPublic text
);
drop table if exists cloudifin_testImage;
create table cloudifin_testImage (
  ID text,
  Name text,
  Status text
);
drop table if exists cloudifin_testSecurity;
create table cloudifin_testSecurity (
  ID text,
  Name text,
  Description text,
  Project text,
  Tags text
);
drop table if exists cloudifin_testNetwork;
create table cloudifin_testNetwork (
  ID text,
  Name text,
  Subnets text
);
drop table if exists cloudifinUser;
create table cloudifinUser (
  ID text,
  Name text,
  Project text,
  Domain text,
  Description text,
  Email text,
  Enabled text
);
drop table if exists cloudifinProject;
create table cloudifinProject (
  ID text,
  Name text,
  Domain text,
  Description text,
  Enabled text
);
drop table if exists cloudifinHosts;
create table cloudifinHosts (
  ID_cloud text,
  Service text,
  Host text,
  Zone text,
  Status text,
  State text,
  Updated text
);
drop table if exists cloudifinFlavor;
create table cloudifinFlavor (
  ID text,
  Name text,
  RAM text,
  Disk text,
  Ephemeral text,
  VCPUs text,
  IsPublic text
);
drop table if exists cloudifinImage;
create table cloudifinImage (
  ID text,
  Name text,
  Status text
);
drop table if exists cloudifinSecurity;
create table cloudifinSecurity (
  ID text,
  Name text,
  Description text,
  Project text,
  Tags text
);
drop table if exists cloudifinNetwork;
create table cloudifinNetwork (
  ID text,
  Name text,
  Subnets text
);
drop table if exists cloudifinServer;
create table cloudifinServer (
  ID text,
  Name text,
  Status text,
  Networks text,
  Image text,
  Flavor text
);
drop table if exists OCCHosts;
create table OCCHosts (
  ID_cloud text,
  Service text,
  Host text,
  Zone text,
  Status text,
  State text,
  Updated text
);
drop table if exists OCCFlavor;
create table OCCFlavor (
  ID text,
  Name text,
  RAM text,
  Disk text,
  Ephemeral text,
  VCPUs text,
  IsPublic text
);
drop table if exists OCCImage;
create table OCCImage (
  ID text,
  Name text,
  Status text
);
drop table if exists OCCSecurity;
create table OCCSecurity (
  ID text,
  Name text,
  Description text,
  Project text,
  Tags text
);
drop table if exists OCCNetwork;
create table OCCNetwork (
  ID text,
  Name text,
  Subnets text
);
drop table if exists OCCServer;
create table OCCServer (
  ID text,
  Name text,
  Status text,
  Networks text,
  Image text,
  Flavor text
);
"""

#Connect or Create DB File
conn = sqlite3.connect(DB_Name)
curs = conn.cursor()

#Create Tables
sqlite3.complete_statement(TableSchema)
curs.executescript(TableSchema)

#Close DB
curs.close()
conn.close()
