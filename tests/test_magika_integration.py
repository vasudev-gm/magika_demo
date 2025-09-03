"""
Tests for Magika integration and file type detection functionality.
"""
import io
import json
from django.test import TestCase, Client
from example.api import check_file_type_magika


class MagikaIntegrationTestCase(TestCase):
    """Test Magika file type detection integration."""

    def setUp(self):
        """Set up test client."""
        self.client = Client()

    def test_magika_function_with_text_content(self):
        """Test the check_file_type_magika function with text content."""
        test_content = b"This is a plain text file with some content."
        result = check_file_type_magika(test_content)
        
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertIn("File Type is", result)
        self.assertIn("with Mime Type", result)

    def test_magika_function_with_html_content(self):
        """Test the check_file_type_magika function with HTML content."""
        test_content = b'<!DOCTYPE html><html><head><title>Test</title></head><body><h1>Hello</h1></body></html>'
        result = check_file_type_magika(test_content)
        
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertIn("File Type is", result)
        self.assertIn("with Mime Type", result)

    def test_magika_function_with_json_content(self):
        """Test the check_file_type_magika function with JSON content."""
        test_content = b'{"name": "test", "value": 123, "array": [1, 2, 3]}'
        result = check_file_type_magika(test_content)
        
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertIn("File Type is", result)
        self.assertIn("with Mime Type", result)

    def test_magika_function_with_xml_content(self):
        """Test the check_file_type_magika function with XML content."""
        test_content = b'<?xml version="1.0" encoding="UTF-8"?><root><item>test</item></root>'
        result = check_file_type_magika(test_content)
        
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertIn("File Type is", result)
        self.assertIn("with Mime Type", result)

    def test_magika_function_with_csv_content(self):
        """Test the check_file_type_magika function with CSV content."""
        test_content = b'name,age,city\nJohn,30,New York\nJane,25,Los Angeles'
        result = check_file_type_magika(test_content)
        
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertIn("File Type is", result)
        self.assertIn("with Mime Type", result)

    def test_magika_function_with_python_content(self):
        """Test the check_file_type_magika function with Python code."""
        test_content = b'#!/usr/bin/env python\ndef hello():\n    print("Hello, World!")\n\nif __name__ == "__main__":\n    hello()'
        result = check_file_type_magika(test_content)
        
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
        self.assertIn("File Type is", result)
        self.assertIn("with Mime Type", result)

    def test_magika_function_with_empty_content(self):
        """Test the check_file_type_magika function with empty content."""
        test_content = b""
        result = check_file_type_magika(test_content)
        
        # Empty content might return None or a generic type
        if result is not None:
            self.assertIsInstance(result, str)

    def test_upload_detects_text_file_correctly(self):
        """Test that upload endpoint correctly detects text files."""
        test_content = b"This is a plain text document with multiple lines.\nSecond line here.\nThird line."
        test_file = io.BytesIO(test_content)
        test_file.name = 'document.txt'
        
        response = self.client.post('/api/upload', {'file': test_file})
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content.decode())
        
        detected_type = response_data['Detected File Type']
        # Should detect some form of text
        self.assertNotEqual(detected_type, 'Unknown')
        self.assertIn('File Type is', detected_type)

    def test_upload_detects_html_file_correctly(self):
        """Test that upload endpoint correctly detects HTML files."""
        test_content = b'''<!DOCTYPE html>
<html>
<head>
    <title>Test HTML Document</title>
    <meta charset="UTF-8">
</head>
<body>
    <h1>Main Heading</h1>
    <p>This is a paragraph with <strong>bold text</strong> and <em>italic text</em>.</p>
    <ul>
        <li>List item 1</li>
        <li>List item 2</li>
    </ul>
</body>
</html>'''
        test_file = io.BytesIO(test_content)
        test_file.name = 'document.html'
        
        response = self.client.post('/api/upload', {'file': test_file})
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content.decode())
        
        detected_type = response_data['Detected File Type']
        self.assertNotEqual(detected_type, 'Unknown')
        self.assertIn('File Type is', detected_type)

    def test_upload_detects_json_file_correctly(self):
        """Test that upload endpoint correctly detects JSON files."""
        test_content = b'''{
    "name": "John Doe",
    "age": 30,
    "email": "john.doe@example.com",
    "address": {
        "street": "123 Main St",
        "city": "Anytown",
        "zipcode": "12345"
    },
    "hobbies": ["reading", "swimming", "coding"]
}'''
        test_file = io.BytesIO(test_content)
        test_file.name = 'data.json'
        
        response = self.client.post('/api/upload', {'file': test_file})
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content.decode())
        
        detected_type = response_data['Detected File Type']
        self.assertNotEqual(detected_type, 'Unknown')
        self.assertIn('File Type is', detected_type)

    def test_chunk_size_environment_variable(self):
        """Test that chunk size is correctly read from environment."""
        import os
        from example.api import chunk_size
        
        expected_chunk_size = int(os.getenv("CHUNK_SIZE", 100))
        self.assertEqual(chunk_size, expected_chunk_size)

    def test_upload_with_large_file_chunking(self):
        """Test upload functionality with a larger file to test chunking."""
        # Create a larger test file
        test_content = b"A" * 1000  # 1000 bytes
        test_file = io.BytesIO(test_content)
        test_file.name = 'large_test.txt'
        
        response = self.client.post('/api/upload', {'file': test_file})
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content.decode())
        
        # Should still detect the file type correctly
        self.assertIn('Detected File Type', response_data)
        self.assertIn('Size', response_data)
        self.assertEqual(response_data['Size'], 1000)
        self.assertNotEqual(response_data['Detected File Type'], 'Unknown')

    def test_magika_import_and_initialization(self):
        """Test that Magika is properly imported and initialized."""
        from example.api import m
        from magika import Magika
        
        self.assertIsInstance(m, Magika)

    def test_different_file_extensions_detection(self):
        """Test detection with different file extensions but same content."""
        test_content = b'{"test": "data"}'
        
        # Test with .json extension
        test_file_json = io.BytesIO(test_content)
        test_file_json.name = 'test.json'
        response_json = self.client.post('/api/upload', {'file': test_file_json})
        
        # Test with .txt extension (same content)
        test_file_txt = io.BytesIO(test_content)
        test_file_txt.name = 'test.txt'
        response_txt = self.client.post('/api/upload', {'file': test_file_txt})
        
        self.assertEqual(response_json.status_code, 200)
        self.assertEqual(response_txt.status_code, 200)
        
        # Both should be detected (Magika doesn't rely on file extensions)
        data_json = json.loads(response_json.content.decode())
        data_txt = json.loads(response_txt.content.decode())
        
        self.assertNotEqual(data_json['Detected File Type'], 'Unknown')
        self.assertNotEqual(data_txt['Detected File Type'], 'Unknown')