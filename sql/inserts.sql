INSERT INTO clube (nome) VALUES
('Chapecoense')
;

INSERT INTO usuario (email, password, nome, id_clube, data_de_registro) VALUES
('teste@teste.gmail.com', 'beberunsdanone', 'Testador', 1, now())
;

INSERT INTO modulo (nome) VALUES
('Desempenho Físico'),
('Desempenho Técnico'),
('Desempenho Tático')
;

INSERT INTO tipo_estatistica (nome, id_modulo) VALUES
('Distância percorrida', 1),
('Velocidade máxima', 1),
('Desgaste previsto', 1),

('Faltas sofridas', 2),
('Gols por jogador', 2),
('Passes completados', 2),
('Passes errados', 2)
;
