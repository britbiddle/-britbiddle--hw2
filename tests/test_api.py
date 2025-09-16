"""
Test suite for the Flask API endpoints of the Numeric Converter application.
Tests the /convert endpoint with various input combinations and error cases.
"""
import pytest
import json
import base64


class TestConvertEndpoint:
    """Test the /convert API endpoint."""
    
    def test_convert_text_to_decimal(self, client):
        """Test converting text to decimal."""
        response = client.post('/convert', 
                             data=json.dumps({
                                 'input': 'forty-two',
                                 'inputType': 'text',
                                 'outputType': 'decimal'
                             }),
                             content_type='application/json')
        
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['error'] is None
        assert data['result'] == '42'
    
    def test_convert_decimal_to_text(self, client):
        """Test converting decimal to text."""
        response = client.post('/convert',
                             data=json.dumps({
                                 'input': '42',
                                 'inputType': 'decimal',
                                 'outputType': 'text'
                             }),
                             content_type='application/json')
        
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['error'] is None
        assert data['result'] == 'forty-two'
    
    def test_convert_binary_to_hexadecimal(self, client):
        """Test converting binary to hexadecimal."""
        response = client.post('/convert',
                             data=json.dumps({
                                 'input': '101010',
                                 'inputType': 'binary',
                                 'outputType': 'hexadecimal'
                             }),
                             content_type='application/json')
        
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['error'] is None
        assert data['result'] == '2a'
    
    def test_convert_hexadecimal_to_octal(self, client):
        """Test converting hexadecimal to octal."""
        response = client.post('/convert',
                             data=json.dumps({
                                 'input': '2a',
                                 'inputType': 'hexadecimal',
                                 'outputType': 'octal'
                             }),
                             content_type='application/json')
        
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['error'] is None
        assert data['result'] == '52'
    
    def test_convert_decimal_to_base64(self, client):
        """Test converting decimal to base64 with little-endian."""
        response = client.post('/convert',
                             data=json.dumps({
                                 'input': '42',
                                 'inputType': 'decimal',
                                 'outputType': 'base64'
                             }),
                             content_type='application/json')
        
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['error'] is None
        # Verify it's little-endian by checking against expected value
        expected = base64.b64encode((42).to_bytes(1, 'little')).decode('utf-8')
        assert data['result'] == expected
    
    def test_convert_base64_to_decimal(self, client):
        """Test converting base64 to decimal with little-endian."""
        b64_input = base64.b64encode((42).to_bytes(1, 'little')).decode('utf-8')
        response = client.post('/convert',
                             data=json.dumps({
                                 'input': b64_input,
                                 'inputType': 'base64',
                                 'outputType': 'decimal'
                             }),
                             content_type='application/json')
        
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['error'] is None
        assert data['result'] == '42'
    
    def test_convert_zero_handling(self, client):
        """Test conversion of zero in various formats."""
        test_cases = [
            ('text', 'zero', 'decimal', '0'),
            ('decimal', '0', 'text', 'zero'),
            ('binary', '0', 'decimal', '0'),
            ('octal', '0', 'decimal', '0'),
            ('hexadecimal', '0', 'decimal', '0'),
        ]
        
        for input_type, input_val, output_type, expected in test_cases:
            response = client.post('/convert',
                                 data=json.dumps({
                                     'input': input_val,
                                     'inputType': input_type,
                                     'outputType': output_type
                                 }),
                                 content_type='application/json')
            
            data = json.loads(response.data)
            assert response.status_code == 200
            assert data['error'] is None
            assert data['result'] == expected
    
    def test_convert_large_numbers(self, client):
        """Test conversion of large numbers."""
        test_cases = [
            ('decimal', '1234', 'binary', '10011010010'),
            ('decimal', '1234', 'octal', '2322'),
            ('decimal', '1234', 'hexadecimal', '4d2'),
            ('decimal', '1234', 'text', 'one thousand, two hundred and thirty-four'),
        ]
        
        for input_type, input_val, output_type, expected in test_cases:
            response = client.post('/convert',
                                 data=json.dumps({
                                     'input': input_val,
                                     'inputType': input_type,
                                     'outputType': output_type
                                 }),
                                 content_type='application/json')
            
            data = json.loads(response.data)
            assert response.status_code == 200
            assert data['error'] is None
            assert data['result'] == expected
    
    def test_convert_negative_numbers(self, client):
        """Test conversion of negative numbers."""
        response = client.post('/convert',
                             data=json.dumps({
                                 'input': '-42',
                                 'inputType': 'decimal',
                                 'outputType': 'text'
                             }),
                             content_type='application/json')
        
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['error'] is None
        assert data['result'] == 'minus forty-two'
    
    def test_convert_negative_to_binary_bug(self, client):
        """Test that negative numbers convert to binary correctly (should detect bug)."""
        response = client.post('/convert',
                             data=json.dumps({
                                 'input': '-42',
                                 'inputType': 'decimal',
                                 'outputType': 'binary'
                             }),
                             content_type='application/json')
        
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['error'] is None
        # This should be a proper binary representation, not '-101010'
        # The current implementation will return '-101010' which is invalid
        assert not data['result'].startswith('-'), f"Binary result should not start with '-', got: {data['result']}"
        # Should be a valid binary string (only 0s and 1s)
        assert all(c in '01' for c in data['result']), f"Binary result should only contain 0s and 1s, got: {data['result']}"
    
    def test_convert_negative_to_octal_bug(self, client):
        """Test that negative numbers convert to octal correctly (should detect bug)."""
        response = client.post('/convert',
                             data=json.dumps({
                                 'input': '-42',
                                 'inputType': 'decimal',
                                 'outputType': 'octal'
                             }),
                             content_type='application/json')
        
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['error'] is None
        # This should be a proper octal representation, not '-52'
        assert not data['result'].startswith('-'), f"Octal result should not start with '-', got: {data['result']}"
        # Should be a valid octal string (only 0-7)
        assert all(c in '01234567' for c in data['result']), f"Octal result should only contain 0-7, got: {data['result']}"
    
    def test_convert_negative_to_hex_bug(self, client):
        """Test that negative numbers convert to hexadecimal correctly (should detect bug)."""
        response = client.post('/convert',
                             data=json.dumps({
                                 'input': '-42',
                                 'inputType': 'decimal',
                                 'outputType': 'hexadecimal'
                             }),
                             content_type='application/json')
        
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['error'] is None
        # This should be a proper hex representation, not '-2a'
        assert not data['result'].startswith('-'), f"Hex result should not start with '-', got: {data['result']}"
        # Should be a valid hex string (only 0-9, a-f)
        assert all(c in '0123456789abcdef' for c in data['result'].lower()), f"Hex result should only contain 0-9, a-f, got: {data['result']}"


class TestErrorHandling:
    """Test error handling in the API."""
    
    def test_invalid_input_type(self, client):
        """Test error handling for invalid input type."""
        response = client.post('/convert',
                             data=json.dumps({
                                 'input': '42',
                                 'inputType': 'invalid',
                                 'outputType': 'decimal'
                             }),
                             content_type='application/json')
        
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['result'] is None
        assert 'Invalid input type' in data['error']
    
    def test_invalid_output_type(self, client):
        """Test error handling for invalid output type."""
        response = client.post('/convert',
                             data=json.dumps({
                                 'input': '42',
                                 'inputType': 'decimal',
                                 'outputType': 'invalid'
                             }),
                             content_type='application/json')
        
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['result'] is None
        assert 'Invalid output type' in data['error']
    
    def test_invalid_text_input(self, client):
        """Test error handling for invalid text input."""
        response = client.post('/convert',
                             data=json.dumps({
                                 'input': 'invalid text',
                                 'inputType': 'text',
                                 'outputType': 'decimal'
                             }),
                             content_type='application/json')
        
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['result'] is None
        assert 'Unable to convert text to number' in data['error']
    
    def test_invalid_binary_input(self, client):
        """Test error handling for invalid binary input."""
        response = client.post('/convert',
                             data=json.dumps({
                                 'input': '123',  # Invalid binary
                                 'inputType': 'binary',
                                 'outputType': 'decimal'
                             }),
                             content_type='application/json')
        
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['result'] is None
        assert 'invalid literal for int()' in data['error']
    
    def test_invalid_octal_input(self, client):
        """Test error handling for invalid octal input."""
        response = client.post('/convert',
                             data=json.dumps({
                                 'input': '89',  # Invalid octal
                                 'inputType': 'octal',
                                 'outputType': 'decimal'
                             }),
                             content_type='application/json')
        
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['result'] is None
        assert 'invalid literal for int()' in data['error']
    
    def test_invalid_hexadecimal_input(self, client):
        """Test error handling for invalid hexadecimal input."""
        response = client.post('/convert',
                             data=json.dumps({
                                 'input': 'gh',  # Invalid hex
                                 'inputType': 'hexadecimal',
                                 'outputType': 'decimal'
                             }),
                             content_type='application/json')
        
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['result'] is None
        assert 'invalid literal for int()' in data['error']
    
    def test_invalid_base64_input(self, client):
        """Test error handling for invalid base64 input."""
        response = client.post('/convert',
                             data=json.dumps({
                                 'input': 'invalid_base64!',
                                 'inputType': 'base64',
                                 'outputType': 'decimal'
                             }),
                             content_type='application/json')
        
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['result'] is None
        assert 'Invalid base64 input' in data['error']
    
    def test_missing_input_field(self, client):
        """Test error handling for missing input field."""
        response = client.post('/convert',
                             data=json.dumps({
                                 'inputType': 'decimal',
                                 'outputType': 'text'
                             }),
                             content_type='application/json')
        
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['result'] is None
        assert "'input'" in data['error']
    
    def test_missing_input_type_field(self, client):
        """Test error handling for missing inputType field."""
        response = client.post('/convert',
                             data=json.dumps({
                                 'input': '42',
                                 'outputType': 'text'
                             }),
                             content_type='application/json')
        
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['result'] is None
        assert "'inputType'" in data['error']
    
    def test_missing_output_type_field(self, client):
        """Test error handling for missing outputType field."""
        response = client.post('/convert',
                             data=json.dumps({
                                 'input': '42',
                                 'inputType': 'decimal'
                             }),
                             content_type='application/json')
        
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['result'] is None
        assert "'outputType'" in data['error']


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_empty_input(self, client):
        """Test handling of empty input."""
        response = client.post('/convert',
                             data=json.dumps({
                                 'input': '',
                                 'inputType': 'decimal',
                                 'outputType': 'text'
                             }),
                             content_type='application/json')
        
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['result'] is None
        assert 'invalid literal for int()' in data['error']
    
    def test_whitespace_input(self, client):
        """Test handling of whitespace-only input."""
        response = client.post('/convert',
                             data=json.dumps({
                                 'input': '   ',
                                 'inputType': 'decimal',
                                 'outputType': 'text'
                             }),
                             content_type='application/json')
        
        data = json.loads(response.data)
        assert response.status_code == 200
        assert data['result'] is None
        assert 'invalid literal for int()' in data['error']
    
    def test_very_large_number(self, client):
        """Test handling of very large numbers."""
        large_num = "999999999999999999999999999999"
        response = client.post('/convert',
                             data=json.dumps({
                                 'input': large_num,
                                 'inputType': 'decimal',
                                 'outputType': 'binary'
                             }),
                             content_type='application/json')
        
        data = json.loads(response.data)
        assert response.status_code == 200
        # Should either succeed or fail gracefully
        if data['error'] is None:
            assert data['result'] is not None
        else:
            assert 'Unable to convert' in data['error'] or 'invalid literal' in data['error']
    
    def test_roundtrip_conversions(self, client):
        """Test roundtrip conversions to ensure consistency."""
        test_value = "42"
        conversions = [
            ('decimal', 'binary', 'binary', 'decimal'),
            ('decimal', 'hexadecimal', 'hexadecimal', 'decimal'),
            ('decimal', 'octal', 'octal', 'decimal'),
        ]
        
        for start_type, intermediate_type, end_type, final_type in conversions:
            # First conversion
            response1 = client.post('/convert',
                                  data=json.dumps({
                                      'input': test_value,
                                      'inputType': start_type,
                                      'outputType': intermediate_type
                                  }),
                                  content_type='application/json')
            
            data1 = json.loads(response1.data)
            assert data1['error'] is None
            
            # Second conversion back
            response2 = client.post('/convert',
                                  data=json.dumps({
                                      'input': data1['result'],
                                      'inputType': end_type,
                                      'outputType': final_type
                                  }),
                                  content_type='application/json')
            
            data2 = json.loads(response2.data)
            assert data2['error'] is None
            assert data2['result'] == test_value
