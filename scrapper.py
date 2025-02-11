import asyncio
import aiohttp
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass
from pathlib import Path
import logging

@dataclass
class SitemapUrl:
    loc: str
    lastmod: Optional[datetime] = None
    priority: Optional[float] = None

@dataclass
class ExtractedContent:
    url: str
    text_content: str

class SitemapCrawler:
    def __init__(self, output_directory: str = "extracted_content"):
        self.output_directory = Path(output_directory)
        self.output_directory.mkdir(parents=True, exist_ok=True)

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('crawler.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    async def process_sitemap(self, sitemap_url: str, max_concurrent: int = 5):
        """Process the sitemap with concurrent URL processing."""
        urls = await self._parse_sitemap_xml(sitemap_url)
        self.logger.info(f"Found {len(urls)} URLs in sitemap")

        semaphore = asyncio.Semaphore(max_concurrent)
        tasks = [self._process_url(url, semaphore) for url in urls]
        await asyncio.gather(*tasks)

    async def _parse_sitemap_xml(self, sitemap_url: str) -> List[SitemapUrl]:
        """Parse the sitemap XML and return a list of URLs."""
        async with aiohttp.ClientSession() as session:
            async with session.get(sitemap_url) as response:
                sitemap_content = await response.text()

        root = ET.fromstring(sitemap_content)
        namespace = {'ns': root.tag.split('}')[0].strip('{')} if '}' in root.tag else {}

        urls = []
        for url in root.findall('.//ns:url' if namespace else './/url', namespace):
            loc = url.find('ns:loc' if namespace else 'loc', namespace).text
            urls.append(SitemapUrl(loc=loc))

        return urls

    async def _process_url(self, sitemap_url: SitemapUrl, semaphore: asyncio.Semaphore):
        """Process a single URL with rate limiting."""
        async with semaphore:
            try:
                content = await self._fetch_page_content(sitemap_url.loc)
                self.logger.info(f"Processing URL: {sitemap_url.loc}")
                await self._save_to_markdown(content)
                self.logger.info(f"Successfully processed {sitemap_url.loc}")
            except Exception as e:
                self.logger.error(f"Error processing {sitemap_url.loc}: {str(e)}")

    async def _fetch_page_content(self, url: str) -> ExtractedContent:
        """Fetch and parse webpage content."""
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')

                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()

                # Extract all visible text
                text_content = "\n".join([line.strip() for line in soup.get_text("\n").split("\n") if line.strip()])
                return ExtractedContent(url=url, text_content=text_content)

    async def _save_to_markdown(self, content: ExtractedContent):
        """Save extracted content as a well-formatted Markdown file."""
        markdown = (
            f"# Extracted Content\n\n"
            f"## URL\n\n"
            f"{content.url}\n\n"
            f"## Text Content\n\n"
            f"{content.text_content}\n"
        )

        # Safe filename creation
        filename = content.url.replace("https://", "").replace("http://", "").replace("/", "_")[:100] + '.md'
        filepath = self.output_directory / filename
        await asyncio.to_thread(filepath.write_text, markdown, encoding='utf-8')

async def main():
    # Initialize and run the crawler
    crawler = SitemapCrawler(output_directory="extracted_content")
    await crawler.process_sitemap(
        sitemap_url="https://blogforge.pythonanywhere.com/sitemap.xml",
        max_concurrent=5
    )

if __name__ == "__main__":
    asyncio.run(main())
