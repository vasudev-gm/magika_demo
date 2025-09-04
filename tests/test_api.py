"""
API tests for Django Ninja endpoints.
"""
import io
import json
import tempfile
from django.test import TestCase, Client
from django.urls import reverse


class APITestCase(TestCase):
    """Test API endpoints functionality."""

    def setUp(self):
        """Set up test client."""
        self.client = Client()

    def test_hello_endpoint(self):
        """Test the /api/hello GET endpoint."""
        response = self.client.get('/api/hello')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), '"Hello world"')
        self.assertTrue(response['Content-Type'].startswith('application/json'))

    def test_hello_endpoint_methods(self):
        """Test that hello endpoint only accepts GET requests."""
        # POST should not be allowed
        response = self.client.post('/api/hello')
        self.assertEqual(response.status_code, 405)
        
        # PUT should not be allowed
        response = self.client.put('/api/hello')
        self.assertEqual(response.status_code, 405)
        
        # DELETE should not be allowed
        response = self.client.delete('/api/hello')
        self.assertEqual(response.status_code, 405)

    def test_upload_endpoint_no_file(self):
        """Test upload endpoint without providing a file."""
        response = self.client.post('/api/upload')
        # Should return an error when no file is provided
        self.assertIn(response.status_code, [400, 422])  # Bad request or unprocessable entity

    def test_upload_endpoint_with_text_file(self):
        """Test upload endpoint with a text file."""
        # Create a simple text file
        test_content = b"Hello, this is a test text file."
        test_file = io.BytesIO(test_content)
        test_file.name = 'test.txt'
        
        response = self.client.post('/api/upload', {'file': test_file})
        
        self.assertEqual(response.status_code, 200)
        
        # Parse JSON response
        response_data = json.loads(response.content.decode())
        
        # Check response structure
        self.assertIn('Detected File Type', response_data)
        self.assertIn('Size', response_data)
        
        # Check that size is correct
        self.assertEqual(response_data['Size'], len(test_content))
        
        # Check that file type is detected (should be text-related)
        detected_type = response_data['Detected File Type']
        self.assertIsInstance(detected_type, str)
        self.assertNotEqual(detected_type, 'Unknown')

    def test_upload_endpoint_with_empty_file(self):
        """Test upload endpoint with an empty file."""
        test_file = io.BytesIO(b"")
        test_file.name = 'empty.txt'
        
        response = self.client.post('/api/upload', {'file': test_file})
        
        # Should handle empty files gracefully
        self.assertEqual(response.status_code, 200)
        
        response_data = json.loads(response.content.decode())
        self.assertIn('Detected File Type', response_data)
        self.assertIn('Size', response_data)
        self.assertEqual(response_data['Size'], 0)

    def test_upload_endpoint_with_json_file(self):
        """Test upload endpoint with a JSON file."""
        test_content = b'{"test": "data", "number": 42}'
        test_file = io.BytesIO(test_content)
        test_file.name = 'test.json'
        
        response = self.client.post('/api/upload', {'file': test_file})
        
        self.assertEqual(response.status_code, 200)
        
        response_data = json.loads(response.content.decode())
        self.assertIn('Detected File Type', response_data)
        self.assertIn('Size', response_data)
        self.assertEqual(response_data['Size'], len(test_content))

    def test_upload_endpoint_with_html_file(self):
        """Test upload endpoint with an HTML file."""
        test_content = b'<!DOCTYPE html><html><head><title>Test</title></head><body><p>Hello World</p></body></html>'
        test_file = io.BytesIO(test_content)
        test_file.name = 'test.html'
        
        response = self.client.post('/api/upload', {'file': test_file})
        
        self.assertEqual(response.status_code, 200)
        
        response_data = json.loads(response.content.decode())
        self.assertIn('Detected File Type', response_data)
        self.assertIn('Size', response_data)
        self.assertEqual(response_data['Size'], len(test_content))

    def test_upload_endpoint_methods(self):
        """Test that upload endpoint only accepts POST requests."""
        # GET should not be allowed
        response = self.client.get('/api/upload')
        self.assertEqual(response.status_code, 405)
        
        # PUT should not be allowed
        response = self.client.put('/api/upload')
        self.assertEqual(response.status_code, 405)
        
        # DELETE should not be allowed
        response = self.client.delete('/api/upload')
        self.assertEqual(response.status_code, 405)

    def test_api_docs_accessibility(self):
        """Test that API documentation endpoint is accessible."""
        response = self.client.get('/api/docs')
        # Should be accessible (200) or redirect (302/301)
        self.assertIn(response.status_code, [200, 301, 302])

    def test_api_openapi_schema(self):
        """Test that OpenAPI schema endpoint is accessible."""
        response = self.client.get('/api/openapi.json')
        # Should be accessible
        self.assertIn(response.status_code, [200, 301, 302])

    def test_invalid_api_endpoint(self):
        """Test accessing a non-existent API endpoint."""
        response = self.client.get('/api/nonexistent')
        self.assertEqual(response.status_code, 404)

    def test_upload_response_format(self):
        """Test that upload endpoint returns properly formatted JSON."""
        test_content = b"Test content for format validation"
        test_file = io.BytesIO(test_content)
        test_file.name = 'test.txt'
        
        response = self.client.post('/api/upload', {'file': test_file})
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response['Content-Type'].startswith('application/json'))
        
        # Ensure response is valid JSON
        try:
            response_data = json.loads(response.content.decode())
        except json.JSONDecodeError:
            self.fail("Response is not valid JSON")
        
        # Check required fields
        self.assertIn('Detected File Type', response_data)
        self.assertIn('Size', response_data)
        
        # Check field types
        self.assertIsInstance(response_data['Detected File Type'], str)
        self.assertIsInstance(response_data['Size'], int)