# Article Scraper

An automated system for extracting structured content from web articles and converting to formatted DOCX documents with preserved image positioning.

## Overview

Article Scraper implements a robust extraction pipeline that leverages state-of-the-art language models to parse web articles into structured data objects. The system processes both textual content and visual elements while maintaining their semantic relationships and relative positioning, then renders the extracted content into standardized document formats.

## Technical Architecture & Implementation Pipeline

The system implements a multi-stage content processing pipeline with the following components:

1. **Content Acquisition & HTTP Processing**
   - Uses [**ScrapegraphAI**](https://github.com/ScrapeGraphAI/Scrapegraph-ai) for intelligent content retrieval
   - Handles response parsing and preliminary document structure analysis

2. **AI-Powered Content Structure Analysis**
   - Leverages **OpenAI GPT-4o** for semantic document parsing
   - Identifies article components, text sections, and embedded media

3. **Structured Content Block Generation**
   - Transforms unstructured content into typed data blocks:
     - Text blocks with formatting metadata (paragraphs, formatting)
     - Image blocks with metadata (URL, alt text, captions)
   - Maintains semantic relationships between content elements

4. **Image Asset Processing Pipeline**
   - Implements parallel downloading of referenced images
   - Processes and optimizes images for document inclusion
   - Creates local cache for efficient document generation

5. **Document Rendering & Layout Engine**
   - Uses **python-docx** for programmatic DOCX generation
   - Implements precise positioning of text and images
   - Applies formatting and styling rules for professional output

6. **Error Handling & Validation**
   - Content validation to ensure extraction completeness
   - Fallback mechanisms for handling extraction challenges
   - Comprehensive error reporting

## Configuration & Deployment


There are two ways how to run the application, the first one is directly from the command line interface, the second one is to run it inside a Docker container.

You will need to configure the environment with the required API credentials, which are stored in a `.env` file. 

### Run through Command Line Interface
1. Clone the repository
2. Install the required dependencies, we suggest using a virtual environment to avoid conflicts (either `venv` or `conda`):
```bash 
pip install -r requirements.txt
```
4. Run the application using the command line interface or as a Python module.

```bash
streamlit run app.py
```

### Run through Docker Container
TODO

### Configure environment with required API credentials
Create a `.env` file in the root directory of the project with the following content:

```
OPENAI_APIKEY=your_openai_api_key
```

## System Architecture

```
article_scraper/
│
├── app.py                  # Command-line interface and application entrypoint
├── scraper.py              # Core extraction and processing engine
├── utils.py                # Document generation and asset management utilities
├── requirements.txt        # Dependencies manifest
├── .env                    # API configuration (git-ignored)
└── README.md               # Documentation
```

## Document Rendering Configuration

The document rendering subsystem accepts the following configuration parameters:

```python
MSWord.create_page_bordered_docx(
    filename="output_document_path.docx",
    title=structured_data.title,
    content_blocks=structured_data.content_blocks,
    border_color=(150, 42, 46),  # RGB color specification
    border_width=200,            # Border width specification in points
    header="Optional document header",
    footer="Optional document footer"
)
```

## License

Licensed under the MIT License.

