from enum import Enum


class DatabaseTypeEnum(Enum):
    SQLITE = "sqlite"
    POSTGRES = "postgres"
    MARIADB = "mariadb"
    MYSQL = "mysql"
    UNKNOWN = ""
