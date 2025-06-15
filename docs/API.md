# CodeBridge API 參考文件

## 核心類別

### CodeBridge

主要的轉換工具類，提供完整的簡繁轉換功能。

```python
from src.codebridge import CodeBridge

codebridge = CodeBridge(config_path=None)
```

#### 方法

##### `convert_project(project_path, preview_mode=False, file_extensions=None)`

轉換整個專案中的簡體中文為繁體中文。

**參數:**
- `project_path` (str): 專案路徑
- `preview_mode` (bool, 可選): 預覽模式，預設為 False
- `file_extensions` (Set[str], 可選): 要處理的檔案類型

**返回:**
- `ConversionResult`: 轉換結果對象

**範例:**
```python
# 預覽模式
result = codebridge.convert_project("./my-project", preview_mode=True)

# 實際轉換
result = codebridge.convert_project("./my-project")

# 指定檔案類型
result = codebridge.convert_project(
    "./my-project", 
    file_extensions={'.py', '.js', '.md'}
)
```

##### `load_custom_mappings(file_path)`

載入自定義映射檔案。

**參數:**
- `file_path` (str): 自定義映射檔案路徑

**返回:**
- `int`: 載入的映射數量

**範例:**
```python
count = codebridge.load_custom_mappings("custom_terms.txt")
print(f"載入了 {count} 個自定義映射")
```

##### `generate_report(result, preview_mode=False)`

生成詳細的轉換報告。

**參數:**
- `result` (ConversionResult): 轉換結果
- `preview_mode` (bool): 是否為預覽模式

**返回:**
- `str`: 格式化的報告字串

---

### ChineseConverter

中文轉換器核心類別。

```python
from src.converter import ChineseConverter
from src.mappings import MappingManager

mapping_manager = MappingManager()
converter = ChineseConverter(mapping_manager)
```

#### 方法

##### `convert_text(text)`

轉換文本中的簡體中文為繁體中文。

**參數:**
- `text` (str): 要轉換的文本

**返回:**
- `Tuple[str, int]`: (轉換後的文本, 轉換次數)

**範例:**
```python
text = "这是一个测试程序"
converted, count = converter.convert_text(text)
print(f"轉換結果: {converted}")  # 這是一個測試程序
print(f"轉換次數: {count}")      # 4
```

##### `preview_conversion(text)`

預覽轉換結果，不實際修改文本。

**參數:**
- `text` (str): 要分析的文本

**返回:**
- `List[Tuple[str, str, int]]`: [(簡體詞, 繁體詞, 出現次數), ...]

**範例:**
```python
text = "数据库连接错误"
preview = converter.preview_conversion(text)
for simplified, traditional, count in preview:
    print(f"'{simplified}' → '{traditional}' ({count} 次)")
```

##### `get_conversion_statistics(text)`

獲取文本的轉換統計信息。

**參數:**
- `text` (str): 要分析的文本

**返回:**
- `Dict[str, int]`: 統計信息字典

**範例:**
```python
stats = converter.get_conversion_statistics(text)
print(f"總字符數: {stats['total_chars']}")
print(f"中文字符數: {stats['chinese_chars']}")
print(f"可轉換字符數: {stats['convertible_chars']}")
```

---

### MappingManager

映射管理器，管理簡繁轉換映射表。

```python
from src.mappings import MappingManager

mapping_manager = MappingManager()
```

#### 方法

##### `get_all_mappings()`

獲取所有映射（內建 + 自定義）。

**返回:**
- `Dict[str, str]`: 所有映射字典

##### `add_custom_mapping(simplified, traditional)`

添加單個自定義映射。

**參數:**
- `simplified` (str): 簡體詞
- `traditional` (str): 繁體詞

**返回:**
- `bool`: 是否添加成功

**範例:**
```python
success = mapping_manager.add_custom_mapping("我们的API", "我們的API")
```

##### `load_custom_mappings(file_path)`

載入自定義映射檔案。

**參數:**
- `file_path` (str): 檔案路徑

**返回:**
- `int`: 載入的映射數量

##### `search_mappings(keyword)`

搜尋包含關鍵字的映射。

**參數:**
- `keyword` (str): 搜尋關鍵字

**返回:**
- `List[Tuple[str, str]]`: 符合的映射列表

**範例:**
```python
results = mapping_manager.search_mappings("数据")
for simplified, traditional in results:
    print(f"{simplified} → {traditional}")
```

##### `get_category_stats()`

獲取字庫分類統計。

**返回:**
- `Dict[str, int]`: 分類統計字典

---

### Config

配置管理類別。

```python
from src.config import Config

config = Config(config_path=None)
```

#### 方法

##### `load_config(config_path)`

載入配置檔案。

**參數:**
- `config_path` (str): 配置檔案路徑

**返回:**
- `bool`: 是否載入成功

##### `save_config(config_path)`

儲存配置到檔案。

**參數:**
- `config_path` (str): 配置檔案路徑

**返回:**
- `bool`: 是否儲存成功

##### `add_target_extension(extension)`

添加目標檔案類型。

**參數:**
- `extension` (str): 檔案擴展名

##### `set_config(key, value)`

設置配置值。

**參數:**
- `key` (str): 配置鍵
- `value` (Any): 配置值

**範例:**
```python
config.add_target_extension("log")
config.set_config("create_backup", True)
config.set_config("max_file_size", 5 * 1024 * 1024)
```

---

### FileProcessor

檔案處理器。

```python
from src.file_processor import FileProcessor
from src.config import Config

config = Config()
processor = FileProcessor(config)
```

#### 方法

##### `process_file(file_path, converter, preview_mode=False)`

處理單個檔案。

**參數:**
- `file_path` (Path): 檔案路徑
- `converter` (ChineseConverter): 轉換器實例
- `preview_mode` (bool): 預覽模式

**返回:**
- `FileProcessResult`: 處理結果

##### `scan_directory(directory)`

掃描目錄中的所有符合條件的檔案。

**參數:**
- `directory` (Path): 目錄路徑

**返回:**
- `List[Path]`: 符合條件的檔案列表

---

### StatisticsCollector

統計收集器。

```python
from src.statistics import StatisticsCollector

stats = StatisticsCollector()
```

#### 方法

##### `start_session(project_path, preview_mode=False, file_extensions=None)`

開始新的統計會話。

**參數:**
- `project_path` (str): 專案路徑
- `preview_mode` (bool): 是否為預覽模式
- `file_extensions` (List[str]): 處理的檔案類型

**返回:**
- `str`: 會話ID

##### `end_session()`

結束當前統計會話。

**返回:**
- `Optional[SessionStats]`: 會話統計

##### `get_overall_summary()`

獲取總體摘要。

**返回:**
- `Dict[str, Any]`: 總體摘要字典

---

## 資料結構

### ConversionResult

轉換結果資料類。

```python
@dataclass
class ConversionResult:
    total_files: int = 0           # 總檔案數
    processed_files: int = 0       # 處理檔案數
    total_conversions: int = 0     # 總轉換次數
    errors: List[str] = None       # 錯誤列表
    file_details: List[Tuple[str, int]] = None  # 檔案詳情
```

### FileProcessResult

檔案處理結果資料類。

```python
@dataclass
class FileProcessResult:
    file_path: str                 # 檔案路徑
    processed: bool = False        # 是否已處理
    conversions: int = 0           # 轉換次數
    error: Optional[str] = None    # 錯誤訊息
    preview_data: List[Tuple[str, str, int]] = None  # 預覽資料
```

---

## 使用範例

### 基本轉換
```python
from src.codebridge import CodeBridge

codebridge = CodeBridge()
result = codebridge.convert_project("./my-project")
print(f"轉換了 {result.total_conversions} 個字符")
```

### 預覽模式
```python
result = codebridge.convert_project("./my-project", preview_mode=True)
report = codebridge.generate_report(result, preview_mode=True)
print(report)
```

### 自定義映射
```python
# 載入檔案
codebridge.load_custom_mappings("custom.txt")

# 動態添加
codebridge.mapping_manager.add_custom_mapping("自定义词", "自定義詞")
```

### 配置管理
```python
from src.config import Config

config = Config()
config.add_target_extension("log")
config.set_config("create_backup", True)

codebridge = CodeBridge()
codebridge.config = config
```
