INSERT INTO currency_exchange_rates (base, currency, rate, date)
VALUES (%s, %s, %s, %s)
ON CONFLICT (base, currency, date) DO NOTHING;