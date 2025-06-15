#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試映射管理器
"""

import unittest
import tempfile
import os
import sys

# 添加 src 目錄到路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(os.path.dirname(current_dir), 'src')
sys.path.insert(0, src_dir)

from mappings import MappingManager


class TestMappingManager(unittest.TestCase):
    """測試 MappingManager 類"""
    
    def setUp(self):
        """設置測試環境"""
        self.mapping_manager = MappingManager()
    
    def test_builtin_mappings_loaded(self):
        """測試內建映射已載入"""
        builtin_mappings = self.mapping_manager.get_builtin_mappings()
        
        self.assertIsInstance(builtin_mappings, dict)
        self.assertGreater(len(builtin_mappings), 1000)  # 應該有大量內建映射
        
        # 檢查一些基本映射
        self.assertEqual(builtin_mappings.get("简体"), "簡體")
        self.assertEqual(builtin_mappings.get("转换"), "轉換")
        self.assertEqual(builtin_mappings.get("软件"), "軟件")
    
    def test_get_all_mappings(self):
        """測試獲取所有映射"""
        all_mappings = self.mapping_manager.get_all_mappings()
        
        self.assertIsInstance(all_mappings, dict)
        self.assertGreater(len(all_mappings), 0)
        
        # 應該包含內建映射
        builtin_mappings = self.mapping_manager.get_builtin_mappings()
        for key, value in builtin_mappings.items():
            self.assertEqual(all_mappings[key], value)
    
    def test_add_custom_mapping(self):
        """測試添加自定義映射"""
        # 添加自定義映射
        result = self.mapping_manager.add_custom_mapping("测试词", "測試詞")
        self.assertTrue(result)
        
        # 檢查映射是否已添加
        all_mappings = self.mapping_manager.get_all_mappings()
        self.assertEqual(all_mappings["测试词"], "測試詞")
        
        # 檢查自定義映射
        custom_mappings = self.mapping_manager.get_custom_mappings()
        self.assertEqual(custom_mappings["测试词"], "測試詞")
    
    def test_remove_custom_mapping(self):
        """測試移除自定義映射"""
        # 添加自定義映射
        self.mapping_manager.add_custom_mapping("临时词", "臨時詞")
        
        # 移除映射
        result = self.mapping_manager.remove_custom_mapping("临时词")
        self.assertTrue(result)
        
        # 檢查映射是否已移除
        custom_mappings = self.mapping_manager.get_custom_mappings()
        self.assertNotIn("临时词", custom_mappings)
        
        # 嘗試移除不存在的映射
        result = self.mapping_manager.remove_custom_mapping("不存在的词")
        self.assertFalse(result)
    
    def test_load_custom_mappings_from_file(self):
        """測試從檔案載入自定義映射"""
        # 創建臨時檔案
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            f.write("# 測試映射檔案\n")
            f.write("文件测试:檔案測試\n")
            f.write("另一个词:另一個詞\n")
            f.write("# 註解行\n")
            f.write("无效行\n")  # 沒有冒號的行
            f.write("第三个:第三個\n")
            temp_file = f.name
        
        try:
            # 載入映射
            count = self.mapping_manager.load_custom_mappings(temp_file)
            
            # 應該載入3個有效映射
            self.assertEqual(count, 3)
            
            # 檢查映射是否正確載入
            custom_mappings = self.mapping_manager.get_custom_mappings()
            self.assertEqual(custom_mappings["文件测试"], "檔案測試")
            self.assertEqual(custom_mappings["另一个词"], "另一個詞")
            self.assertEqual(custom_mappings["第三个"], "第三個")
            
        finally:
            # 清理臨時檔案
            os.unlink(temp_file)
    
    def test_load_nonexistent_file(self):
        """測試載入不存在的檔案"""
        with self.assertRaises(FileNotFoundError):
            self.mapping_manager.load_custom_mappings("不存在的檔案.txt")
    
    def test_save_custom_mappings(self):
        """測試儲存自定義映射"""
        # 添加一些自定義映射
        self.mapping_manager.add_custom_mapping("保存测试1", "保存測試1")
        self.mapping_manager.add_custom_mapping("保存测试2", "保存測試2")
        
        # 創建臨時檔案路徑
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_file = f.name
        
        try:
            # 儲存映射
            result = self.mapping_manager.save_custom_mappings(temp_file)
            self.assertTrue(result)
            
            # 檢查檔案內容
            with open(temp_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.assertIn("保存测试1:保存測試1", content)
            self.assertIn("保存测试2:保存測試2", content)
            
        finally:
            # 清理臨時檔案
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_get_category_stats(self):
        """測試獲取分類統計"""
        stats = self.mapping_manager.get_category_stats()
        
        self.assertIsInstance(stats, dict)
        self.assertIn('基本字符', stats)
        self.assertIn('科技開發', stats)
        self.assertIn('業務管理', stats)
        self.assertIn('系統架構', stats)
        self.assertIn('專業術語', stats)
        
        # 檢查統計數字
        for category, count in stats.items():
            self.assertIsInstance(count, int)
            self.assertGreaterEqual(count, 0)
    
    def test_search_mappings(self):
        """測試搜尋映射"""
        # 搜尋包含"软件"的映射
        results = self.mapping_manager.search_mappings("软件")
        
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        
        # 檢查結果格式
        for simplified, traditional in results:
            self.assertIsInstance(simplified, str)
            self.assertIsInstance(traditional, str)
            self.assertTrue("软件" in simplified or "軟件" in traditional)
    
    def test_export_mappings_json(self):
        """測試匯出映射為JSON"""
        # 創建臨時檔案
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as f:
            temp_file = f.name
        
        try:
            # 匯出映射
            result = self.mapping_manager.export_mappings_json(temp_file)
            self.assertTrue(result)
            
            # 檢查檔案是否存在且有內容
            self.assertTrue(os.path.exists(temp_file))
            self.assertGreater(os.path.getsize(temp_file), 0)
            
            # 檢查JSON格式
            import json
            with open(temp_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.assertIn('metadata', data)
            self.assertIn('mappings', data)
            self.assertIn('total_mappings', data['metadata'])
            
        finally:
            # 清理臨時檔案
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_mappings_updated_flag(self):
        """測試映射更新標誌"""
        # 初始狀態應該為False
        self.assertFalse(self.mapping_manager.is_mappings_updated())
        
        # 添加自定義映射後應該為True
        self.mapping_manager.add_custom_mapping("更新测试", "更新測試")
        self.assertTrue(self.mapping_manager.is_mappings_updated())
        
        # 再次檢查應該為False（已重置）
        self.assertFalse(self.mapping_manager.is_mappings_updated())


if __name__ == "__main__":
    unittest.main()
