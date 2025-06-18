import streamlit as st
import time
from scraper import ArticleDownloader

# main funciton to run the Streamlit app
# This function initializes the app, sets up the layout, and handles user input for article extraction
def main():
    # Initialize the ArticleDownloader instance
    article_downloader = ArticleDownloader()
    # Set up the Streamlit page configuration
    st.set_page_config(
        page_title="Article Extractor",
        page_icon="📰",
        layout="wide", # Use 'wide' layout for more space
        initial_sidebar_state="expanded" # Expanded sidebar for better navigation
    )
    # Set the title of the app
    st.title("Article Extractor")

    # App introduction
    st.markdown("""
    Extract complete articles including text, images, and formatting into a structured DOCX file.
    Simply enter the URL of the article below and click "Extract Article".
    """)

    user_input = st.text_input(
        "Enter the URL of the article you want to extract:",
        placeholder="https://www.example.com/article"
    )
    
    # Create a container for the progress bar and status updates
    progress_container = st.container()
    
    # Function to update progress
    def update_progress(message, percent):
        # Update the progress bar
        progress_bar.progress(int(percent))
        # Update the status message
        status_placeholder.markdown(f"**Status:** {message}")
        # Force a redraw
        time.sleep(0.1)
    
    if st.button("Extract Article", key="extract_button"):
        if user_input:
            with progress_container:
                # Create placeholders for progress elements
                progress_bar = st.progress(0)
                status_placeholder = st.empty()
                
                update_progress("Starting article extraction...", 5)
                
                try:
                    # Run the extraction with progress updates
                    _, result, path = article_downloader.run(
                        user_input, 
                        progress_callback=update_progress
                    )
                    
                    # Complete the progress bar
                    update_progress("Article extracted successfully!", 100)
                    
                    # Show article metadata
                    st.success("✅ Article extracted successfully!")
                    
                    with st.expander("Article Details", expanded=True):
                        st.markdown(f"**Title:** {result["title"]}")
                        st.markdown(f"**Author:** {result["author"] if result["author"] else 'Unknown'}")
                        st.markdown(f"**Date:** {result["date"] if result["date"] else 'Unknown'}")
                        
                        # Count content blocks
                        text_blocks = sum(1 for block in result["content_blocks"] if block["type"] == "text")
                        image_blocks = sum(1 for block in result["content_blocks"] if block["type"] == "image")
                        st.markdown(f"**Content:** {text_blocks} text blocks, {image_blocks} images")
                    
                    # Provide download button
                    st.markdown("### Download Document")
                    st.download_button(
                        label="Download DOCX",
                        data=open(path, "rb").read(),
                        file_name="extracted_article.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key="download_button"
                    )
                    
                except Exception as e:
                    st.error(f"Error during extraction: {str(e)}")
                    update_progress(f"Error: {str(e)}", 100)
        else:
            st.warning("Please enter a valid article URL")

if __name__ == "__main__":
    main()
