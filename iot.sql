CREATE TABLE iot (
    id INT PRIMARY KEY,
    dispositivo TEXT,
    valor INT
);

INSERT INTO iot (id, dispositivo, valor) VALUES (1, 'led', 0);
INSERT INTO iot (id, dispositivo, valor) VALUES (2, 'sensor', 0);
