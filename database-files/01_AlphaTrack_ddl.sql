-- alphatrack database ddl file

DROP DATABASE IF EXISTS alphatrack;
CREATE DATABASE alphatrack;
USE alphatrack;


CREATE TABLE User (
    user_id     INT AUTO_INCREMENT PRIMARY KEY,
    first_name  VARCHAR(50) NOT NULL,
    last_name   VARCHAR(50) NOT NULL,
    email       VARCHAR(100) NOT NULL UNIQUE,
    status      VARCHAR(20) DEFAULT 'active',
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    deactivated_at DATETIME
);

CREATE TABLE Role (
    role_id          INT AUTO_INCREMENT PRIMARY KEY,
    role_name        VARCHAR(50) NOT NULL UNIQUE,
    role_description VARCHAR(255),
    is_active        BOOLEAN DEFAULT TRUE,
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE User_Role (
    user_role_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id      INT NOT NULL,
    role_id      INT NOT NULL,
    assigned_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_user_role (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES Role(role_id) ON DELETE CASCADE
);

CREATE TABLE Asset (
    asset_id      INT AUTO_INCREMENT PRIMARY KEY,
    ticker        VARCHAR(10) NOT NULL UNIQUE,
    asset_name    VARCHAR(100) NOT NULL,
    asset_type    VARCHAR(50) NOT NULL,
    current_price DECIMAL(10,2)
);

CREATE TABLE Price_History (
    price_id      INT AUTO_INCREMENT PRIMARY KEY,
    asset_id      INT NOT NULL,
    date          DATE NOT NULL,
    closing_price DECIMAL(10,2) NOT NULL,
    UNIQUE KEY unique_price (asset_id, date),
    FOREIGN KEY (asset_id) REFERENCES Asset(asset_id) ON DELETE CASCADE
);

CREATE TABLE Benchmark (
    benchmark_id   INT AUTO_INCREMENT PRIMARY KEY,
    benchmark_name VARCHAR(100) NOT NULL,
    ticker         VARCHAR(10) NOT NULL UNIQUE
);

CREATE TABLE Benchmark_Price_History (
    bph_price_id  INT AUTO_INCREMENT PRIMARY KEY,
    benchmark_id  INT NOT NULL,
    date          DATE NOT NULL,
    closing_price DECIMAL(10,2) NOT NULL,
    UNIQUE KEY unique_bph (benchmark_id, date),
    FOREIGN KEY (benchmark_id) REFERENCES Benchmark(benchmark_id) ON DELETE CASCADE
);

CREATE TABLE Portfolio (
    portfolio_id      INT AUTO_INCREMENT PRIMARY KEY,
    user_id           INT NOT NULL,
    benchmark_id      INT,
    portfolio_name    VARCHAR(100) NOT NULL,
    total_value       DECIMAL(15,2) DEFAULT 0.00,
    created_date      DATETIME DEFAULT CURRENT_TIMESTAMP,
    performance_metric DECIMAL(10,4),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (benchmark_id) REFERENCES Benchmark(benchmark_id) ON DELETE SET NULL
);

CREATE TABLE Holding (
    holding_id         INT AUTO_INCREMENT PRIMARY KEY,
    portfolio_id       INT NOT NULL,
    asset_id           INT NOT NULL,
    quantity           DECIMAL(15,6) DEFAULT 0,
    avg_cost           DECIMAL(10,2),
    current_value      DECIMAL(15,2),
    allocation_percent DECIMAL(5,2),
    weight             DECIMAL(5,4),
    UNIQUE KEY unique_holding (portfolio_id, asset_id),
    FOREIGN KEY (portfolio_id) REFERENCES Portfolio(portfolio_id) ON DELETE CASCADE,
    FOREIGN KEY (asset_id) REFERENCES Asset(asset_id) ON DELETE CASCADE
);

CREATE TABLE Watchlist (
    watchlist_id   INT AUTO_INCREMENT PRIMARY KEY,
    user_id        INT NOT NULL,
    watchlist_name VARCHAR(100) NOT NULL,
    created_date   DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE Watchlist_Asset (
    watchlist_id INT NOT NULL,
    asset_id     INT NOT NULL,
    PRIMARY KEY (watchlist_id, asset_id),
    FOREIGN KEY (watchlist_id) REFERENCES Watchlist(watchlist_id) ON DELETE CASCADE,
    FOREIGN KEY (asset_id) REFERENCES Asset(asset_id) ON DELETE CASCADE
);

-- bobby

CREATE TABLE Risk_Metrics (
    metric_id        INT AUTO_INCREMENT PRIMARY KEY,
    portfolio_id     INT NOT NULL,
    sharpe_ratio     DECIMAL(10,4),
    volatility       DECIMAL(10,4),
    max_drawdown     DECIMAL(10,4),
    date_range_start DATE NOT NULL,
    date_range_end   DATE NOT NULL,
    UNIQUE KEY unique_metric (portfolio_id, date_range_start, date_range_end),
    FOREIGN KEY (portfolio_id) REFERENCES Portfolio(portfolio_id) ON DELETE CASCADE
);

-- mike

CREATE TABLE `Transaction` (
    transaction_id   INT AUTO_INCREMENT PRIMARY KEY,
    portfolio_id     INT NOT NULL,
    asset_id         INT NOT NULL,
    transaction_type VARCHAR(10) NOT NULL,
    shares           DECIMAL(15,6) NOT NULL,
    price_per_share  DECIMAL(10,2) NOT NULL,
    trade_date       DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (portfolio_id) REFERENCES Portfolio(portfolio_id) ON DELETE CASCADE,
    FOREIGN KEY (asset_id) REFERENCES Asset(asset_id) ON DELETE CASCADE
);

CREATE TABLE Performance_History (
    performance_id  INT AUTO_INCREMENT PRIMARY KEY,
    portfolio_id    INT NOT NULL,
    date            DATE NOT NULL,
    portfolio_value DECIMAL(15,2) NOT NULL,
    gain_loss       DECIMAL(15,2),
    UNIQUE KEY unique_performance (portfolio_id, date),
    FOREIGN KEY (portfolio_id) REFERENCES Portfolio(portfolio_id) ON DELETE CASCADE
);

-- james

CREATE TABLE Client (
    client_id      INT AUTO_INCREMENT PRIMARY KEY,
    user_id        INT NOT NULL,
    name           VARCHAR(100) NOT NULL,
    email          VARCHAR(100) NOT NULL UNIQUE,
    account_status VARCHAR(20) DEFAULT 'active',
    risk_tolerance VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE Risk_Profile (
    risk_profile_id INT AUTO_INCREMENT PRIMARY KEY,
    client_id       INT NOT NULL,
    risk_level      VARCHAR(20) NOT NULL,
    threshold_min   DECIMAL(10,4),
    threshold_max   DECIMAL(10,4),
    FOREIGN KEY (client_id) REFERENCES Client(client_id) ON DELETE CASCADE
);

CREATE TABLE Alert (
    alert_id   INT AUTO_INCREMENT PRIMARY KEY,
    client_id  INT NOT NULL,
    alert_type VARCHAR(50) NOT NULL,
    message    TEXT,
    timestamp  DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES Client(client_id) ON DELETE CASCADE
);

CREATE TABLE Report (
    report_id      INT AUTO_INCREMENT PRIMARY KEY,
    client_id      INT NOT NULL,
    report_type    VARCHAR(50) NOT NULL,
    summary        TEXT,
    generated_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES Client(client_id) ON DELETE CASCADE
);

-- gregory
CREATE TABLE Activity_Log (
    log_id            INT AUTO_INCREMENT PRIMARY KEY,
    user_id           INT NOT NULL,
    event_type        VARCHAR(50) NOT NULL,
    event_category    VARCHAR(50),
    event_description TEXT,
    ip_address        VARCHAR(45),
    created_at        DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE Backup (
    backup_id        INT AUTO_INCREMENT PRIMARY KEY,
    backup_name      VARCHAR(100) NOT NULL,
    backup_status    VARCHAR(20) DEFAULT 'pending',
    storage_location VARCHAR(255),
    backup_size_gb   DECIMAL(10,2),
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    restore_tested_at DATETIME
);

-- sample data generated from ai

INSERT INTO User (first_name, last_name, email, status) VALUES
('Bobby', 'James', 'bobby.james@firm.com', 'active'),
('Mike', 'Gasly', 'mike.gasly@espn.com', 'active'),
('Gregory', 'Hilton', 'gregory.hilton@alphatrack.com', 'active'),
('James', 'Carter', 'james.carter@firm.com', 'active');

INSERT INTO Role (role_name, role_description, is_active) VALUES
('Portfolio Analyst', 'Can view and analyze portfolios', TRUE),
('Retail Investor', 'Can manage personal portfolio', TRUE),
('System Admin', 'Full system access', TRUE),
('Financial Advisor', 'Can manage client portfolios', TRUE);

INSERT INTO User_Role (user_id, role_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4);

INSERT INTO Asset (ticker, asset_name, asset_type, current_price) VALUES
('AAPL', 'Apple Inc.', 'Equity', 185.20),
('MSFT', 'Microsoft Corporation', 'Equity', 374.00),
('SPY', 'SPDR S&P 500 ETF', 'ETF', 480.50),
('BND', 'Vanguard Bond ETF', 'Bond', 72.30);

INSERT INTO Price_History (asset_id, date, closing_price) VALUES
(1, '2024-01-01', 182.50),
(1, '2024-01-02', 183.75),
(2, '2024-01-01', 370.00),
(2, '2024-01-02', 372.50);

INSERT INTO Benchmark (benchmark_name, ticker) VALUES
('S&P 500', 'SPY'),
('NASDAQ 100', 'QQQ');

INSERT INTO Benchmark_Price_History (benchmark_id, date, closing_price) VALUES
(1, '2024-01-01', 478.00),
(1, '2024-01-02', 479.50),
(2, '2024-01-01', 410.00);

INSERT INTO Portfolio (user_id, benchmark_id, portfolio_name, total_value) VALUES
(1, 1, 'Tech Growth Fund', 150000.00),
(2, 1, 'Mike Personal Portfolio', 25000.00),
(4, 2, 'Client A Portfolio', 200000.00);

INSERT INTO Holding (portfolio_id, asset_id, quantity, avg_cost, current_value, allocation_percent, weight) VALUES
(1, 1, 100.00, 170.00, 18520.00, 12.35, 0.1235),
(1, 2, 50.00, 350.00, 18700.00, 12.47, 0.1247),
(2, 1, 20.00, 180.00, 3704.00, 14.82, 0.1482);

INSERT INTO Watchlist (user_id, watchlist_name) VALUES
(1, 'Tech Concentration'),
(2, 'Mike Watchlist');

INSERT INTO Watchlist_Asset (watchlist_id, asset_id) VALUES
(1, 1),
(1, 2),
(2, 3);

INSERT INTO Risk_Metrics (portfolio_id, sharpe_ratio, volatility, max_drawdown, date_range_start, date_range_end) VALUES
(1, 1.42, 0.183, -0.221, '2023-01-01', '2023-12-31'),
(2, 0.98, 0.215, -0.180, '2023-01-01', '2023-12-31');

INSERT INTO `Transaction` (portfolio_id, asset_id, transaction_type, shares, price_per_share) VALUES
(2, 1, 'BUY', 20.00, 180.00),
(2, 3, 'BUY', 10.00, 475.00),
(2, 1, 'SELL', 5.00, 185.00);

INSERT INTO Performance_History (portfolio_id, date, portfolio_value, gain_loss) VALUES
(2, '2024-01-01', 24000.00, -1000.00),
(2, '2024-02-01', 25500.00, 1500.00),
(2, '2024-03-01', 25000.00, -500.00);

INSERT INTO Client (user_id, name, email, account_status, risk_tolerance) VALUES
(4, 'Sarah Lee', 'sarah.lee@firm.com', 'active', 'moderate'),
(4, 'Tom Reyes', 'tom.reyes@firm.com', 'active', 'aggressive');

INSERT INTO Risk_Profile (client_id, risk_level, threshold_min, threshold_max) VALUES
(1, 'moderate', 0.05, 0.15),
(2, 'aggressive', 0.10, 0.25);

INSERT INTO Alert (client_id, alert_type, message) VALUES
(1, 'risk_breach', 'Portfolio exceeded risk threshold'),
(2, 'rebalance', 'Portfolio drift detected');

INSERT INTO Report (client_id, report_type, summary) VALUES
(1, 'monthly', 'Monthly performance summary for Sarah Lee'),
(2, 'quarterly', 'Quarterly review for Tom Reyes');

INSERT INTO Activity_Log (user_id, event_type, event_category, event_description, ip_address) VALUES
(3, 'LOGIN', 'AUTH', 'Admin user logged in', '192.168.1.1'),
(3, 'USER_DEACTIVATED', 'USER_MGMT', 'Deactivated inactive user account', '192.168.1.1');

INSERT INTO Backup (backup_name, backup_status, storage_location, backup_size_gb) VALUES
('backup_2026_03_29', 'complete', '/backups/2026/03/29', 2.40),
('backup_2026_03_22', 'complete', '/backups/2026/03/22', 2.10);