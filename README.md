# data-security-experiment

基础工具实验：读取 UTF-8 文本并统计单词频次。需要 Python 3，无第三方依赖。

## 项目文件

- `code/demo.py`：命令行程序，核心统计函数为 `count_words(text)`。
- `sample.txt`：示例输入。
- `result/run_result.txt`：已保存的示例结果，程序不会自动更新该文件。
- `tests/test_demo.py`：使用 unittest 编写的单元测试与命令行测试。

## 运行方法

在项目根目录执行，默认读取当前工作目录下的 `sample.txt`：

```powershell
python code/demo.py
```

也可以指定输入文件的相对路径或绝对路径，含空格的路径请加引号：

```powershell
python code/demo.py "path/to/input.txt"
python code/demo.py --help
```

程序将文本统一转换为小写，把英文标点和 Unicode 标点（包括常见中文标点）作为分隔符，再按空白分词。比如 `Hello,world! HELLO` 会得到 `hello: 2` 和 `world: 1`。连字符和撇号也作为分隔符；不进行中文分词。

结果按单词字典顺序输出到终端。文件不存在时，程序在标准错误中显示 `Input file not found` 及文件路径，并以状态码 2 退出，不显示异常堆栈。

## 运行测试

在项目根目录执行：

```powershell
python -B -m unittest discover -s tests -v
```
