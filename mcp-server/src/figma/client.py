"""
Figma API Client
Handles communication with Figma API and data fetching
"""
import re
import os
import asyncio
from typing import Optional, Dict, Any, Tuple
import httpx
from pydantic import BaseModel, Field
from .cache import FigmaCache


class BoundingBox(BaseModel):
    """Bounding box for a node"""
    x: float
    y: float
    width: float
    height: float


class ColorRGBA(BaseModel):
    """RGBA color representation"""
    r: float
    g: float
    b: float
    a: float = 1.0


class FigmaNode(BaseModel):
    """Represents a Figma node"""
    id: str
    name: str
    type: str
    visible: bool = True
    children: list['FigmaNode'] = Field(default_factory=list)
    
    # Layout properties
    absolute_bounding_box: Optional[BoundingBox] = Field(default=None, alias='absoluteBoundingBox')
    background_color: Optional[ColorRGBA] = Field(default=None, alias='backgroundColor')
    
    # Text properties
    characters: Optional[str] = None
    
    # Style properties
    fills: Optional[list[Dict[str, Any]]] = None
    strokes: Optional[list[Dict[str, Any]]] = None
    
    class Config:
        populate_by_name = True


class FigmaClient:
    """Client for Figma API interactions"""
    
    BASE_URL = "https://api.figma.com/v1"
    
    def __init__(self, access_token: Optional[str] = None, use_cache: bool = True) -> None:
        """
        Initialize Figma client
        
        Args:
            access_token: Figma API access token (defaults to env var)
            use_cache: Whether to use caching to reduce API calls
        """
        self.access_token = access_token or os.getenv("FIGMA_ACCESS_TOKEN")
        
        if not self.access_token:
            raise ValueError("Figma access token not found. Set FIGMA_ACCESS_TOKEN environment variable.")
        
        self.client = httpx.AsyncClient(
            headers={
                "X-Figma-Token": self.access_token
            },
            timeout=30.0
        )
        
        # Initialize cache
        self.use_cache = use_cache
        self.cache = FigmaCache() if use_cache else None
    
    async def _request_with_retry(
        self,
        method: str,
        url: str,
        max_retries: int = 3,
        **kwargs
    ) -> httpx.Response:
        """
        Make HTTP request with retry logic for rate limiting
        
        Args:
            method: HTTP method (GET, POST, etc.)
            url: URL to request
            max_retries: Maximum number of retry attempts
            **kwargs: Additional arguments to pass to httpx
            
        Returns:
            HTTP response
            
        Raises:
            httpx.HTTPStatusError: If all retries fail
        """
        for attempt in range(max_retries):
            try:
                response = await self.client.request(method, url, **kwargs)
                response.raise_for_status()
                return response
            except httpx.HTTPStatusError as e:
                # Handle rate limiting (429)
                if e.response.status_code == 429:
                    if attempt < max_retries - 1:
                        # Exponential backoff: 2^attempt seconds
                        wait_time = 2 ** attempt
                        print(f"⚠️  Rate limited by Figma API. Retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})")
                        await asyncio.sleep(wait_time)
                        continue
                # Re-raise if not rate limiting or final attempt
                raise
        
        # Should never reach here, but just in case
        raise httpx.HTTPStatusError("Max retries exceeded", request=None, response=None)
    
    async def get_file(self, file_key: str) -> Dict[str, Any]:
        """
        Fetch entire Figma file with automatic retry on rate limiting
        Caches results to reduce API calls
        
        Args:
            file_key: Figma file key
            
        Returns:
            File data as dictionary
        """
        # Check cache first
        if self.use_cache and self.cache:
            cached_data = self.cache.get(file_key)
            if cached_data is not None:
                return cached_data
        
        # Not cached, fetch from API
        url = f"{self.BASE_URL}/files/{file_key}"
        response = await self._request_with_retry("GET", url)
        data = response.json()
        
        # Cache the result
        if self.use_cache and self.cache:
            self.cache.set(file_key, data)
        
        return data
    
    async def get_node(self, file_key: str, node_id: str) -> FigmaNode:
        """
        Fetch specific node from Figma file with automatic retry on rate limiting
        Caches results to reduce API calls
        
        Args:
            file_key: Figma file key
            node_id: Node ID (format: "123:456")
            
        Returns:
            FigmaNode object
        """
        # Check cache first
        if self.use_cache and self.cache:
            cached_data = self.cache.get(file_key, node_id)
            if cached_data is not None:
                return FigmaNode(**cached_data['nodes'][node_id]['document'])
        
        # Not cached, fetch from API
        url = f"{self.BASE_URL}/files/{file_key}/nodes"
        params = {"ids": node_id}
        response = await self._request_with_retry("GET", url, params=params)
        data = response.json()
        
        # Cache the result
        if self.use_cache and self.cache:
            self.cache.set(file_key, data, node_id)
        
        # Extract the node data
        node_data = data["nodes"][node_id]["document"]
        return FigmaNode(**node_data)
    
    @staticmethod
    def parse_file_url(url: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Extract file key and node ID from Figma URL
        
        Args:
            url: Figma file URL
            
        Returns:
            Tuple of (file_key, node_id)
            
        Examples:
            https://www.figma.com/file/ABC123/Design → ('ABC123', None)
            https://www.figma.com/design/ABC123/Design?node-id=1-2 → ('ABC123', '1:2')
        """
        # Extract file key - support both /file/ and /design/ URLs
        file_match = re.search(r'/(?:file|design)/([A-Za-z0-9]+)', url)
        file_key = file_match.group(1) if file_match else None
        
        # Extract node ID and convert format (1-2 → 1:2)
        node_match = re.search(r'node-id=([0-9]+-[0-9]+)', url)
        node_id = node_match.group(1).replace('-', ':') if node_match else None
        
        return file_key, node_id
    
    async def close(self) -> None:
        """Close the HTTP client"""
        await self.client.aclose()
