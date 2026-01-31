import asyncio
import httpx
from concurrent.futures import ProcessPoolExecutor
from .models import APIConfig, Config, Ebook
from typing import Callable

class CacheManager:
    '''
    缓存管理类，负责缓存的读写
    '''

class APISessionManager:
    '''
    管理最小api请求发送单元的管理，处理多api来源负载均衡、并发限制
    '''
    def __init__(self):
        pass

    def send_req(self):
        '''
        单个“章节”（API请求）翻译，获取最终翻译结果
        '''
        pass

class TranslateBook:
    '''
    简单的组合类，用于集中处理同一本书的缓存处理和多章节翻译（包括缓存比较，实现“断点续翻”）
    '''
    def __init__(self, book: Ebook, cache: CacheManager):
        pass

    async def translate_book(self):
        pass

class TranslateWorkflow:
    '''
    组合类，用于连接epub解析逻辑和api请求，实现批量化
    '''
    def __init__(self, config: Config, parser_factory: Callable, api_handler: APISessionManager):
        self.config = config
        self.parser_factory = parser_factory
        self.api_handler = api_handler

        self.queue = asyncio.Queue(self.config.max_queue_size)
        self.cache_manager = CacheManager()

    async def _parse_wrapper(self, ebook_path: str, pool: ProcessPoolExecutor):
        '''
        Parser.parse()的异步包装函数，负责run_in_executor和添加到队列
        '''
        loop = asyncio.get_running_loop()
        parser = self.parser_factory(ebook_path)
        
        parse_result = await loop.run_in_executor(pool, parser.parse)
        await self.queue.put(parse_result)

    async def _translate_task(self):
        while True:
            current_bookdata = await self.queue.get()
            single_translate = TranslateBook(current_bookdata, self.cache_manager)
            await single_translate.translate_book()
            self.queue.task_done()

    async def translate(self):
        '''
        批量翻译主方法，负责解析和翻译的调度，不返回结果（被存入缓存）
        '''

        # 先启动消费者（翻译任务）等待从队列获得数据
        worker_tasks = [
            asyncio.create_task(self._translate_task())
            for _ in range(self.config.max_concurrent_books)
        ]

        # 并行解析电子书并且加入队列
        with ProcessPoolExecutor(self.config.parser_processes) as pool:
            parser_tasks = [
                self._parse_wrapper(book.path, pool)
                for book in self.config.books
            ]

        await self.queue.join() # 等待queue

        for task in worker_tasks: # 取消等待数据的翻译任务
            task.cancel()
