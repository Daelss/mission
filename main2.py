import psycopg2

# Подключение к базе данных
conn = psycopg2.connect("dbname=test user=postgres password=123 options='-c client_encoding=utf8'")

# Создание курсора для выполнения операций в базе данных
cur = conn.cursor()

# # Создание таблицы сущности "Заказы"
# cur.execute("CREATE TABLE Orders (order_id SERIAL PRIMARY KEY, date DATE, client_id INT, status VARCHAR(20))")
# conn.commit()

# Заполнение таблицы Orders
cur.execute("INSERT INTO Orders (date, client_id, status) VALUES ('2022-01-01', 1, 'Новый')")
cur.execute("INSERT INTO Orders (date, client_id, status) VALUES ('2022-01-02', 2, 'В работе')")
# Добавьте еще записей по аналогии

# Создание процедуры для проверки адреса электронной почты
cur.execute("""
CREATE OR REPLACE FUNCTION check_email(email VARCHAR) RETURNS BOOLEAN AS $$
BEGIN
    -- Проверка на корректность адреса электронной почты
    RETURN email ~* '^[A-Z0-9._%+-]+@[A-Z0-9.-]+.[A-Z]{2,}$';
END;
$$ LANGUAGE plpgsql;
""")
conn.commit()

# # Создание таблицы для истории изменения статусов заказов
# cur.execute("CREATE TABLE History (change_date DATE, order_id INT, order_date DATE, old_status VARCHAR(20), new_status VARCHAR(20))")
# conn.commit()

# # Создание триггера для отслеживания изменения статусов заказов
# cur.execute("""
# CREATE OR REPLACE FUNCTION trigger_history()
# RETURNS TRIGGER AS $$
# BEGIN
#     INSERT INTO History (change_date, order_id, order_date, old_status, new_status)
#     VALUES (current_date, NEW.order_id, NEW.date, OLD.status, NEW.status);
#     RETURN NEW;
# END;
# $$ LANGUAGE plpgsql;
#
# CREATE TRIGGER status_change
# AFTER UPDATE OF status ON Orders
# FOR EACH ROW
# EXECUTE FUNCTION trigger_history();
# """)
# conn.commit()

# Вывести список клиентов с указанием данных о заказе и суммы к оплате
query = """
SELECT c.client_name, o.order_number, o.order_date, SUM(p.price * op.quantity) AS total_payment
FROM clients c
JOIN orders o ON c.client_id = o.client_id
JOIN order_products op ON o.order_id = op.order_id
JOIN products p ON op.product_id = p.product_id
GROUP BY c.client_id, o.order_id;
"""

# Удалить из базы данных все просроченные лекарства
delete_query = "DELETE FROM products WHERE expiration_date < CURDATE();"

# Обновить цену на российские лекарства уменьшив цену на 15%
update_query = "UPDATE products SET price = price * 0.85 WHERE country = 'Russia';"

# Закрытие курсора и соединения
cur.close()
conn.close()
