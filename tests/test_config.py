#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試配置管理
"""

import unittest
import tempfile
import os
import sys
import json

# 添加 src 目錄到路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(os.path.dirname(current_dir), 'src')
sys.path.insert(0, src_dir)

from config import Config


class TestConfig(unittest.TestCase):
    """測試 Config 類"""
    
    def test_default_config(self):
        """測試預設配置"""
        config = Config()
        
        self.assertIsInstance(config.target_extensions, set)
        self.assertIsInstance(config.exclude_dirs, set)
        self.assertGreater(len(config.target_extensions), 0)
        self.assertGreater(len(config.exclude_dirs), 0)
        self.assertGreater(config.max_file_size, 0)
        self.assertIn('INFO', ['DEBUG', 'INFO', 'WARNING', 'ERROR'])
    
    def test_load_config_from_file(self):
        """測試從檔案載入配置"""
        # 創建測試配置
        test_config = {
            "max_file_size": 5000000,
            "create_backup": True,
            "log_level": "DEBUG",
            "target_extensions": [".py", ".js"],
            "exclude_dirs": ["test_exclude"]
        }
        
        # 創建臨時配置檔案
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(test_config, f)
            temp_file = f.name
        
        try:
            # 載入配置
            config = Config(temp_file)
            
            self.assertEqual(config.max_file_size, 5000000)
            self.assertTrue(config.create_backup)
            self.assertEqual(config.log_level, "DEBUG")
            self.assertIn(".py", config.target_extensions)
            self.assertIn(".js", config.target_extensions)
            self.assertIn("test_exclude", config.exclude_dirs)
            
        finally:
            os.unlink(temp_file)
    
    def test_save_config(self):
        """測試儲存配置"""
        config = Config()
        config.set_config("test_key", "test_value")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            # 儲存配置
            result = config.save_config(temp_file)
            self.assertTrue(result)
            
            # 檢查檔案內容
            with open(temp_file, 'r', encoding='utf-8') as f:
                saved_config = json.load(f)
            
            self.assertEqual(saved_config["test_key"], "test_value")
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_add_remove_target_extension(self):
        """測試添加和移除目標檔案類型"""
        config = Config()
        initial_count = len(config.target_extensions)
        
        # 添加新的檔案類型
        config.add_target_extension("xyz")
        self.assertIn(".xyz", config.target_extensions)
        self.assertEqual(len(config.target_extensions), initial_count + 1)
        
        # 移除檔案類型
        config.remove_target_extension(".xyz")
        self.assertNotIn(".xyz", config.target_extensions)
        self.assertEqual(len(config.target_extensions), initial_count)
    
    def test_add_remove_exclude_dir(self):
        """測試添加和移除排除目錄"""
        config = Config()
        initial_count = len(config.exclude_dirs)
        
        # 添加排除目錄
        config.add_exclude_dir("test_exclude")
        self.assertIn("test_exclude", config.exclude_dirs)
        self.assertEqual(len(config.exclude_dirs), initial_count + 1)
        
        # 移除排除目錄
        config.remove_exclude_dir("test_exclude")
        self.assertNotIn("test_exclude", config.exclude_dirs)
        self.assertEqual(len(config.exclude_dirs), initial_count)
    
    def test_validate_config(self):
        """測試配置驗證"""
        config = Config()
        
        # 有效配置應該沒有錯誤
        errors = config.validate_config()
        self.assertEqual(len(errors), 0)
        
        # 設置無效值
        config.set_config("max_file_size", -1)
        config.set_config("max_workers", 0)
        config.set_config("log_level", "INVALID")
        
        errors = config.validate_config()
        self.assertGreater(len(errors), 0)
        self.assertTrue(any("max_file_size" in error for error in errors))
        self.assertTrue(any("max_workers" in error for error in errors))
        self.assertTrue(any("log_level" in error for error in errors))
    
    def test_get_set_config(self):
        """測試獲取和設置配置"""
        config = Config()
        
        # 獲取存在的配置
        max_file_size = config.get_config("max_file_size")
        self.assertIsNotNone(max_file_size)
        
        # 獲取不存在的配置（使用預設值）
        value = config.get_config("nonexistent_key", "default_value")
        self.assertEqual(value, "default_value")
        
        # 設置配置
        config.set_config("new_key", "new_value")
        self.assertEqual(config.get_config("new_key"), "new_value")
    
    def test_get_summary(self):
        """測試獲取配置摘要"""
        config = Config()
        summary = config.get_summary()
        
        self.assertIsInstance(summary, dict)
        self.assertIn("target_extensions_count", summary)
        self.assertIn("exclude_dirs_count", summary)
        self.assertIn("max_file_size_mb", summary)
        self.assertIn("create_backup", summary)
        self.assertIn("log_level", summary)
        
        # 檢查數值類型
        self.assertIsInstance(summary["target_extensions_count"], int)
        self.assertIsInstance(summary["exclude_dirs_count"], int)
        self.assertIsInstance(summary["max_file_size_mb"], (int, float))
    
    def test_create_default_config(self):
        """測試創建預設配置檔案"""
        config = Config()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            # 創建預設配置檔案
            result = config.create_default_config(temp_file)
            self.assertTrue(result)
            
            # 檢查檔案是否存在
            self.assertTrue(os.path.exists(temp_file))
            
            # 檢查檔案內容
            with open(temp_file, 'r', encoding='utf-8') as f:
                saved_config = json.load(f)
            
            self.assertIn("_comment", saved_config)
            self.assertIn("_description", saved_config)
            self.assertIn("target_extensions", saved_config)
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_config_string_representation(self):
        """測試配置的字串表示"""
        config = Config()
        
        str_repr = str(config)
        self.assertIsInstance(str_repr, str)
        self.assertIn("CodeBridge Config", str_repr)
        
        repr_str = repr(config)
        self.assertIsInstance(repr_str, str)
        self.assertIn("Config(", repr_str)


if __name__ == "__main__":
    unittest.main()
