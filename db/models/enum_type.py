# storing all enum types
from enum import Enum


class RoleEnum(str, Enum):
    freshman = "freshman"
    sophomore = "sophomore"
    junior = "junior"
    senior = "senior"
    graduated = "graduated"
    admin = "admin"


class StatusEnum(str, Enum):
    active = "active"
    inactive = "inactive"
    suspended = "suspended"
