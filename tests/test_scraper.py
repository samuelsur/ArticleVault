import unittest
import sys
import os

# Add the parent directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import patch, MagicMock
from scraper import ArticleDownloader

class TestArticleDownloader(unittest.TestCase):
    def setUp(self):
        with patch.dict('os.environ', {'SCRAPER_API_KEY': 'test_key'}):
            self.downloader = ArticleDownloader()
    
    def test_check_structure_valid_input(self):
        """Test check_structure with a valid input structure."""
        # Create a valid test dictionary that matches the expected structure
        valid_input = {
            'title': 'Test Article',
            'date': '2025-06-18',
            'author': 'Test Author',
            'content_blocks': [
                {
                    'type': 'text',
                    'content': 'This is a test paragraph.'
                },
                {
                    'type': 'image',
                    'url': 'https://example.com/image.jpg',
                    'alt_text': 'Test image',
                    'caption': 'Test caption'
                }
            ]
        }
        
        # This should not raise an exception and should return True
        result = self.downloader.check_structure(valid_input)
        self.assertTrue(result)
    
    def test_check_structure_not_dict(self):
        """Test check_structure with a non-dictionary input."""
        with self.assertRaises(ValueError) as context:
            self.downloader.check_structure("not a dictionary")
        
        self.assertEqual(str(context.exception), "Result must be a dictionary")
    
    def test_check_structure_missing_keys(self):
        """Test check_structure with missing required keys."""
        # Missing 'author' key
        invalid_input = {
            'title': 'Test Article',
            'date': '2025-06-18',
            'content_blocks': []
        }
        
        with self.assertRaises(ValueError) as context:
            self.downloader.check_structure(invalid_input)
        
        self.assertIn("Result must contain keys", str(context.exception))
    
    def test_check_structure_content_blocks_not_list(self):
        """Test check_structure with content_blocks that is not a list."""
        invalid_input = {
            'title': 'Test Article',
            'date': '2025-06-18',
            'author': 'Test Author',
            'content_blocks': 'not a list'
        }
        
        with self.assertRaises(ValueError) as context:
            self.downloader.check_structure(invalid_input)
        
        self.assertEqual(str(context.exception), "content_blocks must be a list")
    
    def test_check_structure_block_not_dict(self):
        """Test check_structure with a content block that is not a dictionary."""
        invalid_input = {
            'title': 'Test Article',
            'date': '2025-06-18',
            'author': 'Test Author',
            'content_blocks': ["not a dictionary"]
        }
        
        with self.assertRaises(ValueError) as context:
            self.downloader.check_structure(invalid_input)
        
        self.assertEqual(str(context.exception), "Each content block must be a dictionary")
    
    def test_check_structure_invalid_block_type(self):
        """Test check_structure with an invalid block type."""
        # Block with invalid 'type' value
        invalid_input = {
            'title': 'Test Article',
            'date': '2025-06-18',
            'author': 'Test Author',
            'content_blocks': [
                {
                    'type': 'invalid_type',
                    'content': 'Test content'
                }
            ]
        }
        
        with self.assertRaises(ValueError) as context:
            self.downloader.check_structure(invalid_input)
        
        self.assertEqual(str(context.exception), "Each content block must have a valid 'type' key")
        
        # Block missing 'type' key
        invalid_input = {
            'title': 'Test Article',
            'date': '2025-06-18',
            'author': 'Test Author',
            'content_blocks': [
                {
                    'content': 'Test content'
                }
            ]
        }
        
        with self.assertRaises(ValueError) as context:
            self.downloader.check_structure(invalid_input)
        
        self.assertEqual(str(context.exception), "Each content block must have a valid 'type' key")
    
    def test_check_structure_text_block_without_content(self):
        """Test check_structure with a text block missing content."""
        invalid_input = {
            'title': 'Test Article',
            'date': '2025-06-18',
            'author': 'Test Author',
            'content_blocks': [
                {
                    'type': 'text'
                    # Missing 'content' key
                }
            ]
        }
        
        with self.assertRaises(ValueError) as context:
            self.downloader.check_structure(invalid_input)
        
        self.assertEqual(str(context.exception), "Text blocks must have a 'content' key")
    
    def test_check_structure_image_block_missing_fields(self):
        """Test check_structure with an image block missing required fields."""
        # Missing 'url' key
        invalid_input = {
            'title': 'Test Article',
            'date': '2025-06-18',
            'author': 'Test Author',
            'content_blocks': [
                {
                    'type': 'image',
                    'alt_text': 'Test alt text',
                    'caption': 'Test caption'
                    # Missing 'url' key
                }
            ]
        }
        
        with self.assertRaises(ValueError) as context:
            self.downloader.check_structure(invalid_input)
        
        self.assertEqual(str(context.exception), "Image blocks must have 'url' and 'alt_text' keys")
        
        # Missing 'alt_text' key
        invalid_input = {
            'title': 'Test Article',
            'date': '2025-06-18',
            'author': 'Test Author',
            'content_blocks': [
                {
                    'type': 'image',
                    'url': 'https://example.com/image.jpg',
                    'caption': 'Test caption'
                    # Missing 'alt_text' key
                }
            ]
        }
        
        with self.assertRaises(ValueError) as context:
            self.downloader.check_structure(invalid_input)
        
        self.assertEqual(str(context.exception), "Image blocks must have 'url' and 'alt_text' keys")
        
        # Missing 'caption' key
        invalid_input = {
            'title': 'Test Article',
            'date': '2025-06-18',
            'author': 'Test Author',
            'content_blocks': [
                {
                    'type': 'image',
                    'url': 'https://example.com/image.jpg',
                    'alt_text': 'Test alt text'
                    # Missing 'caption' key
                }
            ]
        }
        
        with self.assertRaises(ValueError) as context:
            self.downloader.check_structure(invalid_input)
        
        self.assertEqual(str(context.exception), "Image blocks must have 'url' and 'alt_text' keys")

if __name__ == '__main__':
    unittest.main()



