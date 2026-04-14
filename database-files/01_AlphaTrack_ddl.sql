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

