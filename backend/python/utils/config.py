"""Configuration Management"""
import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    DATABASE_URI = os.getenv('DATABASE_URI', 'mongodb://localhost:27017/bww')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
