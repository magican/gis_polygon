#!/bin/sh
#################
# Installation script for setting up the PostGIS Database
#################

sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | sudo apt-key add -
sudo apt-get update
sudo apt-get install -yq postgresql-9.5 postgresql-contrib-9.5 postgis pgadmin3

#sudo chown -R postgres:postgres /var/lib/postgresql/
#sudo chmod -R u=rwX,g=xr,o=x /var/lib/postgresql/
#sudo /etc/init.d/postgresql restart

sudo service postgresql start

psqluser="gis_polygon_user" # Database username
psqlpass="12345678"   # Database password
psqldb="gis_polygon_db"   # Database name

echo "CREATE USER $psqluser WITH PASSWORD '$psqlpass';" | sudo -u postgres psql

echo "CREATE DATABASE $psqldb WITH OWNER $psqluser;" | sudo -u postgres psql

echo "grant all privileges on database $psqldb to $psqluser;" | sudo -u postgres psql

sudo -u postgres psql
\connect $psqldb;
CREATE EXTENSION postgis;
SELECT PostGIS_version();
\q

#sudo vim /etc/postgresql/9.6/main/postgresql.conf
sudo service postgresql restart

