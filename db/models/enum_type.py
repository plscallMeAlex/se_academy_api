# storing all enum types
from enum import Enum

class RoleEnum(str, Enum):
    freshman = "freshman"
    sophomore = "sophomore"
    junior = "junior"
    senior = "senior"
    graduate = "graduate"
    admin = "admin"

class StatusEnum(str, Enum):
    active = "active"
    inactive = "inactive"
    suspended = "suspended"