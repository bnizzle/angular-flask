__author__ = 'Bnizzle'
#MYSQL Settings
mysql_db_username =     ""
mysql_db_password =     ""
mysql_db_name =         ""
mysql_db_hostname =     ""
SQLALCHEMY_TRACK_MODIFICATIONS = True

# SQLAlchemy Connect string
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{DB_USER}+:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER=mysql_db_username,
                                                                                            DB_PASS=mysql_db_password,
                                                                                            DB_ADDR=mysql_db_hostname,
                                                                                            DB_NAME=mysql_db_name)