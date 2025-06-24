import streamlit as st
import time
from scraper import ArticleDownloader
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader


def authenticate_user():
    with open(".streamlit/config.yaml") as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )
    
    
    authenticator.login(location = 'sidebar')
    
    auth_state = st.session_state.get("authentication_status")

    if auth_state:
        # User is connected
        authenticator.logout('Logout', 'sidebar')
    elif auth_state == False:
        st.error('Username or password is incorrect')
        # Stop the rendering if the user isn't connected
        st.stop()
    elif auth_state is None:
        st.warning('Please enter your username and password')
        # Stop the rendering if the user isn't connected
        st.stop()

    return authenticator



def set_layout():
    st.set_page_config(
        page_title="Article Extractor",
        page_icon="📰",
        layout="centered",  # Centered layout for better aesthetics
    )
    st.sidebar.header("Article Extractor")
    # Set the title of the app
    st.title("Article Extractor")



# main function to run the Streamlit app
# This function initializes the app, sets up the layout, and handles user input for article extraction
def main():
    # Set up the Streamlit page configuration
    set_layout()
    # Authenticate the user
    authenticator = authenticate_user()
    # Initialize the ArticleDownloader instance
    article_downloader = ArticleDownloader()


    # App introduction
    st.markdown("""
    Extract complete articles including text, images, and formatting into a structured DOCX file.
    Simply enter the URL of the article below and click "Extract Article".
    """)

    # Initialize session state variables
    if "extracting" not in st.session_state: # Track if extraction is in progress
        st.session_state.extracting = False
    if "result" not in st.session_state: # Store the result of the extraction
        st.session_state.result = None
    if "path" not in st.session_state: # Store the path to the generated DOCX file
        st.session_state.path = None

    # Define callback functions for buttons
    def start_extraction():
        # Clear any previous results before starting a new extraction
        if "result" in st.session_state:
            st.session_state.result = None
        if "path" in st.session_state:
            st.session_state.path = None
        # Set extraction flag
        st.session_state.extracting = True
    

    def clear_results(): # Clear the results and reset the state
        # Clear all session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.extracting = False

    user_input = st.text_input(
        "Enter the URL of the article you want to extract:",
        placeholder="https://www.example.com/article",
        key="url_input"
    )
    
    # Only disable the button during active extraction
    st.button(
        "Extract Article", 
        key="extract_button", 
        on_click=start_extraction, 
        disabled=st.session_state.extracting
    )
    # Create a container for the progress bar and status updates
    progress_container = st.container()
    
    # Function to update progress
    def update_progress(message, percent, progress_bar_obj, status_ph):
        # Update the progress bar
        progress_bar_obj.progress(int(percent))
        # Update the status message
        status_ph.markdown(f"**Status:** {message}")
        # Force a redraw
        time.sleep(0.1)
        # Always continue processing
        return True
    

    # Only show results if we have them
    if st.session_state.get("result") and st.session_state.get("path"):
        result = st.session_state.result
        path = st.session_state.path
        
        # Show article metadata
        st.success("✅ Article extracted successfully!")
        
        with st.expander("Article Details", expanded=True):
            st.markdown(f"**Title:** {result['title']}")
            st.markdown(f"**Author:** {result['author'] if result['author'] else 'Unknown'}")
            st.markdown(f"**Date:** {result['date'] if result['date'] else 'Unknown'}")
            
            # Count content blocks
            text_blocks = sum(1 for block in result["content_blocks"] if block["type"] == "text")
            image_blocks = sum(1 for block in result["content_blocks"] if block["type"] == "image")
            st.markdown(f"**Content:** {text_blocks} text blocks, {image_blocks} images")
        
        # Provide download button and clear button side by side
        st.markdown("### Actions")
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="Download DOCX",
                data=open(path, "rb").read(),
                file_name="extracted_article.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                key="download_button",
                use_container_width=True
            )
        with col2:
            st.button("Clear", key="clear_button", on_click=clear_results, use_container_width=True)
    
    # Extraction logic - runs when extraction state is true and we have input
    if st.session_state.extracting and user_input:
        with progress_container:
            # Create placeholders for progress elements
            progress_bar = st.progress(0)
            status_placeholder = st.empty()
            
            update_progress("Starting article extraction...", 5, progress_bar, status_placeholder)
            
            try:
                # Run the extraction with progress updates using a lambda for the callback
                _, result, path = article_downloader.run(
                    user_input, 
                    progress_callback=lambda message, percent: update_progress(message, percent, progress_bar, status_placeholder)
                )
                
                # Complete the progress bar
                update_progress("Article extracted successfully!", 100, progress_bar, status_placeholder)
                # Store results in session state
                st.session_state.result = result
                st.session_state.path = path
                # Reset extraction state
                st.session_state.extracting = False
                # Force a rerun to show results
                st.rerun()
                
            except Exception as e:
                st.error(f"Error during extraction: {str(e)}")
                update_progress(f"Error: {str(e)}", 100, progress_bar, status_placeholder)
                # Button to clear the input/output (centered)
                col1, col2 = st.columns([1, 2])
                with col2:
                    st.button("Clear and Try Again", key="error_clear_button", on_click=clear_results, use_container_width=True)
                st.session_state.extracting = False
    
    elif st.session_state.extracting and not user_input:
        st.warning("Please enter a valid article URL")
        st.session_state.extracting = False

if __name__ == "__main__":
    main()
