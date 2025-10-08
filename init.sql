-- 数据库初始化脚本
-- 创建必要的数据库扩展和初始数据

-- 创建UUID扩展（如果需要）
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 创建应用用户（可选，在生产环境中推荐）
-- CREATE USER gushi_user WITH PASSWORD 'gushi_password';
-- GRANT ALL PRIVILEGES ON DATABASE gushi_db TO gushi_user;

-- 创建初始表结构（Flask应用会在启动时自动创建）
-- 这里可以添加一些初始数据或特殊配置

-- 创建索引以提高查询性能
-- CREATE INDEX idx_stocks_symbol ON stocks(symbol);
-- CREATE INDEX idx_stocks_market_cap ON stocks(market_cap);
-- CREATE INDEX idx_stock_data_symbol_date ON stock_data(stock_symbol, date);
-- CREATE INDEX idx_analysis_results_symbol ON analysis_results(stock_symbol);
-- CREATE INDEX idx_analysis_results_type ON analysis_results(analysis_type);

-- 插入一些示例数据（可选）
-- INSERT INTO stocks (symbol, name, industry, market_cap, pe_ratio, pb_ratio) VALUES 
-- ('000001', '平安银行', '金融', 100000000000, 8.5, 0.8),
-- ('000002', '万科A', '房地产', 80000000000, 12.3, 1.2);

-- 授权（生产环境中应细化权限）
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO gushi_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO gushi_user;