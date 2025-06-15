#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CodeBridge 進階使用範例
"""

import sys
import json
import tempfile
import shutil
from pathlib import Path

# 添加 src 目錄到 Python 路徑
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from src.codebridge import CodeBridge
from src.config import Config
from src.statistics import StatisticsCollector


def batch_processing_example():
    """批量處理範例"""
    print("=== 批量處理範例 ===\n")
    
    # 創建臨時專案結構用於演示
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # 創建測試專案結構
        print("1. 創建測試專案結構...")
        project_structure = {
            "src": {
                "main.py": "# 主程序文件\ndef main():\n    print('数据处理完成')",
                "utils.py": "# 工具函数\ndef process_data(data):\n    return data",
                "config.py": "# 配置文件\nDATABASE_URL = 'mysql://localhost/数据库'"
            },
            "tests": {
                "test_main.py": "# 测试文件\nimport unittest\nclass TestMain(unittest.TestCase):\n    def test_process(self):\n        pass"
            },
            "docs": {
                "README.md": "# 项目说明\n这是一个测试项目，用于演示简体转繁体功能。",
                "API.md": "# API文档\n数据接口说明"
            },
            "frontend": {
                "src": {
                    "app.js": "// 前端应用\nconsole.log('系统初始化完成');",
                    "utils.js": "// 工具函数\nfunction formatData(data) { return data; }"
                }
            }
        }
        
        def create_files(base_path, structure):
            for name, content in structure.items():
                path = base_path / name
                if isinstance(content, dict):
                    path.mkdir(exist_ok=True)
                    create_files(path, content)
                else:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(content)
        
        create_files(temp_path, project_structure)
        
        # 2. 初始化 CodeBridge
        print("2. 初始化 CodeBridge...")
        codebridge = CodeBridge()
        
        # 3. 預覽整個專案
        print("3. 預覽專案轉換...")
        preview_result = codebridge.convert_project(str(temp_path), preview_mode=True)
        
        print(f"   掃描檔案總數: {preview_result.total_files}")
        print(f"   包含簡體字的檔案: {preview_result.processed_files}")
        print(f"   預計轉換字符數: {preview_result.total_conversions}")
        
        # 4. 按檔案類型分別處理
        print("\n4. 按檔案類型分別處理...")
        
        file_type_groups = [
            ("Python 檔案", {'.py'}),
            ("JavaScript 檔案", {'.js'}),
            ("Markdown 檔案", {'.md'})
        ]
        
        for group_name, extensions in file_type_groups:
            print(f"\n   處理 {group_name}:")
            result = codebridge.convert_project(
                str(temp_path), 
                preview_mode=True, 
                file_extensions=extensions
            )
            print(f"     檔案數量: {result.processed_files}")
            print(f"     轉換字符: {result.total_conversions}")
        
        # 5. 生成詳細報告
        print("\n5. 生成詳細報告...")
        report = codebridge.generate_report(preview_result, preview_mode=True)
        
        # 儲存報告到檔案
        report_file = temp_path / "conversion_report.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"   報告已儲存到: {report_file}")


def statistics_example():
    """統計功能範例"""
    print("\n=== 統計功能範例 ===\n")
    
    # 1. 初始化統計收集器
    print("1. 初始化統計收集器...")
    stats_collector = StatisticsCollector()
    
    # 2. 開始統計會話
    print("2. 開始統計會話...")
    session_id = stats_collector.start_session(
        project_path="./test_project",
        preview_mode=True,
        file_extensions=['.py', '.js', '.md']
    )
    print(f"   會話 ID: {session_id}")
    
    # 3. 模擬處理過程
    print("3. 模擬處理過程...")
    
    # 模擬轉換結果
    class MockResult:
        def __init__(self):
            self.total_files = 25
            self.processed_files = 12
            self.total_conversions = 156
            self.errors = []
    
    mock_result = MockResult()
    stats_collector.update(mock_result)
    
    # 4. 結束會話並獲取統計
    print("4. 結束會話...")
    session_stats = stats_collector.end_session()
    
    if session_stats:
        print(f"   執行時長: {session_stats.duration:.2f} 秒")
        print(f"   成功率: {session_stats.success_rate:.1f}%")
        print(f"   轉換效率: {session_stats.total_conversions/session_stats.duration:.1f} 字符/秒")
    
    # 5. 獲取總體統計
    print("\n5. 總體使用統計:")
    overall_summary = stats_collector.get_overall_summary()
    for key, value in overall_summary.items():
        if key != 'top_file_types':
            print(f"   {key}: {value}")


def advanced_config_example():
    """進階配置範例"""
    print("\n=== 進階配置範例 ===\n")
    
    # 1. 創建進階配置
    print("1. 創建進階配置...")
    
    advanced_config = {
        "target_extensions": [".py", ".js", ".ts", ".vue", ".md"],
        "exclude_dirs": ["node_modules", "venv", "__pycache__", ".git"],
        "max_file_size": 5242880,  # 5MB
        "create_backup": True,
        "log_level": "DEBUG",
        "output_format": "json",
        "encoding_detection": True,
        "parallel_processing": False,
        "max_workers": 2
    }
    
    # 2. 儲存配置到檔案
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(advanced_config, f, ensure_ascii=False, indent=2)
        config_file = f.name
    
    print(f"2. 配置檔案: {config_file}")
    
    try:
        # 3. 載入配置
        print("3. 載入進階配置...")
        config = Config(config_file)
        
        # 4. 驗證配置
        print("4. 驗證配置...")
        errors = config.validate_config()
        if errors:
            print("   配置錯誤:")
            for error in errors:
                print(f"     - {error}")
        else:
            print("   ✅ 配置有效")
        
        # 5. 顯示配置摘要
        print("\n5. 配置摘要:")
        summary = config.get_summary()
        for key, value in summary.items():
            print(f"   {key}: {value}")
        
        # 6. 使用配置創建 CodeBridge
        print("\n6. 使用進階配置...")
        codebridge = CodeBridge(config_file)
        print("   ✅ CodeBridge 已使用進階配置初始化")
        
    finally:
        # 清理臨時檔案
        Path(config_file).unlink(missing_ok=True)


def custom_converter_example():
    """自定義轉換器範例"""
    print("\n=== 自定義轉換器範例 ===\n")
    
    # 1. 創建 CodeBridge 實例
    print("1. 創建 CodeBridge 實例...")
    codebridge = CodeBridge()
    
    # 2. 添加專案特定的映射
    print("2. 添加專案特定映射...")
    
    project_mappings = [
        ("我们的系统", "我們的系統"),
        ("内部模块", "內部模組"),
        ("业务逻辑", "業務邏輯"),
        ("数据模型", "資料模型"),
        ("接口设计", "介面設計"),
        ("性能测试", "效能測試"),
        ("错误处理", "錯誤處理"),
        ("日志记录", "日誌記錄")
    ]
    
    for simplified, traditional in project_mappings:
        codebridge.mapping_manager.add_custom_mapping(simplified, traditional)
    
    print(f"   添加了 {len(project_mappings)} 個專案特定映射")
    
    # 3. 測試自定義轉換
    print("\n3. 測試自定義轉換...")
    
    test_cases = [
        "我们的系统采用微服务架构设计",
        "内部模块通过接口设计进行通信",
        "业务逻辑层负责数据模型的处理",
        "性能测试显示系统运行稳定，错误处理机制完善，日志记录详细"
    ]
    
    for i, test_text in enumerate(test_cases, 1):
        converted, count = codebridge.converter.convert_text(test_text)
        print(f"   測試 {i}:")
        print(f"     原文: {test_text}")
        print(f"     轉換: {converted}")
        print(f"     轉換次數: {count}")
        print()
    
    # 4. 匯出自定義映射
    print("4. 匯出自定義映射...")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        for simplified, traditional in project_mappings:
            f.write(f"{simplified}:{traditional}\n")
        export_file = f.name
    
    print(f"   自定義映射已匯出到: {export_file}")
    
    # 清理
    Path(export_file).unlink(missing_ok=True)


def performance_analysis_example():
    """效能分析範例"""
    print("\n=== 效能分析範例 ===\n")
    
    import time
    
    # 1. 準備測試資料
    print("1. 準備測試資料...")
    
    test_texts = [
        "这是一个简单的测试文本，包含一些基本的中文字符。",
        "人工智能和机器学习技术在现代软件开发中越来越重要。",
        "我们的系统采用微服务架构，通过API接口进行数据交换。",
        "数据库优化、缓存策略、负载均衡是提高系统性能的关键技术。",
        "前端开发使用现代框架，后端采用云原生架构设计。" * 10  # 重複10次
    ]
    
    # 2. 初始化轉換器
    print("2. 初始化轉換器...")
    codebridge = CodeBridge()
    
    # 3. 效能測試
    print("3. 執行效能測試...")
    
    results = []
    for i, text in enumerate(test_texts, 1):
        start_time = time.time()
        converted, count = codebridge.converter.convert_text(text)
        end_time = time.time()
        
        duration = end_time - start_time
        chars_per_second = len(text) / duration if duration > 0 else 0
        
        results.append({
            'test': i,
            'input_length': len(text),
            'conversions': count,
            'duration': duration,
            'chars_per_second': chars_per_second
        })
        
        print(f"   測試 {i}: {len(text)} 字符, {count} 次轉換, {duration:.4f} 秒, {chars_per_second:.1f} 字符/秒")
    
    # 4. 分析結果
    print("\n4. 效能分析:")
    
    total_chars = sum(r['input_length'] for r in results)
    total_conversions = sum(r['conversions'] for r in results)
    total_duration = sum(r['duration'] for r in results)
    avg_chars_per_second = total_chars / total_duration if total_duration > 0 else 0
    
    print(f"   總字符數: {total_chars:,}")
    print(f"   總轉換次數: {total_conversions}")
    print(f"   總耗時: {total_duration:.4f} 秒")
    print(f"   平均處理速度: {avg_chars_per_second:.1f} 字符/秒")
    print(f"   平均轉換率: {(total_conversions/total_chars*100):.2f}%")


def main():
    """主函數"""
    print("🚀 CodeBridge 進階使用範例")
    print("=" * 60)
    
    try:
        # 執行各種進階範例
        batch_processing_example()
        statistics_example()
        advanced_config_example()
        custom_converter_example()
        performance_analysis_example()
        
        print("\n" + "=" * 60)
        print("🎉 所有進階範例執行完成！")
        print("\n📚 更多功能:")
        print("   - 批量處理多個專案")
        print("   - 自定義映射管理")
        print("   - 詳細統計報告")
        print("   - 效能監控與分析")
        print("   - 進階配置選項")
        print("\n💡 提示: 查看 docs/ 目錄了解更多進階用法")
        
    except Exception as e:
        print(f"❌ 執行進階範例時發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
