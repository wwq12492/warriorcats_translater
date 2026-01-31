from abc import ABC, abstractmethod
from .models import Ebook
from os import path

# EPUBParser用到的模块
import re
from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup

class Parser(ABC):
    '''
    电子书解析器抽象基类，必须实现parse()方法
    '''
    @abstractmethod
    def parse(self) -> Ebook:
        pass

class EPUBParser(Parser):
    '''
    epub解析类（继承Parser）,为每本电子书实例化，只负责单本电子书的解析
    '''
    def __init__(self, ebook_path):
        self.ebook_path = ebook_path

    def _text_from_chapter_meta(self, content: bytes) -> str:
        '''
        将章节html content解析为文本，只负责单个章节
        '''
        soup = BeautifulSoup(content,"lxml")
        parsed_text = soup.get_text()
        return parsed_text

    def parse(self) -> Ebook:
        '''
        主解析方法，获取一本epub的信息
        '''
        book = epub.read_epub(self.ebook_path)
        chapter_contents = {}

        for document in book.get_items_of_type(ITEM_DOCUMENT):
            document_name = document.get_name()
            if re.search(r"chapter_\d+",document_name):
                parsed_content = self._text_from_chapter_meta(document.get_content())
                chapter_contents[document_name] = parsed_content
        
        bookdata = Ebook(path.splitext(self.ebook_path)[0], chapter_contents)
        return bookdata
    
def create_parser(ebook_path: str) -> Parser:
    '''
    工厂函数，用于自动为不同格式电子书实例化Parser
    '''
    if path.splitext(ebook_path)[1] == "epub":
        return EPUBParser(ebook_path)
    else:
        raise ValueError("错误的电子书格式")