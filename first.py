import scrapy
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from urllib.parse import urljoin
import json
import pymysql
from datetime import datetime

class MovieSpider(RedisSpider):
    name = 'movie'
    redis_key = 'movie:start_urls'
    page_count = 0
    movie_count = 0
    
    def __init__(self, *args, **kwargs):
        super(MovieSpider, self).__init__(*args, **kwargs)
        # 连接MySQL
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            charset='utf8mb4'
        )
        self.cursor = self.conn.cursor()
        
        # 创建数据库和表
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS movies_db")
        self.cursor.execute("USE movies_db")
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                score FLOAT,
                page_num INT,
                crawl_time DATETIME,
                UNIQUE KEY (title)
            )
        """)
        self.conn.commit()
    
    def parse(self, response):
        # 更新页数计数
        self.page_count += 1
        print(f"\n正在处理第 {self.page_count} 页")
        
        # 提取电影信息
        for movie in response.css('div.el-card'):
            self.movie_count += 1
            title = movie.css('h2.m-b-sm::text').get().strip()
            score = movie.css('p.score::text').get().strip()
            
            try:
                # 保存到MySQL
                sql = """
                    INSERT INTO movies (title, score, page_num, crawl_time)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    score = VALUES(score),
                    page_num = VALUES(page_num),
                    crawl_time = VALUES(crawl_time)
                """
                self.cursor.execute(sql, (
                    title,
                    float(score),
                    self.page_count,
                    datetime.now()
                ))
                self.conn.commit()
                print(f"找到电影: {title} - 评分: {score}")
                
            except Exception as e:
                print(f"保存电影数据时出错: {e}")
                self.conn.rollback()
        
        # 处理下一页（最多爬取10页）
        if self.page_count < 10:
            next_page = response.css('a.next::attr(href)').get()
            if next_page:
                next_url = urljoin(response.url, next_page)
                yield Request(next_url, dont_filter=True)
        else:
            print("\n爬取完成！")
            print(f"总共爬取了 {self.page_count} 页")
            print(f"总共找到 {self.movie_count} 部电影")
            
            # 从MySQL中读取并显示所有电影
            print("\n电影列表:")
            self.cursor.execute("""
                SELECT title, score, page_num, crawl_time 
                FROM movies 
                ORDER BY score DESC
            """)
            for movie in self.cursor.fetchall():
                print(f"- 第{movie[2]}页: {movie[0]} (评分: {movie[1]}) [爬取时间: {movie[3]}]")
            
            # 关闭数据库连接
            self.cursor.close()
            self.conn.close()
            
            self.crawler.engine.close_spider(self, '爬取完成')

def main():
    from scrapy.crawler import CrawlerProcess
    from redis import Redis
    
    # 基本设置
    settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 1,
        'REDIS_HOST': 'localhost',
        'REDIS_PORT': 6379,
        'SCHEDULER': "scrapy_redis.scheduler.Scheduler",
        'DUPEFILTER_CLASS': "scrapy_redis.dupefilter.RFPDupeFilter"
    }
    
    # 只清理Redis的URL队列
    redis_cli = Redis(host='localhost', port=6379)
    redis_cli.delete('movie:start_urls')
    redis_cli.lpush('movie:start_urls', 'https://ssr1.scrape.center/')
    
    # 运行爬虫
    process = CrawlerProcess(settings)
    process.crawl(MovieSpider)
    process.start()

if __name__ == "__main__":
    main()