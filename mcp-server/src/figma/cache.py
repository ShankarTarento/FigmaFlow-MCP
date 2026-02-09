"""
Simple cache for Figma API responses to reduce API calls
"""
import json
import hashlib
import os
from pathlib import Path
from typing import Optional, Any
from datetime import datetime, timedelta


class FigmaCache:
    """Simple file-based cache for Figma API responses"""
    
    def __init__(self, cache_dir: str = "/tmp/figma_cache", ttl_hours: int = 24):
        """
        Initialize cache
        
        Args:
            cache_dir: Directory to store cache files
            ttl_hours: Time to live for cached items in hours
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)
    
    def _get_cache_key(self, file_key: str, node_id: Optional[str] = None) -> str:
        """Generate cache key for a request"""
        key_string = f"{file_key}:{node_id or 'full'}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> Path:
        """Get path to cache file"""
        return self.cache_dir / f"{cache_key}.json"
    
    def get(self, file_key: str, node_id: Optional[str] = None) -> Optional[Any]:
        """
        Get cached data if available and not expired
        
        Args:
            file_key: Figma file key
            node_id: Optional node ID
            
        Returns:
            Cached data or None if not found/expired
        """
        cache_key = self._get_cache_key(file_key, node_id)
        cache_path = self._get_cache_path(cache_key)
        
        if not cache_path.exists():
            return None
        
        try:
            # Check if cache is expired
            modified_time = datetime.fromtimestamp(cache_path.stat().st_mtime)
            if datetime.now() - modified_time > self.ttl:
                # Cache expired, remove it
                cache_path.unlink()
                return None
            
            # Load cached data
            with open(cache_path, 'r') as f:
                cached = json.load(f)
                print(f"✓ Using cached Figma data (cached {(datetime.now() - modified_time).seconds}s ago)")
                return cached['data']
        except (json.JSONDecodeError, KeyError, OSError):
            # Cache corrupted, remove it
            if cache_path.exists():
                cache_path.unlink()
            return None
    
    def set(self, file_key: str, data: Any, node_id: Optional[str] = None) -> None:
        """
        Store data in cache
        
        Args:
            file_key: Figma file key
            data: Data to cache
            node_id: Optional node ID
        """
        cache_key = self._get_cache_key(file_key, node_id)
        cache_path = self._get_cache_path(cache_key)
        
        try:
            with open(cache_path, 'w') as f:
                json.dump({
                    'data': data,
                    'cached_at': datetime.now().isoformat()
                }, f)
        except (OSError, TypeError):
            # Silently fail if caching doesn't work
            pass
    
    def clear(self) -> None:
        """Clear all cached data"""
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
        print("✓ Cache cleared")
    
    def clear_expired(self) -> None:
        """Remove expired cache entries"""
        removed = 0
        for cache_file in self.cache_dir.glob("*.json"):
            modified_time = datetime.fromtimestamp(cache_file.stat().st_mtime)
            if datetime.now() - modified_time > self.ttl:
                cache_file.unlink()
                removed += 1
        if removed > 0:
            print(f"✓ Removed {removed} expired cache entries")
