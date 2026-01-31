from warriorcats_translater.translate import TranslateWorkflow,APISessionManager
from warriorcats_translater.models import Config,EbookConfig,APIConfig,Ebook
from warriorcats_translater.parse import create_parser
import asyncio

async def main():
    config = Config([], [EbookConfig("./into_the_wild.epub")], 8, 4, 10)
    api = APISessionManager()
    workflow = TranslateWorkflow(config,create_parser,api)
    await workflow.translate()

asyncio.run(main())
