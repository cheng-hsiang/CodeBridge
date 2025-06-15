#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CodeBridge - 配置管理
"""

import json
from pathlib import Path
from typing import Set, Dict, Any, Optional, List
import logging


class Config:
    """
    配置管理類
    
    管理 CodeBridge 的所有配置選項
    """
    
    # 預設配置
    DEFAULT_CONFIG = {
        "target_extensions": [
            ".py", ".js", ".jsx", ".ts", ".tsx", ".vue", ".html", ".htm",
            ".css", ".scss", ".sass", ".less", ".json", ".xml", ".yaml", ".yml",
            ".md", ".txt", ".csv", ".sql", ".conf", ".config", ".ini", ".toml",
            ".dockerfile", ".gitignore", ".env", ".properties", ".sh", ".bat",
            ".ps1", ".makefile", ".cmake", ".gradle", ".maven", ".npm", ".lock",
            ".java", ".c", ".cpp", ".h", ".hpp", ".cs", ".go", ".rs", ".php", 
            ".rb", ".swift", ".kt", ".scala", ".clj", ".hs", ".ml", ".r", ".m"
        ],
        "exclude_dirs": [
            "node_modules", "venv", "__pycache__", ".git", "dist", "build",
            ".next", ".nuxt", ".vscode", ".idea", "logs", "temp", "tmp",
            "coverage", ".pytest_cache", ".tox", ".env", "vendor", "target",
            "bin", "obj", ".gradle", ".maven", "out", ".output", ".svn",
            ".hg", "bower_components", ".sass-cache", ".nyc_output"
        ],
        "max_file_size": 10 * 1024 * 1024,  # 10MB
        "create_backup": False,
        "log_level": "INFO",
        "output_format": "console",
        "custom_mappings_file": None,
        "report_file": None,
        "encoding_detection": True,
        "parallel_processing": False,
        "max_workers": 4
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化配置
        
        Args:
            config_path: 配置檔案路徑
        """
        self.logger = logging.getLogger('CodeBridge.Config')
        self.config_data = self.DEFAULT_CONFIG.copy()
        
        if config_path:
            self.load_config(config_path)
        
        self._setup_properties()
    
    def _setup_properties(self):
        """設置配置屬性"""
        self.target_extensions = set(self.config_data["target_extensions"])
        self.exclude_dirs = set(self.config_data["exclude_dirs"])
        self.max_file_size = self.config_data["max_file_size"]
        self.create_backup = self.config_data["create_backup"]
        self.log_level = self.config_data["log_level"]
        self.output_format = self.config_data["output_format"]
        self.custom_mappings_file = self.config_data["custom_mappings_file"]
        self.report_file = self.config_data["report_file"]
        self.encoding_detection = self.config_data["encoding_detection"]
        self.parallel_processing = self.config_data["parallel_processing"]
        self.max_workers = self.config_data["max_workers"]
    
    def load_config(self, config_path: str) -> bool:
        """
        載入配置檔案
        
        Args:
            config_path: 配置檔案路徑
        
        Returns:
            bool: 是否載入成功
        """
        config_file = Path(config_path)
        
        if not config_file.exists():
            self.logger.warning(f"配置檔案不存在: {config_path}")
            return False
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
            
            # 合併配置
            self.config_data.update(user_config)
            self._setup_properties()
            
            self.logger.info(f"載入配置檔案: {config_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"載入配置檔案失敗: {e}")
            return False
    
    def save_config(self, config_path: str) -> bool:
        """
        儲存配置到檔案
        
        Args:
            config_path: 配置檔案路徑
        
        Returns:
            bool: 是否儲存成功
        """
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"儲存配置到: {config_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"儲存配置失敗: {e}")
            return False
    
    def create_default_config(self, config_path: str) -> bool:
        """
        創建預設配置檔案
        
        Args:
            config_path: 配置檔案路徑
        
        Returns:
            bool: 是否創建成功
        """
        config_content = {
            "_comment": "CodeBridge 配置檔案",
            "_description": {
                "target_extensions": "要處理的檔案類型",
                "exclude_dirs": "要排除的目錄",
                "max_file_size": "最大檔案大小 (bytes)",
                "create_backup": "是否創建備份檔案",
                "log_level": "日誌級別 (DEBUG, INFO, WARNING, ERROR)",
                "output_format": "輸出格式 (console, json, markdown)",
                "custom_mappings_file": "自定義映射檔案路徑",
                "report_file": "報告輸出檔案路徑",
                "encoding_detection": "是否啟用編碼自動檢測",
                "parallel_processing": "是否啟用平行處理",
                "max_workers": "最大工作執行緒數"
            }
        }
        config_content.update(self.DEFAULT_CONFIG)
        
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_content, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"創建預設配置檔案: {config_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"創建配置檔案失敗: {e}")
            return False
    
    def get_config(self, key: str, default=None) -> Any:
        """
        獲取配置值
        
        Args:
            key: 配置鍵
            default: 預設值
        
        Returns:
            Any: 配置值
        """
        return self.config_data.get(key, default)
    
    def set_config(self, key: str, value: Any) -> None:
        """
        設置配置值
        
        Args:
            key: 配置鍵
            value: 配置值
        """
        self.config_data[key] = value
        self._setup_properties()
    
    def add_target_extension(self, extension: str) -> None:
        """
        添加目標檔案類型
        
        Args:
            extension: 檔案擴展名
        """
        if not extension.startswith('.'):
            extension = '.' + extension
        
        self.target_extensions.add(extension)
        self.config_data["target_extensions"] = list(self.target_extensions)
    
    def remove_target_extension(self, extension: str) -> None:
        """
        移除目標檔案類型
        
        Args:
            extension: 檔案擴展名
        """
        if not extension.startswith('.'):
            extension = '.' + extension
        
        self.target_extensions.discard(extension)
        self.config_data["target_extensions"] = list(self.target_extensions)
    
    def add_exclude_dir(self, directory: str) -> None:
        """
        添加排除目錄
        
        Args:
            directory: 目錄名稱
        """
        self.exclude_dirs.add(directory)
        self.config_data["exclude_dirs"] = list(self.exclude_dirs)
    
    def remove_exclude_dir(self, directory: str) -> None:
        """
        移除排除目錄
        
        Args:
            directory: 目錄名稱
        """
        self.exclude_dirs.discard(directory)
        self.config_data["exclude_dirs"] = list(self.exclude_dirs)
    
    def validate_config(self) -> List[str]:
        """
        驗證配置的有效性
        
        Returns:
            List[str]: 錯誤訊息列表
        """
        errors = []
        
        # 檢查檔案大小限制
        if self.max_file_size <= 0:
            errors.append("max_file_size 必須大於 0")
        
        # 檢查工作執行緒數
        if self.max_workers <= 0:
            errors.append("max_workers 必須大於 0")
        
        # 檢查日誌級別
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR"]
        if self.log_level not in valid_log_levels:
            errors.append(f"log_level 必須是 {valid_log_levels} 之一")
        
        # 檢查輸出格式
        valid_formats = ["console", "json", "markdown"]
        if self.output_format not in valid_formats:
            errors.append(f"output_format 必須是 {valid_formats} 之一")
        
        # 檢查自定義映射檔案
        if self.custom_mappings_file:
            if not Path(self.custom_mappings_file).exists():
                errors.append(f"自定義映射檔案不存在: {self.custom_mappings_file}")
        
        return errors
    
    def get_summary(self) -> Dict[str, Any]:
        """
        獲取配置摘要
        
        Returns:
            Dict[str, Any]: 配置摘要
        """
        return {
            "target_extensions_count": len(self.target_extensions),
            "exclude_dirs_count": len(self.exclude_dirs),
            "max_file_size_mb": round(self.max_file_size / (1024 * 1024), 2),
            "create_backup": self.create_backup,
            "log_level": self.log_level,
            "parallel_processing": self.parallel_processing,
            "max_workers": self.max_workers if self.parallel_processing else 1
        }
    
    def __str__(self) -> str:
        """字串表示"""
        return f"CodeBridge Config: {len(self.target_extensions)} extensions, {len(self.exclude_dirs)} excluded dirs"
    
    def __repr__(self) -> str:
        """詳細字串表示"""
        return f"Config(target_extensions={len(self.target_extensions)}, exclude_dirs={len(self.exclude_dirs)}, max_file_size={self.max_file_size})"
