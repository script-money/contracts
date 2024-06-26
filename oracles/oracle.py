import asyncio

import settings

from src.repositories.ipfs_repository import IpfsRepository
from src.repositories.web3.chat_repository import Web3ChatRepository
from src.repositories.web3.function_repository import Web3FunctionRepository
from src.repositories.web3.knowledge_base_repository import Web3KnowledgeBaseRepository
from src.repositories.knowledge_base_repository import KnowledgeBaseRepository
from src.service import chat_service
from src.service import functions_service
from src.service import knowledge_base_indexing_service
from src.service import knowledge_base_query_service

web3_chat_repository = Web3ChatRepository()
web3_function_repository = Web3FunctionRepository()
web3_kb_repository = Web3KnowledgeBaseRepository()
ipfs_repository = IpfsRepository()
kb_repository = KnowledgeBaseRepository(max_size=settings.KNOWLEDGE_BASE_CACHE_MAX_SIZE)


async def main():
    tasks = [
        chat_service.execute(web3_chat_repository),
        functions_service.execute(web3_function_repository),
        knowledge_base_indexing_service.execute(web3_kb_repository, ipfs_repository, kb_repository),
        knowledge_base_query_service.execute(web3_kb_repository, ipfs_repository, kb_repository),
    ]

    print("Oracle started!")
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
