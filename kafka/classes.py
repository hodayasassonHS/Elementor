from sqlalchemy import Column, Integer, String, Float, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    address = Column(String)
    phone_number = Column(String)
    password = Column(String)


class Packages(Base):
    __tablename__ = 'packages'
    package_id = Column(Integer, primary_key=True, autoincrement=True)
    package_name = Column(String)
    cost_per_month = Column(Integer)
    storage_gb = Column(Float)
    AI_tokens_amount = Column(Integer)
    cpu_percent = Column(Float)


class Sites(Base):
    __tablename__ = 'sites'
    site_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    site_name = Column(String)
    site_description = Column(String)
    date_created = Column(TIMESTAMP)


class PackagesToUsers(Base):
    __tablename__ = 'packages_to_users'
    package_to_user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    package_id = Column(Integer, ForeignKey('packages.package_id'))


class SitesToPackage(Base):
    __tablename__ = 'sites_to_package'
    id = Column(Integer, primary_key=True, autoincrement=True)
    package_id = Column(Integer, ForeignKey('packages_to_users.package_to_user_id'))
    site_id = Column(Integer, ForeignKey('sites.site_id'))


class UsagePerSite(Base):
    __tablename__ = 'usage_per_site'
    id = Column(Integer, primary_key=True, autoincrement=True)
    site_id = Column(Integer, ForeignKey('sites.site_id'))
    time = Column(TIMESTAMP)
    storage_gb = Column(Float)
    cpu_percent = Column(Float)
    ai_tokens_amount=Column(Integer)
