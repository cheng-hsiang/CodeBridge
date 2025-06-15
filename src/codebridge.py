#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CodeBridge - 主要轉換工具類
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
import json
import logging

from .converter import ChineseConverter
from .mappings import MappingManager
from .file_processor import FileProcessor
from .config import Config
from .statistics import StatisticsCollector


@dataclass
class ConversionResult:
    """轉換結果數據類"""
    total_files: int = 0
    processed_files: int = 0
    total_conversions: int = 0
    errors: List[str] = None
    file_details: List[Tuple[str, int]] = None
    preview_results: List[Tuple[str, str, int]] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
        if self.file_details is None:
            self.file_details = []
        if self.preview_results is None:
            self.preview_results = []


class CodeBridge:
    """
    CodeBridge 主要轉換工具類
    
    功能：
    - 批量轉換專案中的簡體中文為繁體中文
    - 支援預覽模式
    - 自定義映射管理
    - 智慧檔案類型識別
    - 詳細統計報告
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """初始化 CodeBridge"""
        self.config = Config(config_path)
        self.mapping_manager = MappingManager()
        self.converter = ChineseConverter(self.mapping_manager)
        self.file_processor = FileProcessor(self.config)
        self.stats = StatisticsCollector()
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """設置日誌"""
        logger = logging.getLogger('CodeBridge')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def load_custom_mappings(self, custom_file_path: str) -> int:
        """載入自定義映射檔案"""
        return self.mapping_manager.load_custom_mappings(custom_file_path)
    
    def convert_project(
        self, 
        project_path: str, 
        preview_mode: bool = False,
        file_extensions: Optional[Set[str]] = None
    ) -> ConversionResult:
        """
        轉換整個專案
        
        Args:
            project_path: 專案路徑
            preview_mode: 預覽模式，不實際修改檔案
            file_extensions: 要處理的檔案類型
        
        Returns:
            ConversionResult: 轉換結果
        """
        project_path = Path(project_path)
        if not project_path.exists():
            raise FileNotFoundError(f"專案路徑不存在: {project_path}")
        
        # 使用指定的檔案類型或默認類型
        target_extensions = file_extensions or self.config.target_extensions
        
        self.logger.info(f"開始處理專案: {project_path}")
        self.logger.info(f"模式: {'預覽' if preview_mode else '轉換'}")
        self.logger.info(f"檔案類型: {', '.join(sorted(target_extensions))}")
        
        result = ConversionResult()
        
        # 遍歷所有檔案
        for file_path in project_path.rglob('*'):
            if not self._should_process_file(file_path, target_extensions):
                continue
            
            result.total_files += 1
            
            try:
                file_result = self.file_processor.process_file(
                    file_path, self.converter, preview_mode
                )
                
                if file_result.conversions > 0:
                    result.processed_files += 1
                    result.total_conversions += file_result.conversions
                    result.file_details.append((file_path.name, file_result.conversions))
                
                if file_result.preview_data:
                    result.preview_results.extend(file_result.preview_data)
                
            except Exception as e:
                error_msg = f"{file_path}: {str(e)}"
                result.errors.append(error_msg)
                self.logger.error(error_msg)
        
        # 更新統計
        self.stats.update(result)
        
        return result
    
    def _should_process_file(self, file_path: Path, target_extensions: Set[str]) -> bool:
        """判斷是否應該處理該檔案"""
        if not file_path.is_file():
            return False
        
        # 檢查是否在排除目錄中
        if any(part in self.config.exclude_dirs for part in file_path.parts):
            return False
        
        # 檢查檔案類型
        return (file_path.suffix.lower() in target_extensions or 
                file_path.name in target_extensions)
    
    def generate_report(self, result: ConversionResult, preview_mode: bool = False) -> str:
        """生成詳細報告"""
        report_lines = []
        
        # 標題
        mode_text = "預覽模式" if preview_mode else "轉換模式"
        report_lines.append("🌉 CodeBridge - 程式碼簡繁轉換工具")
        report_lines.append("=" * 70)
        report_lines.append(f"執行模式: {mode_text}")
        report_lines.append(f"字庫規模: {len(self.mapping_manager.get_all_mappings()):,} 個映射")
        
        # 字庫分類統計
        categories = self.mapping_manager.get_category_stats()
        report_lines.append("\n📊 字庫分類統計:")
        for category, count in categories.items():
            report_lines.append(f"  • {category}: {count:,} 個")
        
        # 處理結果
        report_lines.append("\n" + "=" * 70)
        report_lines.append("📊 處理結果:")
        report_lines.append(f"掃描檔案總數: {result.total_files:,}")
        
        if preview_mode:
            report_lines.append(f"包含簡體字的檔案: {result.processed_files:,}")
            report_lines.append(f"預計轉換字符數: {result.total_conversions:,}")
        else:
            report_lines.append(f"實際處理檔案數量: {result.processed_files:,}")
            report_lines.append(f"實際轉換字符總數: {result.total_conversions:,}")
        
        # 檔案詳情
        if result.file_details:
            action_text = "需要轉換" if preview_mode else "已轉換"
            report_lines.append(f"\n🔄 {action_text}詳情 (前10個檔案):")
            sorted_details = sorted(result.file_details, key=lambda x: x[1], reverse=True)
            for filename, count in sorted_details[:10]:
                report_lines.append(f"  • {filename}: {count:,} 個字符")
        
        # 錯誤資訊
        if result.errors:
            report_lines.append(f"\n❌ 錯誤數量: {len(result.errors)}")
            for error in result.errors[:5]:
                report_lines.append(f"  - {error}")
            if len(result.errors) > 5:
                report_lines.append(f"  ... 還有 {len(result.errors) - 5} 個錯誤")
        else:
            report_lines.append("\n✅ 沒有錯誤")
        
        # 結尾
        report_lines.append("=" * 70)
        if result.processed_files > 0:
            avg_conversions = result.total_conversions / result.processed_files
            if preview_mode:
                report_lines.append("🔍 預覽完成！")
                report_lines.append(f"📈 平均每個檔案需轉換: {avg_conversions:.1f} 個字符")
                report_lines.append("💡 執行時請移除 --preview 參數以實際執行轉換")
            else:
                report_lines.append("🎉 轉換完成！")
                report_lines.append(f"📈 平均每個檔案轉換: {avg_conversions:.1f} 個字符")
                report_lines.append("💡 建議：定期執行此腳本以保持程式碼的繁體中文一致性")
        else:
            report_lines.append("ℹ️  沒有發現需要轉換的簡體中文。")
            report_lines.append("💡 提示：這可能表示您的專案已經使用了繁體中文")
        
        report_lines.append("\n🌉 CodeBridge - Bridging the gap between Simplified and Traditional Chinese in code!")
        
        return "\n".join(report_lines)


def main():
    """命令行入口點"""
    parser = argparse.ArgumentParser(
        description='CodeBridge - 程式碼簡繁轉換工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例:
  %(prog)s --path /path/to/project
  %(prog)s --preview --custom mappings.txt
  %(prog)s --extensions .py,.js,.vue --path ./src
        """
    )
    
    parser.add_argument(
        '--path', '-p', 
        default=".",
        help='專案路徑 (預設: 當前目錄)'
    )
    parser.add_argument(
        '--preview', 
        action='store_true',
        help='預覽模式：只顯示會被轉換的內容，不實際修改檔案'
    )
    parser.add_argument(
        '--custom', '-c',
        help='自定義映射檔案路徑 (格式: 簡體:繁體，每行一個)'
    )
    parser.add_argument(
        '--extensions', '-e',
        help='要處理的檔案類型，用逗號分隔 (例如: .py,.js,.md)'
    )
    parser.add_argument(
        '--config',
        help='配置檔案路徑'
    )
    parser.add_argument(
        '--output', '-o',
        help='輸出報告檔案路徑'
    )
    parser.add_argument(
        '--version', 
        action='version', 
        version='CodeBridge 2.0.0'
    )
    
    args = parser.parse_args()
    
    try:
        # 初始化 CodeBridge
        codebridge = CodeBridge(args.config)
        
        # 載入自定義映射
        if args.custom:
            count = codebridge.load_custom_mappings(args.custom)
            print(f"✅ 載入自定義映射: {count} 個")
        
        # 處理檔案類型
        file_extensions = None
        if args.extensions:
            file_extensions = set(args.extensions.split(','))
        
        # 執行轉換
        result = codebridge.convert_project(
            args.path, 
            args.preview, 
            file_extensions
        )
        
        # 生成並顯示報告
        report = codebridge.generate_report(result, args.preview)
        print(report)
        
        # 輸出報告到檔案
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"\n📄 報告已儲存至: {args.output}")
        
        # 返回適當的退出碼
        return 0 if not result.errors else 1
        
    except Exception as e:
        print(f"❌ 執行錯誤: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
