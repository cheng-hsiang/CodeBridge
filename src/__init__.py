"""
CodeBridge - 程式碼簡繁轉換工具

Advanced Simplified to Traditional Chinese Converter for Development Projects
"""

__version__ = "2.0.0"
__author__ = "Development Team"
__email__ = "dev@codebridge.com"
__license__ = "MIT"

from .codebridge import CodeBridge
from .converter import ChineseConverter
from .mappings import MappingManager

__all__ = ['CodeBridge', 'ChineseConverter', 'MappingManager']
