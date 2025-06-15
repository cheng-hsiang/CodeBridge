#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CodeBridge 基本使用範例
"""

import sys
from pathlib import Path

# 添加 src 目錄到 Python 路徑
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from src.codebridge import CodeBridge
from src.config import Config


def basic_usage_example():
    """基本使用範例"""
    print("=== CodeBridge 基本使用範例 ===\n")
    
    # 1. 初始化 CodeBridge
    print("1. 初始化 CodeBridge...")
    codebridge = CodeBridge()
    
    # 2. 設定要轉換的專案路徑（這裡使用當前目錄作為範例）
    project_path = "."
    print(f"2. 設定專案路徑: {project_path}")
    
    # 3. 預覽模式 - 查看會被轉換的內容
    print("\n3. 執行預覽模式...")
    preview_result = codebridge.convert_project(project_path, preview_mode=True)
    
    print(f"   掃描檔案總數: {preview_result.total_files}")
    print(f"   包含簡體字的檔案: {preview_result.processed_files}")
    print(f"   預計轉換字符數: {preview_result.total_conversions}")
    
    if preview_result.file_details:
        print("\n   需要轉換的檔案:")
        for filename, count in preview_result.file_details[:5]:
            print(f"     • {filename}: {count} 個字符")
    
    # 4. 詢問用戶是否要執行實際轉換
    if preview_result.processed_files > 0:
        print(f"\n4. 確認轉換...")
        answer = input("   是否要執行實際轉換？(y/N): ").strip().lower()
        
        if answer == 'y':
            print("   執行實際轉換...")
            actual_result = codebridge.convert_project(project_path, preview_mode=False)
            
            print(f"   實際處理檔案數量: {actual_result.processed_files}")
            print(f"   實際轉換字符總數: {actual_result.total_conversions}")
            print("   ✅ 轉換完成！")
        else:
            print("   取消轉換操作。")
    else:
        print("   沒有發現需要轉換的簡體中文。")


def custom_mapping_example():
    """自定義映射範例"""
    print("\n=== 自定義映射範例 ===\n")
    
    # 1. 初始化 CodeBridge
    codebridge = CodeBridge()
    
    # 2. 載入自定義映射
    custom_file = Path(__file__).parent.parent / "data" / "custom_mappings_example.txt"
    if custom_file.exists():
        print(f"2. 載入自定義映射: {custom_file}")
        count = codebridge.load_custom_mappings(str(custom_file))
        print(f"   成功載入 {count} 個自定義映射")
    else:
        print("2. 創建臨時自定義映射...")
        # 動態添加一些自定義映射
        codebridge.mapping_manager.add_custom_mapping("我们的项目", "我們的專案")
        codebridge.mapping_manager.add_custom_mapping("内部接口", "內部介面")
        print("   添加了 2 個自定義映射")
    
    # 3. 測試自定義映射
    test_text = "这是我们的项目，包含内部接口的数据处理功能。"
    converted, count = codebridge.converter.convert_text(test_text)
    
    print(f"\n3. 測試自定義映射:")
    print(f"   原文: {test_text}")
    print(f"   轉換: {converted}")
    print(f"   轉換次數: {count}")


def config_example():
    """配置檔案範例"""
    print("\n=== 配置檔案範例 ===\n")
    
    # 1. 創建自定義配置
    print("1. 創建自定義配置...")
    config = Config()
    
    # 2. 修改配置
    print("2. 修改配置選項...")
    config.add_target_extension("log")  # 添加 .log 檔案
    config.set_config("create_backup", True)  # 啟用備份
    config.set_config("max_file_size", 5 * 1024 * 1024)  # 5MB 限制
    
    print(f"   目標檔案類型數量: {len(config.target_extensions)}")
    print(f"   創建備份: {config.create_backup}")
    print(f"   最大檔案大小: {config.max_file_size / (1024*1024):.1f}MB")
    
    # 3. 使用自定義配置初始化 CodeBridge
    print("\n3. 使用自定義配置...")
    codebridge = CodeBridge()
    codebridge.config = config  # 替換配置
    
    print("   配置已套用到 CodeBridge")


def file_type_example():
    """特定檔案類型處理範例"""
    print("\n=== 特定檔案類型處理範例 ===\n")
    
    # 1. 只處理特定檔案類型
    print("1. 只處理 Python 和 JavaScript 檔案...")
    codebridge = CodeBridge()
    
    # 設定只處理特定檔案類型
    target_extensions = {'.py', '.js', '.jsx', '.ts', '.tsx'}
    
    project_path = "."
    result = codebridge.convert_project(
        project_path, 
        preview_mode=True, 
        file_extensions=target_extensions
    )
    
    print(f"   掃描檔案總數: {result.total_files}")
    print(f"   處理檔案數量: {result.processed_files}")
    
    if result.file_details:
        print("\n   處理的檔案:")
        for filename, count in result.file_details:
            print(f"     • {filename}: {count} 個字符")


def generate_report_example():
    """生成報告範例"""
    print("\n=== 生成報告範例 ===\n")
    
    # 1. 執行轉換並生成報告
    print("1. 執行轉換...")
    codebridge = CodeBridge()
    
    project_path = "."
    result = codebridge.convert_project(project_path, preview_mode=True)
    
    # 2. 生成詳細報告
    print("2. 生成詳細報告...")
    report = codebridge.generate_report(result, preview_mode=True)
    
    print("\n" + "="*50)
    print(report)
    print("="*50)


def main():
    """主函數"""
    print("🌉 CodeBridge 使用範例")
    print("=" * 50)
    
    try:
        # 執行各種範例
        basic_usage_example()
        custom_mapping_example()
        config_example()
        file_type_example()
        generate_report_example()
        
        print("\n🎉 所有範例執行完成！")
        print("\n💡 提示:")
        print("   - 使用 --preview 參數可以安全地預覽轉換結果")
        print("   - 使用 --custom 參數可以載入自定義映射檔案")
        print("   - 使用 --extensions 參數可以指定要處理的檔案類型")
        print("   - 查看 README.md 了解更多使用方法")
        
    except Exception as e:
        print(f"❌ 執行範例時發生錯誤: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
