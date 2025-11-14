import asyncio
import os
import ssl
from typing import List

import certifi
from langchain_core.documents import Document
from langchain_tavily import TavilyCrawl

from assistants import init_env
from assistants.logger import get_logger
from assistants.study_assistant.study_material_ingestor import (
    LANGCHAIN_NOTES_PATH,
)

init_env()

logger = get_logger()


async def fetch() -> List[Document]:

    LANGCHAIN_NOTES_PATH.mkdir(parents=True, exist_ok=True)

    ssl_context = ssl.create_default_context(capath=certifi.where())
    os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
    os.environ["SSL_CERT_FILE"] = certifi.where()

    """
Why use certifi()?

- When your code makes an HTTPS request to a website, it needs to verify the site is legitimate
by checking its SSL certificate.

- Think of this like checking someone's ID - but who do you 
trust to issue valid IDs? That's where Certificate Authorities (CAs) come in.

- During an HTTPS handshake with a domain, the browser (Safari/Edge/Chrome) uses the OS'
"trust store" of CA public signatures for authenticating the website's
SSL certificate.

- Now, depending on the environment - where does the trust store exist?
    - Mac uses a keychain
    - Docker doesn't have any certificates!
    - For Linux machines, they are located at: /etc/ssl/certs/
    etc.

- certifi.where() always returns a valid path: /path/to/site-packages/certifi/cacert.pem
    - This `.pem` file contains ~150 root CA certificates from Mozilla's program.
"""
    try:
        results = await TavilyCrawl().ainvoke(
            input={
                "url": "https://python.langchain.com/",
                "max_depth": 5,
                "extract_depth": "advanced",
            },
        )
    except Exception as e:
        raise RuntimeError(f"Failed to performing web crawling: {e}")

    logger.info(
        f"[b d]Finished web crawling operation, retrieved {len(results['results'])} pages"
    )

    for doc_idx, result in enumerate(results["results"]):

        if not result.get("raw_content"):
            logger.error(f"[b d]Skipping doc_{doc_idx} - no content retrieved")
            continue

        file_name = f"doc_{doc_idx}.md"
        file_path = LANGCHAIN_NOTES_PATH / file_name

        with open(file_path, "w+", encoding="utf-8") as f:
            f.write(result["raw_content"])

        logger.debug(f"[b d]Wrote scraped page to: {file_path}")

    langchain_documents = [
        Document(
            page_content=result["raw_content"],
            metadata={
                "source": result["url"],
            },
        )
        for result in results["results"]
        if result.get("raw_content") is not None
    ]

    return langchain_documents


if __name__ == "__main__":
    asyncio.run(fetch())
