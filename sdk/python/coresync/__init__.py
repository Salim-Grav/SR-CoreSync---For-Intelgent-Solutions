"""
S&R CoreSync Python SDK
Official Client Library for S&R CoreSync ERP & Sovereign Cloud Platform (v2.4 LTS)
"""

from .client import CoreSyncClient, CoreSyncError

__version__ = "2.4.0"
__all__ = ["CoreSyncClient", "CoreSyncError"]
