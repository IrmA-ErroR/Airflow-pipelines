-- Таблица currency_exchange_rates:

-- base — код базовой валюты
-- currency — код конвертируемой валюты
-- rate — обменный курс между currency и base, т.е. стоимость base в currency
-- date — дата

CREATE TABLE IF NOT EXISTS currency_exchange_rates (
    base VARCHAR(3) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    rate NUMERIC(12, 3) NOT NULL,
    date DATE NOT NULL,
    UNIQUE (base, currency, date)
);