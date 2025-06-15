#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CodeBridge - 統計收集器
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import logging


@dataclass
class SessionStats:
    """單次執行統計"""
    session_id: str
    start_time: float
    end_time: Optional[float] = None
    total_files: int = 0
    processed_files: int = 0
    total_conversions: int = 0
    errors_count: int = 0
    preview_mode: bool = False
    project_path: str = ""
    file_extensions: List[str] = None
    
    def __post_init__(self):
        if self.file_extensions is None:
            self.file_extensions = []
    
    @property
    def duration(self) -> float:
        """執行時長（秒）"""
        if self.end_time:
            return self.end_time - self.start_time
        return time.time() - self.start_time
    
    @property
    def success_rate(self) -> float:
        """成功率（百分比）"""
        if self.total_files == 0:
            return 0.0
        return (self.processed_files / self.total_files) * 100


@dataclass
class OverallStats:
    """總體統計"""
    total_sessions: int = 0
    total_files_processed: int = 0
    total_conversions: int = 0
    total_errors: int = 0
    total_duration: float = 0.0
    first_run: Optional[str] = None
    last_run: Optional[str] = None
    most_converted_file_types: Dict[str, int] = None
    
    def __post_init__(self):
        if self.most_converted_file_types is None:
            self.most_converted_file_types = {}


class StatisticsCollector:
    """
    統計收集器
    
    收集和管理 CodeBridge 的使用統計
    """
    
    def __init__(self, stats_file: Optional[str] = None):
        """
        初始化統計收集器
        
        Args:
            stats_file: 統計檔案路徑
        """
        self.logger = logging.getLogger('CodeBridge.Statistics')
        self.stats_file = Path(stats_file) if stats_file else Path.home() / '.codebridge' / 'stats.json'
        self.current_session: Optional[SessionStats] = None
        self.overall_stats = self._load_overall_stats()
        
        # 確保統計目錄存在
        self.stats_file.parent.mkdir(parents=True, exist_ok=True)
    
    def start_session(self, project_path: str, preview_mode: bool = False, file_extensions: List[str] = None) -> str:
        """
        開始新的統計會話
        
        Args:
            project_path: 專案路徑
            preview_mode: 是否為預覽模式
            file_extensions: 處理的檔案類型
        
        Returns:
            str: 會話ID
        """
        session_id = f"session_{int(time.time())}_{id(self)}"
        
        self.current_session = SessionStats(
            session_id=session_id,
            start_time=time.time(),
            project_path=project_path,
            preview_mode=preview_mode,
            file_extensions=file_extensions or []
        )
        
        self.logger.info(f"開始統計會話: {session_id}")
        return session_id
    
    def end_session(self) -> Optional[SessionStats]:
        """
        結束當前統計會話
        
        Returns:
            Optional[SessionStats]: 會話統計，如果沒有活動會話則返回None
        """
        if not self.current_session:
            return None
        
        self.current_session.end_time = time.time()
        
        # 更新總體統計
        self._update_overall_stats(self.current_session)
        
        # 儲存統計
        self._save_stats()
        
        session = self.current_session
        self.current_session = None
        
        self.logger.info(f"結束統計會話: {session.session_id}, 耗時: {session.duration:.2f}秒")
        return session
    
    def update(self, conversion_result) -> None:
        """
        更新當前會話統計
        
        Args:
            conversion_result: 轉換結果對象
        """
        if not self.current_session:
            return
        
        self.current_session.total_files = conversion_result.total_files
        self.current_session.processed_files = conversion_result.processed_files
        self.current_session.total_conversions = conversion_result.total_conversions
        self.current_session.errors_count = len(conversion_result.errors)
        
        self.logger.debug(f"更新會話統計: {self.current_session.processed_files}/{self.current_session.total_files} 檔案")
    
    def add_file_conversion(self, file_extension: str, conversions: int) -> None:
        """
        添加檔案轉換統計
        
        Args:
            file_extension: 檔案擴展名
            conversions: 轉換次數
        """
        if not self.current_session:
            return
        
        # 更新當前會話
        self.current_session.total_conversions += conversions
        self.current_session.processed_files += 1
        
        # 更新檔案類型統計
        if file_extension not in self.overall_stats.most_converted_file_types:
            self.overall_stats.most_converted_file_types[file_extension] = 0
        self.overall_stats.most_converted_file_types[file_extension] += conversions
    
    def record_file_rename(self, old_name: str, new_name: str) -> None:
        """
        記錄檔名轉換
        
        Args:
            old_name: 原檔名
            new_name: 新檔名
        """
        if not hasattr(self, 'renamed_files'):
            self.renamed_files = {}
        
        self.renamed_files[old_name] = new_name
        self.logger.info(f"記錄檔名轉換: {old_name} → {new_name}")
    
    def get_current_session_stats(self) -> Optional[SessionStats]:
        """獲取當前會話統計"""
        return self.current_session
    
    def get_overall_stats(self) -> OverallStats:
        """獲取總體統計"""
        return self.overall_stats
    
    def get_session_summary(self, session: SessionStats) -> Dict[str, Any]:
        """
        獲取會話摘要
        
        Args:
            session: 會話統計
        
        Returns:
            Dict[str, Any]: 會話摘要
        """
        return {
            'session_id': session.session_id,
            'duration': f"{session.duration:.2f}秒",
            'mode': '預覽模式' if session.preview_mode else '轉換模式',
            'total_files': session.total_files,
            'processed_files': session.processed_files,
            'total_conversions': session.total_conversions,
            'errors_count': session.errors_count,
            'success_rate': f"{session.success_rate:.1f}%",
            'avg_conversions_per_file': (
                session.total_conversions / session.processed_files 
                if session.processed_files > 0 else 0
            ),
            'project_path': session.project_path,
            'file_extensions': session.file_extensions
        }
    
    def get_overall_summary(self) -> Dict[str, Any]:
        """
        獲取總體摘要
        
        Returns:
            Dict[str, Any]: 總體摘要
        """
        # 計算平均值
        avg_files_per_session = (
            self.overall_stats.total_files_processed / self.overall_stats.total_sessions
            if self.overall_stats.total_sessions > 0 else 0
        )
        
        avg_conversions_per_session = (
            self.overall_stats.total_conversions / self.overall_stats.total_sessions
            if self.overall_stats.total_sessions > 0 else 0
        )
        
        avg_duration_per_session = (
            self.overall_stats.total_duration / self.overall_stats.total_sessions
            if self.overall_stats.total_sessions > 0 else 0
        )
        
        # 找出最常轉換的檔案類型
        top_file_types = sorted(
            self.overall_stats.most_converted_file_types.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        return {
            'total_sessions': self.overall_stats.total_sessions,
            'total_files_processed': self.overall_stats.total_files_processed,
            'total_conversions': self.overall_stats.total_conversions,
            'total_errors': self.overall_stats.total_errors,
            'total_duration': f"{self.overall_stats.total_duration:.2f}秒",
            'avg_files_per_session': f"{avg_files_per_session:.1f}",
            'avg_conversions_per_session': f"{avg_conversions_per_session:.1f}",
            'avg_duration_per_session': f"{avg_duration_per_session:.1f}秒",
            'first_run': self.overall_stats.first_run,
            'last_run': self.overall_stats.last_run,
            'top_file_types': top_file_types,
            'error_rate': (
                f"{(self.overall_stats.total_errors / self.overall_stats.total_files_processed * 100):.2f}%"
                if self.overall_stats.total_files_processed > 0 else "0%"
            )
        }
    
    def export_stats(self, output_path: str, format_type: str = 'json') -> bool:
        """
        匯出統計資料
        
        Args:
            output_path: 輸出路徑
            format_type: 格式類型 ('json', 'csv', 'markdown')
        
        Returns:
            bool: 是否匯出成功
        """
        try:
            if format_type == 'json':
                return self._export_json(output_path)
            elif format_type == 'csv':
                return self._export_csv(output_path)
            elif format_type == 'markdown':
                return self._export_markdown(output_path)
            else:
                self.logger.error(f"不支持的匯出格式: {format_type}")
                return False
        except Exception as e:
            self.logger.error(f"匯出統計失敗: {e}")
            return False
    
    def _export_json(self, output_path: str) -> bool:
        """匯出為JSON格式"""
        data = {
            'overall_stats': asdict(self.overall_stats),
            'current_session': asdict(self.current_session) if self.current_session else None,
            'export_time': datetime.now().isoformat()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    
    def _export_csv(self, output_path: str) -> bool:
        """匯出為CSV格式"""
        import csv
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # 寫入標題
            writer.writerow(['指標', '數值'])
            
            # 寫入總體統計
            overall = self.get_overall_summary()
            for key, value in overall.items():
                if key != 'top_file_types':
                    writer.writerow([key, value])
            
            # 寫入檔案類型統計
            writer.writerow(['', ''])  # 空行
            writer.writerow(['檔案類型', '轉換次數'])
            for file_type, count in overall['top_file_types']:
                writer.writerow([file_type, count])
        
        return True
    
    def _export_markdown(self, output_path: str) -> bool:
        """匯出為Markdown格式"""
        overall = self.get_overall_summary()
        
        content = [
            "# CodeBridge 使用統計報告",
            "",
            f"**報告生成時間**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## 總體統計",
            "",
            f"- **總執行次數**: {overall['total_sessions']}",
            f"- **總處理檔案數**: {overall['total_files_processed']}",
            f"- **總轉換次數**: {overall['total_conversions']}",
            f"- **總錯誤數**: {overall['total_errors']}",
            f"- **總執行時間**: {overall['total_duration']}",
            f"- **首次使用**: {overall['first_run'] or 'N/A'}",
            f"- **最後使用**: {overall['last_run'] or 'N/A'}",
            "",
            "## 平均統計",
            "",
            f"- **平均每次處理檔案數**: {overall['avg_files_per_session']}",
            f"- **平均每次轉換次數**: {overall['avg_conversions_per_session']}",
            f"- **平均執行時間**: {overall['avg_duration_per_session']}",
            f"- **錯誤率**: {overall['error_rate']}",
            "",
            "## 熱門檔案類型",
            "",
            "| 檔案類型 | 轉換次數 |",
            "|---------|---------|"
        ]
        
        for file_type, count in overall['top_file_types']:
            content.append(f"| {file_type} | {count} |")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        
        return True
    
    def _load_overall_stats(self) -> OverallStats:
        """載入總體統計"""
        if not self.stats_file.exists():
            return OverallStats()
        
        try:
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return OverallStats(**data)
        except Exception as e:
            self.logger.warning(f"載入統計檔案失敗: {e}")
            return OverallStats()
    
    def _update_overall_stats(self, session: SessionStats) -> None:
        """更新總體統計"""
        now = datetime.now().isoformat()
        
        self.overall_stats.total_sessions += 1
        self.overall_stats.total_files_processed += session.processed_files
        self.overall_stats.total_conversions += session.total_conversions
        self.overall_stats.total_errors += session.errors_count
        self.overall_stats.total_duration += session.duration
        
        if not self.overall_stats.first_run:
            self.overall_stats.first_run = now
        self.overall_stats.last_run = now
    
    def _save_stats(self) -> None:
        """儲存統計到檔案"""
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(self.overall_stats), f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"儲存統計失敗: {e}")
    
    def reset_stats(self) -> bool:
        """
        重置所有統計
        
        Returns:
            bool: 是否重置成功
        """
        try:
            self.overall_stats = OverallStats()
            self.current_session = None
            
            if self.stats_file.exists():
                self.stats_file.unlink()
            
            self.logger.info("統計資料已重置")
            return True
        except Exception as e:
            self.logger.error(f"重置統計失敗: {e}")
            return False
