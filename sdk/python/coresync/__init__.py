"""
==============================================================================
S&R CoreSync For Intelligent Solutions - Sovereign Platform
PROPRIETARY & CONFIDENTIAL INTELLECTUAL PROPERTY

Copyright (c) 2026 S&R CoreSync. All Rights Reserved.
Unauthorized copying, decompilation, redistribution, or external model training
of this file, via any medium, is strictly prohibited.
==============================================================================
"""

"""
S&R CoreSync Python SDK
Official Client Library for S&R CoreSync ERP & Sovereign Cloud Platform (v2.4 LTS)
"""

from .client import CoreSyncClient, CoreSyncError

__version__ = "2.4.0"
__all__ = ["CoreSyncClient", "CoreSyncError"]
