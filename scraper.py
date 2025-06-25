import os
from dotenv import load_dotenv
from scrapegraphai.graphs import SmartScraperGraph
from scrapegraphai.utils import prettify_exec_info
from pydantic import BaseModel, Field
from typing import List, Optional
from utils import MSWord, Article, ContentBlock
from scrapegraphai.utils import prettify_exec_info


class ArticleDownloader:
    _instance = None

    # Singleton pattern to ensure only one instance of ArticleDownloader exists
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ArticleDownloader, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        # Ensure the class is only initialized once
        if self.__initialized:
            return
        
        load_dotenv()
        self.api_key = os.getenv("OPENAI_APIKEY")
        self.graph_config = {
            "llm": {
                "api_key": self.api_key,
                "model": "openai/gpt-4o",
                "temperature": 0.0,  # Set to 0 for deterministic output
            },
        }

        self.default_prompt = """
            CRITICAL: Extract the COMPLETE article with ALL content. Do not summarize or omit any sections.

            Extract the following elements:
            1. title - The complete headline of the article
            2. date - Publication date in original format
            3. author - Writer's full name (use 'NA' if not available)
            4. Content - EVERY paragraph from beginning to end with the original formatting (subtitles, bold, italics, etc.)
            5. Images - ALL images with their URLs, alt text, and captions

            Split content into paragraphs, same as they appear in the text. Maintain original formatting including quotes, lists, and emphasis.
            Include every image exactly where it appears in the original article.
            Links in text will remain only as text, do not convert them to hyperlinks.

            IMPORTANT: Verify you've captured the ENTIRE article from start to finish before submitting.
            """

        self.__initialized = True

    def _get_callback(self, callback=None):
        """
        Returns the provided callback or a no-op function if None is provided.
        This simplifies progress reporting by eliminating repeated null checks.
        
        Args:
            callback (callable, optional): The callback function to use
        Returns:
            callable: Either the provided callback or a no-op function
        """
        if callback is None:
            return lambda message, percent: None  # No-op function
        return callback

    def scrape(self, url: str) -> dict:
        """
        Scrape the article from the given URL using SmartScraperGraph.
        Args:
            url (str): The URL of the article to scrape.
        Returns:
            dict: The extracted article data in a structured format defined 
            by the Article model.
        """
        smart_scraper_graph = SmartScraperGraph(
            prompt = self.default_prompt,
            # also accepts a string with the already downloaded HTML code
            source=url,
            config=self.graph_config,
            schema=Article,
            )

        result = smart_scraper_graph.run()
        
        graph_exec_info = smart_scraper_graph.get_execution_info()
        total_price_usd = next((node['total_cost_USD'] for node in graph_exec_info if node['node_name'] == 'TOTAL RESULT'), None)
        # print(f'graph_exec_info: {graph_exec_info}')
        # print(prettify_exec_info(graph_exec_info))
        print(f'Total price of the run {total_price_usd}')
        return result
    

    def create_docx(self, result: Article, url, uuid, progress_callback=None):
        """
        Create a DOCX file with the extracted article content.
        
        Args:
            result (Article): The extracted article data.
            url (str): The URL of the article, used for context.
            uuid (str): Unique identifier for the extraction run.
            progress_callback (callable, optional): Callback function to report progress.
        Returns:
            str: The filename of the created DOCX file where the article is saved.
        """
        progress_callback = self._get_callback(progress_callback)
        
        docx_filename = "article_with_border.docx"
        MSWord.create_page_bordered_docx(
            uuid=uuid,
            filename=docx_filename,
            content=result,
            url = url,
            border_color=(150, 42, 46),  # Brown color
            border_width=200,  # Border width in points
            progress_callback=progress_callback
            # header=f"Author: {result.author}" if result.author else None,
            # footer=f"Date: {result.date}" if result.date else None
        )
        return docx_filename

    def check_structure(self, result: dict):
        """
        The output of the model is JSON, so we can check if the structure is correct.

        The structure is a dictionary which looks like the following:
         {
            title: string
            date: string
            author: string
            content_blocks: [
                {
                type: "text" | "image",
                content?: string,     // only for text
                url?: string,         // only for image
                alt_text?: string,    // only for image
                caption?: string      // only for image
                },
                ...
            ]
        }
        Args:
            result (dict): The extracted article data to validate.
        Returns:
            bool: True if the structure is valid, raises ValueError otherwise.
        Raises:
            ValueError: If the structure does not match the expected format.
        """
        required_keys = {'title', 'date', 'author', 'content_blocks'}
        if not isinstance(result, dict):
            raise ValueError("Result must be a dictionary")
        if not required_keys.issubset(result.keys()):
            raise ValueError(f"Result must contain keys: {required_keys}")
        if not isinstance(result['content_blocks'], list):
            raise ValueError("content_blocks must be a list")
        for block in result['content_blocks']:
            if not isinstance(block, dict):
                raise ValueError("Each content block must be a dictionary")
            if 'type' not in block or block['type'] not in {'text', 'image'}:
                raise ValueError("Each content block must have a valid 'type' key")
            if block['type'] == 'text' and 'content' not in block:
                raise ValueError("Text blocks must have a 'content' key")
            if block['type'] == 'image':
                if 'url' not in block or 'alt_text' not in block or 'caption' not in block:
                    raise ValueError("Image blocks must have 'url' and 'alt_text' keys")
                

        return True
                


        

    def run(self, unique_id, url: str, progress_callback=None) -> tuple[str, str]:
        """
        Run the scraper and create a DOCX file with the extracted article.
        
        Args:
            url (str): The URL of the article to scrape.
            progress_callback (callable, optional): Callback function to report progress.
                The function should accept a message string and a percentage float.
        Returns:
            str: The filename of the created DOCX file.
            str: The extracted article data.
            str: The absolute path to the created DOCX file.
        """
        # Each extraction run has a unique ID
        progress_callback = self._get_callback(progress_callback)
        progress_callback("Initializing article extraction...", 10)
        
        # Extract article content
        result = self.scrape(url)
        progress_callback("Article content extracted successfully", 40)
        
        try:
            self.check_structure(result)
            progress_callback("Article structure validated", 50)
        except ValueError as e:
            print(f"Error in result structure: {e}")
            progress_callback(f"Error: {e}", 100)
            raise ValueError(f"Invalid result structure: {e}")
        
        # Generate DOCX file
        progress_callback("Creating DOCX document...", 60)
        
        filename = self.create_docx(result, url, unique_id, progress_callback)
        progress_callback("DOCX document created successfully", 90)
        
        path = f"temp/{unique_id}/{filename}"
        progress_callback("Process complete!", 100)
        
        return filename, result, path


