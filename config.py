# -*- coding: utf-8 -*-
import os

# 创建必要的目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'downloaded_images')
CRAWLED_DATA_DIR = os.path.join(BASE_DIR, 'crawled_data')

# 确保目录存在
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(CRAWLED_DATA_DIR, exist_ok=True)

# Redis配置
REDIS_CONFIG = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    'decode_responses': True
}

# URL配置
SEED_URLS = [
    'https://sc.chinaz.com/tupian/meishitupian.html',
    'https://sc.chinaz.com/tupian/meishitupian_2.html',
    'https://sc.chinaz.com/tupian/meishitupian_3.html',
    'https://sc.chinaz.com/tupian/meishitupian_4.html',
    'https://sc.chinaz.com/tupian/meishitupian_5.html'
]

# 爬虫配置
CRAWLER_CONFIG = {
    'max_workers': 3,
    'timeout': 10,
    'max_retries': 3,
    'download_path': 'downloaded_images'
}

# 简单代理池配置
PROXY_POOL = [
    'http://182.34.102.166:9999',
    'http://183.236.232.160:8080',
    'http://120.220.220.95:8085',
]

# Redis键名配置
REDIS_KEYS = {
    'seed_urls': 'seed_urls',
    'pending_urls': 'pending_urls',
    'failed_urls': 'failed_urls',
    'success_urls': 'success_urls',
    'crawler_status': 'crawler_status',
    'parsed_data': 'parsed_data',
    'image_titles': 'image_titles'
} 