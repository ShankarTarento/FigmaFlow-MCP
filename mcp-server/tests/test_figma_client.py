"""
Basic tests for Figma client
"""
import pytest
from src.figma.client import FigmaClient


def test_parse_file_url_basic():
    """Test parsing basic Figma URL"""
    url = "https://www.figma.com/file/ABC123/MyDesign"
    file_key, node_id = FigmaClient.parse_file_url(url)
    
    assert file_key == "ABC123"
    assert node_id is None


def test_parse_file_url_with_node():
    """Test parsing Figma URL with node ID"""
    url = "https://www.figma.com/file/ABC123/MyDesign?node-id=1-2"
    file_key, node_id = FigmaClient.parse_file_url(url)
    
    assert file_key == "ABC123"
    assert node_id == "1:2"


def test_parse_file_url_invalid():
    """Test parsing invalid URL"""
    url = "https://example.com/notfigma"
    file_key, node_id = FigmaClient.parse_file_url(url)
    
    assert file_key is None
    assert node_id is None
