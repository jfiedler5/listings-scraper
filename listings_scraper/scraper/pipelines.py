import psycopg2
from time import sleep
from scrapy.exceptions import NotConfigured


class PostgresPipeline:

    def __init__(self, database_settings):
        self.database_settings = database_settings
        self.conn = None
        self.cur = None

    @classmethod
    def from_crawler(cls, crawler):
        database_settings = crawler.settings.get('DATABASE')
        if not database_settings:
            raise NotConfigured
        return cls(database_settings)

    def open_spider(self, spider):
        self.connect_to_database()
        self.prepare_table()

    def prepare_table(self):
        drop_table_query = "DROP TABLE IF EXISTS scrapy_table;"
        create_table_query = """
            CREATE TABLE IF NOT EXISTS scrapy_table (
                id INT PRIMARY KEY,
                title VARCHAR(255),
                image_url TEXT
            );
        """
        self.cur.execute(drop_table_query)
        self.cur.execute(create_table_query)
        self.conn.commit()

    def connect_to_database(self):
        retries = 5
        delay = 5  # seconds

        for i in range(retries):
            try:
                self.conn = psycopg2.connect(
                    dbname=self.database_settings['database'],
                    user=self.database_settings['username'],
                    password=self.database_settings['password'],
                    host=self.database_settings['host'],
                    port=self.database_settings['port']
                )
                self.cur = self.conn.cursor()
                break
            except psycopg2.OperationalError as e:
                if i < retries - 1:
                    sleep(delay)
                    continue
                else:
                    raise e

    def close_spider(self, spider):
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()

    def process_item(self, item, spider):
        try:
            self.cur.execute("INSERT INTO scrapy_table (id, title, image_url) VALUES (%s, %s, %s)",
                             (item['id'], item['title'], item['image_url']))
            self.conn.commit()
        except Exception as e:
            spider.logger.error(f"Error processing item: {e}")
            self.conn.rollback()  # Rollback the transaction on error
        return item

