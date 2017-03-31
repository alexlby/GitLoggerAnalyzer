# GitLoggerAnalyzer
练手用的git日志分析小程序, 基于Python实现
1. 解析git log, 根据约定的commit message进行分析
2. 抽离每次commit中的需求部分 start with "ST", 插入db用于后续report分析
3. 抽离每次commit中的bugfix部分 start with "DE", 插入db用于后续report分析
4. report分析,生成柱状图
