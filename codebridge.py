#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CodeBridge - 主要執行檔案
"""

import sys
from pathlib import Path

# 添加 src 目錄到 Python 路徑
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

from src.codebridge import main

if __name__ == "__main__":
    sys.exit(main())
