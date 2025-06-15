#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CodeBridge - 程式碼簡繁轉換工具
Setup script for installation
"""

from pathlib import Path
from setuptools import setup, find_packages

# 讀取 README.md
README_PATH = Path(__file__).parent / "README.md"
if README_PATH.exists():
    with open(README_PATH, "r", encoding="utf-8") as f:
        long_description = f.read()
else:
    long_description = "CodeBridge - Advanced Simplified to Traditional Chinese Converter for Development Projects"

# 讀取版本資訊
def get_version():
    """從 __init__.py 讀取版本資訊"""
    init_path = Path(__file__).parent / "src" / "__init__.py"
    if init_path.exists():
        with open(init_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("__version__"):
                    return line.split("=")[1].strip().strip('"').strip("'")
    return "2.0.0"

setup(
    name="codebridge",
    version=get_version(),
    author="Development Team",
    author_email="dev@codebridge.com",
    description="Advanced Simplified to Traditional Chinese Converter for Development Projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/codebridge/codebridge",
    project_urls={
        "Bug Tracker": "https://github.com/codebridge/codebridge/issues",
        "Documentation": "https://codebridge.readthedocs.io",
        "Source Code": "https://github.com/codebridge/codebridge",
    },
    packages=find_packages(),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Internationalization",
        "Topic :: Software Development :: Localization",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: Chinese (Traditional)",
    ],
    keywords=[
        "chinese", "simplified", "traditional", "converter", "translation",
        "localization", "i18n", "development", "code", "programming",
        "ai", "machine-learning", "cloud", "blockchain", "iot", "devops"
    ],
    python_requires=">=3.6",
    install_requires=[
        # CodeBridge 使用零相依性設計
        # 所有功能都使用 Python 標準庫實現
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "black>=21.0.0",
            "flake8>=3.8.0",
            "mypy>=0.800",
            "coverage>=5.0.0",
            "pre-commit>=2.0.0",
        ],
        "docs": [
            "sphinx>=3.0.0",
            "sphinx-rtd-theme>=0.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "codebridge=codebridge:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": [
            "*.txt",
            "*.json",
            "*.md",
            "config/*.json",
            "data/*.txt",
        ],
    },
    zip_safe=False,
    platforms=["any"],
    license="MIT",
    test_suite="tests",
)
