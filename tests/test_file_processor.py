#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試檔案處理器
"""

import unittest
import tempfile
import os
import sys
from pathlib import Path

# 添加 src 目錄到路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(os.path.dirname(current_dir), 'src')
sys.path.insert(0, src_dir)

from file_processor import FileProcessor
from converter import ChineseConverter
from mappings import MappingManager
from config import Config


class TestFileProcessor(unittest.TestCase):
    """測試 FileProcessor 類"""
    
    def setUp(self):
        """設置測試環境"""
        self.config = Config()
        self.file_processor = FileProcessor(self.config)
        self.mapping_manager = MappingManager()
        self.converter = ChineseConverter(self.mapping_manager)
    
    def test_process_file_with_chinese(self):
        """測試處理包含中文的檔案"""
        # 創建臨時檔案
        test_content = "这是一个测试文件，包含简体中文。"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', suffix='.txt') as f:
            f.write(test_content)
            temp_file = Path(f.name)
        
        try:
            # 處理檔案
            result = self.file_processor.process_file(temp_file, self.converter, preview_mode=False)
            
            self.assertTrue(result.processed)
            self.assertGreater(result.conversions, 0)
            self.assertIsNone(result.error)
            
            # 檢查檔案是否被修改
            with open(temp_file, 'r', encoding='utf-8') as f:
                modified_content = f.read()
            
            self.assertNotEqual(test_content, modified_content)
            self.assertIn("這", modified_content)
            self.assertIn("個", modified_content)
            
        finally:
            if temp_file.exists():
                temp_file.unlink()
    
    def test_process_file_preview_mode(self):
        """測試預覽模式處理檔案"""
        # 創建臨時檔案
        test_content = "这是预览模式测试。"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', suffix='.txt') as f:
            f.write(test_content)
            temp_file = Path(f.name)
        
        try:
            # 預覽模式處理檔案
            result = self.file_processor.process_file(temp_file, self.converter, preview_mode=True)
            
            self.assertFalse(result.processed)  # 預覽模式不應修改檔案
            self.assertGreater(result.conversions, 0)
            self.assertGreater(len(result.preview_data), 0)
            self.assertIsNone(result.error)
            
            # 檢查檔案內容未被修改
            with open(temp_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.assertEqual(test_content, content)
            
        finally:
            if temp_file.exists():
                temp_file.unlink()
    
    def test_process_file_no_chinese(self):
        """測試處理不包含中文的檔案"""
        # 創建臨時檔案
        test_content = "This is an English test file."
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', suffix='.txt') as f:
            f.write(test_content)
            temp_file = Path(f.name)
        
        try:
            # 處理檔案
            result = self.file_processor.process_file(temp_file, self.converter, preview_mode=False)
            
            self.assertFalse(result.processed)
            self.assertEqual(result.conversions, 0)
            self.assertIsNone(result.error)
            
        finally:
            if temp_file.exists():
                temp_file.unlink()
    
    def test_process_nonexistent_file(self):
        """測試處理不存在的檔案"""
        nonexistent_file = Path("/nonexistent/file.txt")
        
        result = self.file_processor.process_file(nonexistent_file, self.converter)
        
        self.assertFalse(result.processed)
        self.assertEqual(result.conversions, 0)
        self.assertIsNotNone(result.error)
    
    def test_is_text_file(self):
        """測試文字檔案判斷"""
        # 創建文字檔案
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', suffix='.txt') as f:
            f.write("This is a text file.")
            text_file = Path(f.name)
        
        try:
            self.assertTrue(self.file_processor.is_text_file(text_file))
        finally:
            if text_file.exists():
                text_file.unlink()
        
        # 測試二進位檔案
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            f.write(b'\x00\x01\x02\x03')
            binary_file = Path(f.name)
        
        try:
            self.assertFalse(self.file_processor.is_text_file(binary_file))
        finally:
            if binary_file.exists():
                binary_file.unlink()
    
    def test_get_file_info(self):
        """測試獲取檔案資訊"""
        # 創建測試檔案
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', suffix='.py') as f:
            f.write("# Python test file")
            test_file = Path(f.name)
        
        try:
            file_info = self.file_processor.get_file_info(test_file)
            
            self.assertIsInstance(file_info, dict)
            self.assertIn('path', file_info)
            self.assertIn('name', file_info)
            self.assertIn('size', file_info)
            self.assertIn('extension', file_info)
            self.assertIn('is_text', file_info)
            
            self.assertEqual(file_info['extension'], '.py')
            self.assertTrue(file_info['is_text'])
            self.assertGreater(file_info['size'], 0)
            
        finally:
            if test_file.exists():
                test_file.unlink()
    
    def test_scan_directory(self):
        """測試掃描目錄"""
        # 創建臨時目錄和檔案
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # 創建一些測試檔案
            (temp_path / "test1.py").write_text("# Python file", encoding='utf-8')
            (temp_path / "test2.js").write_text("// JavaScript file", encoding='utf-8')
            (temp_path / "test3.txt").write_text("Text file", encoding='utf-8')
            (temp_path / "ignore.bin").write_bytes(b'\x00\x01\x02')  # 二進位檔案
            
            # 創建排除目錄
            exclude_dir = temp_path / "node_modules"
            exclude_dir.mkdir()
            (exclude_dir / "should_ignore.js").write_text("Should be ignored", encoding='utf-8')
            
            # 掃描目錄
            files = self.file_processor.scan_directory(temp_path)
            
            # 檢查結果
            self.assertIsInstance(files, list)
            file_names = [f.name for f in files]
            
            self.assertIn("test1.py", file_names)
            self.assertIn("test2.js", file_names)
            self.assertIn("test3.txt", file_names)
            self.assertNotIn("should_ignore.js", file_names)  # 應該被排除
    
    def test_batch_process(self):
        """測試批量處理檔案"""
        # 創建多個測試檔案
        test_files = []
        
        try:
            for i in range(3):
                with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', suffix='.txt') as f:
                    f.write(f"这是第{i+1}个测试文件。")
                    test_files.append(Path(f.name))
            
            # 批量處理
            results = self.file_processor.batch_process(test_files, self.converter, preview_mode=True)
            
            self.assertEqual(len(results), len(test_files))
            
            for result in results:
                self.assertGreater(result.conversions, 0)
                self.assertIsNone(result.error)
                
        finally:
            # 清理檔案
            for file_path in test_files:
                if file_path.exists():
                    file_path.unlink()


if __name__ == "__main__":
    unittest.main()
