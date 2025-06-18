# ArticleVault

An automated system for extracting structured content from web articles and converting to formatted DOCX documents with preserved image positioning.

## Why ArticleVault?

In my company there is a need to archive and store some web articles in a 
structured format. Docx document format was chosen as most of the people 
are familiar with it. 

The task of extracting is simple when performed manually, however, 
it is repetitive. Thus ArticleVault was created.

## Overview

Article Scraper implements a robust extraction pipeline that leverages state-of-the-art language models to parse web articles into structured data objects. The system processes both textual content and visual elements while maintaining their semantic relationships and relative positioning, then renders the extracted content into standardized document formats.

The application features a user-friendly **web interface built with Streamlit**, allowing users to easily input article URLs, view extraction progress in real-time, and download the resulting DOCX documents. Streamlit provides an interactive dashboard experience where users can monitor the extraction process and access their downloaded articles.

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

6. **Interactive Web Interface**
   - Built with **Streamlit** for intuitive user experience
   - Real-time progress updates and status notifications
   - Preview capabilities for extracted content
   - Integrated download functionality for generated documents

7. **Error Handling & Validation**
   - Content validation to ensure extraction completeness
   - Fallback mechanisms for handling extraction challenges
   - Comprehensive error reporting with user-friendly messages

## Configuration & Deployment

The application runs as a Streamlit web app, providing an interactive interface accessible through your browser. There are two ways to run the application: directly from the command line interface or inside a Docker container.

You will need to configure the environment with the required API credentials, which are stored in a `.env` file.

### Run through Command Line Interface
1. Clone the repository
2. Install the required dependencies, we suggest using a virtual environment to avoid conflicts (either `venv` or `conda`):
```bash 
pip install -r requirements.txt
```
4. Start the Streamlit web application:

```bash
streamlit run app.py
```

This will launch the Streamlit server and automatically open a browser window with the application running at http://localhost:8501.

### Run using Docker Container
1. Clone the repository
2. Create a `.env` file with your OpenAI API key (see next section)
3. Build and run the Docker image using docker-compose:
```bash 
docker compose up -d
```
This will:
- Build a Docker image based on the Dockerfile
- Configure the container with proper environment variables from your `.env` file
- Start the application in detached mode
- Set up health checks to monitor application status
- Make the application accessible at `http://localhost:8501`

4. To stop the application, run:
```bash
docker compose down
```

5. To view logs:
```bash
docker compose logs -f
```



### Configure environment with required API credentials
Create a `.env` file in the root directory of the project with the following content:

```
OPENAI_APIKEY=your_openai_api_key
```

The example of the `.env` file is provided in the repository as `.env.example`. Make sure to rename it to `.env` and fill in your OpenAI API key.

When running with Docker, the `.env` file is automatically loaded via the `env_file` configuration in docker-compose.yml.

## System Architecture

```
article_scraper/
│
├── app.py                  # Streamlit web interface and application entrypoint
├── scraper.py              # Core extraction and processing engine
├── utils.py                # Document generation and asset management utilities
├── requirements.txt        # Dependencies manifest
├── .env                    # API configuration (git-ignored)
├── .env.example            # Example environment configuration
├── Dockerfile              # Container definition for Docker deployment
├── docker-compose.yml      # Docker Compose configuration
├── .dockerignore           # Files to exclude from Docker build
└── README.md               # Documentation
```

## Containerization Approach

The application is containerized using Docker with the following architecture:

1. **Base Image**: Python 3.12 slim for a lightweight container footprint
2. **Security**: Runs as a non-root user (appuser) with appropriate permissions
3. **Dependency Management**: Two-stage copy for better caching of dependencies
4. **Configuration**: Environment variables for application settings
5. **Health Monitoring**: Container health checks to ensure application availability
6. **Orchestration**: Docker Compose for easy deployment and service management

This containerization approach ensures:
- Consistent environments across development and production
- Isolation from the host system
- Easy deployment and scaling
- Security through principle of least privilege
- Simplified dependency management

## TODO
- [ ] Implement error handling when the user provides an invalid URL
- [ ] Paywall detection and handling
- [ ] Implement option for user to select size of the images in the document as well as other formatting options
- [ ] Implement option for user to select the format of the document (PDF, DOCX, etc.)
- [ ] Implement option for user to add extra prompts to the AI model to improve the extraction quality
- [ ] Tests


## License

Licensed under the MIT License.

