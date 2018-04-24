#!/bin/sh
DATABASE="app_aio"
USERNAME="postgres"
HOsTNAME="127.0.0.1"
export PGPASSWORD=""

psql -h $HOSTNAME -U $USERNAME -v ON_ERROR_STOP=1 <<-EOSQL
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE DATABASE $DATABASE;
\c $DATABASE
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE TABLE users(
   login varchar(30) PRIMARY KEY,
   password varchar(30)
);
CREATE TABLE hosts(
  host_id UUID PRIMARY KEY DEFAULT uuid_generate_v1(),
  host varchar(50),
  port INT,
  status varchar(20)

);
CREATE TABLE user_host(
  CONSTRAINT login_host PRIMARY KEY (login, host_id),
  login varchar(30) REFERENCES users (login) ON UPDATE CASCADE ON DELETE CASCADE,
  host_id UUID  REFERENCES hosts (host_id) ON UPDATE CASCADE ON DELETE CASCADE

);
EOSQL
