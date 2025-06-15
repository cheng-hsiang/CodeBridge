#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試中文轉換器
"""

import unittest
import sys
import os

# 添加 src 目錄到路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(os.path.dirname(current_dir), 'src')
sys.path.insert(0, src_dir)

from converter import ChineseConverter
from mappings import MappingManager


class TestChineseConverter(unittest.TestCase):
    """測試 ChineseConverter 類"""
    
    def setUp(self):
        """設置測試環境"""
        self.mapping_manager = MappingManager()
        self.converter = ChineseConverter(self.mapping_manager)
    
    def test_convert_simple_text(self):
        """測試簡單文本轉換"""
        text = "这是一个简单的测试。"
        converted, count = self.converter.convert_text(text)
        
        self.assertNotEqual(text, converted)
        self.assertGreater(count, 0)
        self.assertIn("這", converted)
        self.assertIn("個", converted)
        self.assertIn("簡", converted)
        self.assertIn("測", converted)
    
    def test_convert_empty_text(self):
        """測試空文本轉換"""
        text = ""
        converted, count = self.converter.convert_text(text)
        
        self.assertEqual(text, converted)
        self.assertEqual(count, 0)
    
    def test_convert_no_chinese_text(self):
        """測試無中文文本轉換"""
        text = "Hello World! 123 @#$"
        converted, count = self.converter.convert_text(text)
        
        self.assertEqual(text, converted)
        self.assertEqual(count, 0)
    
    def test_convert_mixed_text(self):
        """測試中英混合文本轉換"""
        text = "这是一个 Python 程序，用于处理数据。"
        converted, count = self.converter.convert_text(text)
        
        self.assertNotEqual(text, converted)
        self.assertGreater(count, 0)
        self.assertIn("Python", converted)  # 英文保持不變
        self.assertIn("這", converted)
        self.assertIn("程序", converted)
    
    def test_convert_technical_terms(self):
        """測試技術術語轉換"""
        text = "软件开发中的设计模式和架构"
        converted, count = self.converter.convert_text(text)
        
        self.assertNotEqual(text, converted)
        self.assertGreater(count, 0)
        self.assertIn("軟體開發", converted)
        self.assertIn("設計模式", converted)
        self.assertIn("架構", converted)
    
    def test_preview_conversion(self):
        """測試預覽轉換"""
        text = "这是一个测试。"
        conversions = self.converter.preview_conversion(text)
        
        self.assertIsInstance(conversions, list)
        self.assertGreater(len(conversions), 0)
        
        # 檢查轉換結果格式
        for simplified, traditional, count in conversions:
            self.assertIsInstance(simplified, str)
            self.assertIsInstance(traditional, str)
            self.assertIsInstance(count, int)
            self.assertGreater(count, 0)
    
    def test_find_chinese_text(self):
        """測試查找中文文本"""
        text = "Hello 这是中文 World 测试"
        matches = self.converter.find_chinese_text(text)
        
        self.assertIsInstance(matches, list)
        self.assertEqual(len(matches), 2)  # 應該找到兩段中文
        
        # 檢查第一段中文
        start, end, chinese = matches[0]
        self.assertEqual(text[start:end], chinese)
        self.assertIn("這", chinese + "这")  # 包含中文字符
    
    def test_validate_mapping(self):
        """測試映射驗證"""
        # 有效映射
        self.assertTrue(self.converter.validate_mapping("简体", "簡體"))
        self.assertTrue(self.converter.validate_mapping("测试", "測試"))
        
        # 無效映射
        self.assertFalse(self.converter.validate_mapping("", ""))
        self.assertFalse(self.converter.validate_mapping("test", "test"))  # 無中文
        self.assertFalse(self.converter.validate_mapping("很長" * 30, "很長" * 30))  # 過長
    
    def test_conversion_statistics(self):
        """測試轉換統計"""
        text = "这是一个包含多个中文词汇的测试文本。"
        stats = self.converter.get_conversion_statistics(text)
        
        self.assertIsInstance(stats, dict)
        self.assertIn('total_chars', stats)
        self.assertIn('chinese_chars', stats)
        self.assertIn('convertible_chars', stats)
        self.assertIn('conversion_mappings', stats)
        
        self.assertGreater(stats['chinese_chars'], 0)
        self.assertGreater(stats['convertible_chars'], 0)
        self.assertGreater(stats['conversion_mappings'], 0)
    
    def test_batch_convert(self):
        """測試批量轉換"""
        texts = [
            "第一个测试文本",
            "第二个测试文本",
            "Third text with 中文"
        ]
        
        results = self.converter.batch_convert(texts)
        
        self.assertEqual(len(results), len(texts))
        for converted, count in results:
            self.assertIsInstance(converted, str)
            self.assertIsInstance(count, int)
    
    def test_get_unique_conversions(self):
        """測試獲取唯一轉換對"""
        text = "这个测试中包含重复的词汇，这个测试很重要。"
        unique_conversions = self.converter.get_unique_conversions(text)
        
        self.assertIsInstance(unique_conversions, set)
        self.assertGreater(len(unique_conversions), 0)
        
        # 檢查是否包含預期的轉換對
        conversion_dict = dict(unique_conversions)
        if "这个" in conversion_dict:
            self.assertEqual(conversion_dict["这个"], "這個")


if __name__ == "__main__":
    unittest.main()
