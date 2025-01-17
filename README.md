# qingxunying
简易分布式爬虫系统
class SeedURLManager:
    def __init__(self):
        # 使用集合来存储 URL，集合自动去重
        self.seed_urls = set()

    def add_url(self, url):
        """
        添加种子 URL，如果 URL 已存在则不会重复添加
        """
        if url not in self.seed_urls:
            self.seed_urls.add(url)
            print(f"URL added: {url}")
        else:
            print(f"URL already exists: {url}")

    def get_all_urls(self):
        """
        获取所有种子 URL
        """
        return self.seed_urls

    def remove_url(self, url):
        """
        移除指定的种子 URL
        """
        if url in self.seed_urls:
            self.seed_urls.remove(url)
            print(f"URL removed: {url}")
        else:
            print(f"URL not found: {url}")
