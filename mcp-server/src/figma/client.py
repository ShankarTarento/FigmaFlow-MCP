"""
Figma API Client
Handles communication with Figma API and data fetching
"""
import re
import os
from typing import Optional, Dict, Any, Tuple
import httpx
from pydantic import BaseModel, Field


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
    
    def __init__(self, access_token: Optional[str] = None) -> None:
        """
        Initialize Figma client
        
        Args:
            access_token: Figma API access token (defaults to env var)
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
    
    async def get_file(self, file_key: str) -> Dict[str, Any]:
        """
        Fetch entire Figma file
        
        Args:
            file_key: Figma file key
            
        Returns:
            File data as dictionary
        """
        url = f"{self.BASE_URL}/files/{file_key}"
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()
    
    async def get_node(self, file_key: str, node_id: str) -> FigmaNode:
        """
        Fetch specific node from Figma file
        
        Args:
            file_key: Figma file key
            node_id: Node ID (format: "123:456")
            
        Returns:
            FigmaNode object
        """
        url = f"{self.BASE_URL}/files/{file_key}/nodes"
        params = {"ids": node_id}
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
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
            https://www.figma.com/file/ABC123/Design?node-id=1-2 → ('ABC123', '1:2')
        """
        # Extract file key
        file_match = re.search(r'/file/([A-Za-z0-9]+)', url)
        file_key = file_match.group(1) if file_match else None
        
        # Extract node ID and convert format (1-2 → 1:2)
        node_match = re.search(r'node-id=([0-9]+-[0-9]+)', url)
        node_id = node_match.group(1).replace('-', ':') if node_match else None
        
        return file_key, node_id
    
    async def close(self) -> None:
        """Close the HTTP client"""
        await self.client.aclose()
