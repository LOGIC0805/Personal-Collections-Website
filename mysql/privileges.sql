use mysql;
select host, user from user;
update user set authentication_string = password('root') where user = 'root';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'root' WITH GRANT OPTION;
flush priveleges;
