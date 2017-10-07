<?php
// Zabbix GUI configuration file.
global $DB;

$DB['TYPE']                             = 'MYSQL';
$DB['SERVER']                   = '{{zabbix_server_dbhost}}';
$DB['PORT']                             = '{{zabbix_server_dbport}}';
$DB['DATABASE']                 = '{{zabbix_server_dbname}}';
$DB['USER']                             = '{{zabbix_server_dbuser}}';
$DB['PASSWORD']                 = '{{zabbix_server_dbpassword}}';
// Schema name. Used for IBM DB2 and PostgreSQL.
$DB['SCHEMA']                   = '';

$ZBX_SERVER                             = '{{zabbix_server_ip}}';
$ZBX_SERVER_PORT                = '10051';
$ZBX_SERVER_NAME                = 'jz';

$IMAGE_FORMAT_DEFAULT   = IMAGE_FORMAT_PNG;
