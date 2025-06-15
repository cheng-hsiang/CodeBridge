#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CodeBridge - 測試套件
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import sys
import os

# 添加 src 目錄到 Python 路徑
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from src.converter import ChineseConverter
from src.mappings import MappingManager
from src.file_processor import FileProcessor
from src.config import Config
from src.codebridge import CodeBridge


class TestChineseConverter(unittest.TestCase):
    """測試中文轉換器"""
    
    def setUp(self):
        """設置測試環境"""
        self.mapping_manager = MappingManager()
        self.converter = ChineseConverter(self.mapping_manager)
    
    def test_basic_conversion(self):
        """測試基本轉換"""
        text = "这是一个测试程序"
        converted, count = self.converter.convert_text(text)
        self.assertEqual(converted, "這是一個測試程序")
        self.assertGreater(count, 0)
    
    def test_no_conversion_needed(self):
        """測試不需要轉換的文本"""
        text = "This is English text"
        converted, count = self.converter.convert_text(text)
        self.assertEqual(converted, text)
        self.assertEqual(count, 0)
    
    def test_empty_text(self):
        """測試空文本"""
        converted, count = self.converter.convert_text("")
        self.assertEqual(converted, "")
        self.assertEqual(count, 0)
    
    def test_preview_conversion(self):
        """測試預覽轉換"""
        text = "数据库连接错误"
        preview = self.converter.preview_conversion(text)
        self.assertIsInstance(preview, list)
        self.assertGreater(len(preview), 0)
        
        # 檢查預覽結果格式
        for simplified, traditional, count in preview:
            self.assertIsInstance(simplified, str)
            self.assertIsInstance(traditional, str)
            self.assertIsInstance(count, int)
            self.assertGreater(count, 0)
    
    def test_tech_terms_conversion(self):
        """測試技術術語轉換"""
        text = "人工智能和机器学习算法优化"
        converted, count = self.converter.convert_text(text)
        expected = "人工智慧和機器學習演算法最佳化"
        self.assertEqual(converted, expected)
    
    def test_mixed_content(self):
        """測試混合內容"""
        text = "// 这是一个JavaScript函数\nfunction test() {\n  console.log('数据处理');\n}"
        converted, count = self.converter.convert_text(text)
        self.assertIn("這是一個", converted)
        self.assertIn("數據處理", converted)


class TestMappingManager(unittest.TestCase):
    """測試映射管理器"""
    
    def setUp(self):
        """設置測試環境"""
        self.mapping_manager = MappingManager()
    
    def test_get_all_mappings(self):
        """測試獲取所有映射"""
        mappings = self.mapping_manager.get_all_mappings()
        self.assertIsInstance(mappings, dict)
        self.assertGreater(len(mappings), 0)
        
        # 檢查一些已知的映射
        self.assertIn("数据", mappings)
        self.assertEqual(mappings["数据"], "數據")
    
    def test_add_custom_mapping(self):
        """測試添加自定義映射"""
        result = self.mapping_manager.add_custom_mapping("测试词", "測試詞")
        self.assertTrue(result)
        
        mappings = self.mapping_manager.get_all_mappings()
        self.assertIn("测试词", mappings)
        self.assertEqual(mappings["测试词"], "測試詞")
    
    def test_remove_custom_mapping(self):
        """測試移除自定義映射"""
        # 先添加
        self.mapping_manager.add_custom_mapping("临时词", "臨時詞")
        
        # 再移除
        result = self.mapping_manager.remove_custom_mapping("临时词")
        self.assertTrue(result)
        
        mappings = self.mapping_manager.get_all_mappings()
        self.assertNotIn("临时词", mappings)
    
    def test_search_mappings(self):
        """測試搜尋映射"""
        results = self.mapping_manager.search_mappings("数据")
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        
        # 檢查結果格式
        for simplified, traditional in results:
            self.assertTrue("数据" in simplified or "數據" in traditional)
    
    def test_category_stats(self):
        """測試分類統計"""
        stats = self.mapping_manager.get_category_stats()
        self.assertIsInstance(stats, dict)
        self.assertIn("基本字符", stats)
        self.assertIn("科技開發", stats)
        
        # 檢查統計數字合理性
        total = sum(stats.values())
        mappings_count = len(self.mapping_manager.get_all_mappings())
        self.assertEqual(total, mappings_count)


class TestFileProcessor(unittest.TestCase):
    """測試檔案處理器"""
    
    def setUp(self):
        """設置測試環境"""
        self.config = Config()
        self.file_processor = FileProcessor(self.config)
        self.mapping_manager = MappingManager()
        self.converter = ChineseConverter(self.mapping_manager)
        
        # 創建臨時目錄
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """清理測試環境"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_process_text_file(self):
        """測試處理文字檔案"""
        # 創建測試檔案
        test_file = self.temp_dir / "test.txt"
        test_content = "这是一个测试文件，包含简体中文。"
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        # 處理檔案
        result = self.file_processor.process_file(test_file, self.converter, False)
        
        self.assertTrue(result.processed)
        self.assertGreater(result.conversions, 0)
        self.assertIsNone(result.error)
        
        # 檢查檔案內容是否已轉換
        with open(test_file, 'r', encoding='utf-8') as f:
            converted_content = f.read()
        
        self.assertIn("這是一個", converted_content)
        self.assertIn("測試", converted_content)
    
    def test_preview_mode(self):
        """測試預覽模式"""
        # 創建測試檔案
        test_file = self.temp_dir / "preview.py"
        test_content = "# 数据处理函数\ndef process_data():\n    pass"
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        # 預覽模式處理
        result = self.file_processor.process_file(test_file, self.converter, True)
        
        self.assertFalse(result.processed)  # 預覽模式不修改檔案
        self.assertGreater(result.conversions, 0)
        self.assertGreater(len(result.preview_data), 0)
        
        # 檢查檔案內容未被修改
        with open(test_file, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        self.assertEqual(original_content, test_content)
    
    def test_scan_directory(self):
        """測試掃描目錄"""
        # 創建測試檔案結構
        (self.temp_dir / "src").mkdir()
        (self.temp_dir / "tests").mkdir()
        (self.temp_dir / "node_modules").mkdir()
        
        # 創建各種檔案
        test_files = [
            "src/main.py",
            "src/utils.js",
            "tests/test_main.py",
            "README.md",
            "node_modules/package.json"  # 應該被排除
        ]
        
        for file_path in test_files:
            full_path = self.temp_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, 'w') as f:
                f.write("test content")
        
        # 掃描目錄
        files = self.file_processor.scan_directory(self.temp_dir)
        
        # 檢查結果
        self.assertGreater(len(files), 0)
        
        # 檢查 node_modules 中的檔案被排除
        for file_path in files:
            self.assertNotIn("node_modules", str(file_path))


class TestConfig(unittest.TestCase):
    """測試配置管理"""
    
    def setUp(self):
        """設置測試環境"""
        self.config = Config()
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """清理測試環境"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_default_config(self):
        """測試預設配置"""
        self.assertIsInstance(self.config.target_extensions, set)
        self.assertIsInstance(self.config.exclude_dirs, set)
        self.assertGreater(len(self.config.target_extensions), 0)
        self.assertGreater(len(self.config.exclude_dirs), 0)
    
    def test_add_remove_extensions(self):
        """測試添加和移除檔案類型"""
        original_count = len(self.config.target_extensions)
        
        # 添加新的檔案類型
        self.config.add_target_extension("xyz")
        self.assertIn(".xyz", self.config.target_extensions)
        self.assertEqual(len(self.config.target_extensions), original_count + 1)
        
        # 移除檔案類型
        self.config.remove_target_extension("xyz")
        self.assertNotIn(".xyz", self.config.target_extensions)
        self.assertEqual(len(self.config.target_extensions), original_count)
    
    def test_validate_config(self):
        """測試配置驗證"""
        errors = self.config.validate_config()
        self.assertEqual(len(errors), 0)  # 預設配置應該是有效的
        
        # 測試無效配置
        self.config.set_config("max_file_size", -1)
        errors = self.config.validate_config()
        self.assertGreater(len(errors), 0)
    
    def test_save_load_config(self):
        """測試儲存和載入配置"""
        config_file = self.temp_dir / "test_config.json"
        
        # 修改配置
        self.config.add_target_extension("test")
        self.config.set_config("max_file_size", 1024)
        
        # 儲存配置
        result = self.config.save_config(str(config_file))
        self.assertTrue(result)
        self.assertTrue(config_file.exists())
        
        # 載入配置
        new_config = Config()
        result = new_config.load_config(str(config_file))
        self.assertTrue(result)
        
        # 檢查配置是否正確載入
        self.assertIn(".test", new_config.target_extensions)
        self.assertEqual(new_config.max_file_size, 1024)


class TestCodeBridgeIntegration(unittest.TestCase):
    """測試 CodeBridge 整合功能"""
    
    def setUp(self):
        """設置測試環境"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.codebridge = CodeBridge()
    
    def tearDown(self):
        """清理測試環境"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_convert_project_preview(self):
        """測試專案轉換預覽模式"""
        # 創建測試專案結構
        (self.temp_dir / "src").mkdir()
        test_files = [
            ("src/main.py", "# 主程序\nprint('数据处理完成')"),
            ("src/utils.js", "// 工具函数\nconsole.log('系统初始化');"),
            ("README.md", "# 项目说明\n这是一个测试项目。")
        ]
        
        for file_path, content in test_files:
            full_path = self.temp_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        # 執行預覽轉換
        result = self.codebridge.convert_project(str(self.temp_dir), preview_mode=True)
        
        # 檢查結果
        self.assertGreater(result.total_files, 0)
        self.assertGreaterEqual(result.processed_files, 0)
        self.assertEqual(len(result.errors), 0)
        
        # 檢查檔案未被修改
        for file_path, original_content in test_files:
            full_path = self.temp_dir / file_path
            with open(full_path, 'r', encoding='utf-8') as f:
                current_content = f.read()
            self.assertEqual(current_content, original_content)
    
    def test_convert_project_actual(self):
        """測試專案實際轉換"""
        # 創建測試檔案
        test_file = self.temp_dir / "test.py"
        original_content = "# 这是一个Python程序\nprint('数据库连接成功')"
        
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(original_content)
        
        # 執行實際轉換
        result = self.codebridge.convert_project(str(self.temp_dir), preview_mode=False)
        
        # 檢查結果
        self.assertGreater(result.total_files, 0)
        self.assertGreater(result.processed_files, 0)
        self.assertGreater(result.total_conversions, 0)
        
        # 檢查檔案已被修改
        with open(test_file, 'r', encoding='utf-8') as f:
            converted_content = f.read()
        
        self.assertNotEqual(converted_content, original_content)
        self.assertIn("這是一個", converted_content)
        self.assertIn("數據庫", converted_content)
    
    def test_custom_mappings(self):
        """測試自定義映射"""
        # 創建自定義映射檔案
        custom_file = self.temp_dir / "custom.txt"
        with open(custom_file, 'w', encoding='utf-8') as f:
            f.write("自定义词:自定義詞\n测试词汇:測試詞彙\n")
        
        # 載入自定義映射
        count = self.codebridge.load_custom_mappings(str(custom_file))
        self.assertEqual(count, 2)
        
        # 測試自定義映射是否生效
        test_file = self.temp_dir / "test.txt"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("这是一个自定义词和测试词汇")
        
        result = self.codebridge.convert_project(str(self.temp_dir), preview_mode=False)
        
        with open(test_file, 'r', encoding='utf-8') as f:
            converted_content = f.read()
        
        self.assertIn("自定義詞", converted_content)
        self.assertIn("測試詞彙", converted_content)


def run_tests():
    """執行所有測試"""
    # 創建測試套件
    test_suite = unittest.TestSuite()
    
    # 添加測試類別
    test_classes = [
        TestChineseConverter,
        TestMappingManager,
        TestFileProcessor,
        TestConfig,
        TestCodeBridgeIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # 執行測試
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
