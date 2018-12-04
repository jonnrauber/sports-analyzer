INSERT INTO clube (nome) VALUES
('Chapecoense'),
('São Paulo'),
('Figueirense')
;

INSERT INTO jogador (nome, idade, id_clube) VALUES
('Walter Branco', 33, 1),
('Chimbinha', 24, 1)
;

INSERT INTO modulo (nome) VALUES
('Desempenho Físico'),
('Desempenho Técnico'),
('Desempenho Tático')
;

INSERT INTO tipo_estatistica (nome, id_modulo, unidade_medida) VALUES
('Distância percorrida', 1, 'm'),
('Velocidade máxima', 1, 'km/h'),
('Desgaste previsto', 1, '%'),

('Faltas sofridas', 2, ''),
('Gols por jogador', 2, ''),
('Passes completados', 2, ''),
('Passes errados', 2, '')
;

INSERT INTO esquema_tatico (formacao) VALUES
('4-3-3'), ('4-4-2'), ('4-1-4-1'), ('4-5-1'),
('4-2-3-1'), ('4-3-2-1'), ('3-5-2'), ('3-4-3'),
('3-6-1'), ('5-3-2'), ('5-4-1')
;

INSERT INTO jogo (data, local, id_time, id_adversario, id_esquema_tatico, placar_time, placar_adversario)
SELECT '02/12/2018', 1, clube.id, adversario.id, esquema_tatico.id, 1, 0
FROM clube, clube adversario, esquema_tatico
WHERE clube.nome = 'Chapecoense'
AND adversario.nome = 'São Paulo'
AND esquema_tatico.formacao = '4-3-3';

INSERT INTO jogo (data, local, id_time, id_adversario, id_esquema_tatico, placar_time, placar_adversario)
SELECT '10/12/2018', 0, clube.id, adversario.id, esquema_tatico.id, 2, 1
FROM clube, clube adversario, esquema_tatico
WHERE clube.nome = 'Chapecoense'
AND adversario.nome = 'Figueirense'
AND esquema_tatico.formacao = '4-4-2';


INSERT INTO estatistica (id_jogo, id_jogador, id_tipo_estatistica, quantidade) VALUES
(1, 1, 1, 10000),
(1, 1, 2, 25),
(1, 1, 3, 98), --jogo 1 / jogador 1
(1, 1, 4, 6),
(1, 1, 5, 1),
(1, 1, 6, 19),
(1, 1, 7, 4),

(1, 2, 1, 8000),
(1, 2, 2, 24),
(1, 2, 3, 98), --jogo 1 / jogador 2
(1, 2, 4, 7),
(1, 2, 5, 0),
(1, 2, 6, 30),
(1, 2, 7, 5),

(2, 1, 1, 9200),
(2, 1, 2, 27),
(2, 1, 3, 93), --jogo 2 / jogador 1
(2, 1, 4, 3),
(2, 1, 5, 0),
(2, 1, 6, 22),
(2, 1, 7, 3)
;

INSERT INTO usuario (email, password, nome, id_clube, data_de_registro) VALUES
('teste@teste.gmail.com', 'beberunsdanone', 'Testador', 1, now())
;
