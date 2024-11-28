intransitables = [(2, 2), (2, 3), (2, 6), (2, 7), (2, 12), (2, 13), (2, 15), (2, 16), (2, 17), (2, 18), (2, 19), (2, 20), (2, 21), (3, 2), (3, 3), (3, 7), (3, 12), (3, 13), (3, 14), (3, 15), (3, 16), (3, 17), (3, 18), (3, 19), (3, 20), (4, 2), (4, 6), (4, 7), (4, 13), (4, 14), (4, 15), (4, 16), (4, 17), (4, 18), (4, 19), (4, 20), (4, 21), (5, 2), (5, 3), (5, 6), (5, 7), (5, 12), (5, 13), (5, 14), (5, 15), (5, 16), (5, 18), (5, 19), (5, 20), (5, 21), (8, 2), (8, 3), (8, 6), (8, 7), (8, 12), (8, 13), (8, 14), (8, 16), (8, 19), (8, 20), (8, 21), (9, 3), (9, 6), (9, 7), (9, 12), (9, 13), (9, 14), (9, 15), (9, 16), (9, 19), (9, 20), (9, 21), (10, 2), (10, 3), (10, 6), (10, 13), (10, 14), (10, 15), (10, 16), (10, 20), (10, 21), (11, 2), (11, 3), (11, 6), (11, 7), (11, 12), (11, 13), (11, 14), (11, 15), (11, 16), (11, 19), (11, 20), (11, 21), (13, 9), (13, 10), (14, 9), (14, 10), (16, 2), (16, 3), (16, 4), (16, 5), (16, 6), (16, 7), (16, 12), (16, 13), (16, 14), (16, 15), (16, 18), (16, 19), (16, 20), (16, 21), (17, 2), (17, 3), (17, 5), (17, 7), (17, 12), (17, 13), (17, 14), (17, 15), (17, 18), (17, 19), (17, 20), (18, 12), (18, 13), (18, 14), (18, 15), (18, 18), (18, 19), (18, 20), (18, 21), (19, 12), (19, 13), (19, 14), (19, 15), (19, 18), (19, 19), (19, 20), (19, 21), (20, 2), (20, 3), (20, 5), (20, 6), (20, 7), (20, 12), (20, 13), (20, 14), (20, 19), (20, 20), (20, 21), (21, 2), (21, 3), (21, 4), (21, 5), (21, 6), (21, 7), (21, 12), (21, 13), (21, 14), (21, 15), (21, 18), (21, 19), (21, 20), (21, 21)]

transitables = {'N': {(15, 21), (6, 18), (23, 4), (7, 17), (22, 17), (14, 13), (15, 5), (15, 14), (6, 20), (7, 19), (22, 10), (22, 19), (19, 2), (14, 15), (15, 7), (18, 3), (15, 16), (6, 13), (7, 12), (7, 21), (22, 3), (22, 12), (19, 4), (22, 21), (23, 20), (14, 17), (15, 9), (18, 5), (15, 18), (7, 14), (22, 5), (22, 14), (23, 13), (19, 6), (23, 22), (14, 19), (15, 2), (15, 11), (18, 7), (7, 16), (22, 7), (23, 6), (14, 3), (22, 16), (23, 15), (14, 12), (14, 21), (15, 4), (15, 13), (22, 9), (23, 8), (14, 5), (22, 18), (23, 17), (14, 14), (15, 6), (18, 2), (22, 2), (23, 1), (6, 15), (22, 11), (23, 10), (14, 7), (22, 20), (23, 19), (14, 16), (18, 4), (22, 4), (23, 3), (6, 17), (15, 20), (22, 13), (23, 12), (23, 21), (14, 18), (22, 6), (23, 5), (6, 19), (14, 2), (7, 18), (23, 14), (15, 15), (6, 12), (22, 8), (23, 7), (14, 4), (6, 21), (7, 20), (23, 16), (19, 3), (23, 0), (15, 17), (6, 14), (7, 13), (23, 9), (14, 6), (23, 18), (22, 22), (19, 5), (15, 10), (18, 6), (15, 19), (6, 16), (23, 2), (7, 15), (23, 11), (22, 15), (19, 7), (14, 20), (15, 3), (15, 12)}, 'O': {(18, 17), (11, 1), (11, 0), (21, 16), (5, 10), (14, 22), (3, 22), (8, 18), (9, 17), (2, 11), (11, 23), (6, 11), (7, 10), (18, 10), (15, 23), (16, 22), (20, 22), (8, 11), (19, 11), (9, 10), (17, 23), (4, 23), (2, 4), (5, 5), (17, 16), (5, 23), (10, 22), (16, 17), (7, 23), (18, 23), (20, 17), (3, 10), (22, 23), (12, 22), (16, 10), (13, 23), (18, 16), (20, 10), (17, 11), (4, 11), (10, 17), (1, 23), (2, 22), (21, 11), (3, 5), (6, 22), (4, 4), (5, 11), (3, 23), (14, 23), (4, 22), (10, 10), (19, 22), (8, 22), (11, 18), (18, 11), (7, 11), (16, 23), (20, 23), (5, 4), (21, 22), (13, 11), (11, 11), (9, 23), (16, 16), (20, 16), (19, 17), (8, 17), (2, 10), (10, 23), (11, 22), (6, 10), (15, 22), (21, 17), (3, 11), (14, 11), (4, 10), (23, 23), (12, 23), (19, 10), (8, 10), (17, 22), (9, 18), (20, 11), (21, 10), (3, 4), (9, 11), (2, 5), (5, 22), (10, 18), (11, 17), (2, 23), (6, 23), (4, 5), (7, 22), (18, 22), (17, 17), (10, 11), (11, 10), (19, 23), (8, 23), (9, 22), (13, 22), (12, 11), (21, 23), (17, 10), (19, 16), (16, 11), (1, 22)}, 'S': {(12, 4), (0, 5), (0, 14), (0, 23), (6, 2), (13, 17), (1, 15), (12, 18), (0, 7), (0, 16), (1, 8), (6, 4), (7, 3), (13, 19), (1, 17), (12, 20), (0, 9), (13, 3), (13, 12), (1, 10), (6, 6), (7, 5), (13, 21), (1, 19), (12, 13), (0, 2), (13, 5), (1, 3), (13, 14), (1, 12), (7, 7), (1, 21), (12, 6), (12, 15), (13, 7), (1, 5), (13, 16), (1, 14), (12, 8), (12, 17), (1, 7), (7, 2), (13, 18), (0, 18), (1, 16), (12, 10), (12, 19), (13, 2), (1, 9), (0, 11), (7, 4), (1, 18), (0, 20), (12, 3), (12, 12), (12, 21), (13, 4), (1, 2), (0, 4), (1, 11), (0, 13), (1, 20), (0, 22), (12, 5), (12, 14), (1, 4), (0, 6), (1, 13), (0, 15), (6, 3), (12, 7), (12, 16), (1, 6), (0, 8), (0, 17), (6, 5), (13, 20), (12, 9), (0, 1), (0, 10), (0, 19), (13, 13), (6, 7), (7, 6), (12, 2), (1, 1), (0, 3), (0, 12), (13, 6), (0, 21), (13, 15)}, 'E': {(4, 0), (4, 9), (5, 1), (8, 0), (19, 0), (8, 9), (19, 9), (9, 8), (11, 5), (13, 8), (7, 1), (18, 1), (21, 0), (21, 9), (9, 1), (13, 1), (3, 8), (14, 8), (8, 4), (11, 0), (0, 0), (11, 9), (15, 0), (16, 8), (20, 8), (3, 1), (17, 0), (14, 1), (17, 9), (9, 5), (16, 1), (20, 1), (5, 0), (5, 9), (11, 4), (10, 8), (6, 1), (7, 0), (18, 0), (7, 9), (18, 9), (22, 0), (9, 0), (9, 9), (10, 1), (13, 0), (7, 8), (12, 1), (1, 0), (2, 8), (6, 8), (3, 0), (14, 0), (3, 9), (4, 8), (19, 8), (10, 5), (8, 8), (2, 1), (16, 0), (16, 9), (20, 0), (20, 9), (21, 8), (4, 1), (8, 1), (19, 1), (21, 1), (10, 0), (10, 9), (11, 8), (15, 8), (22, 1), (12, 0), (17, 8), (8, 5), (9, 4), (11, 1), (15, 1), (17, 1), (5, 8), (10, 4), (2, 0), (2, 9), (6, 0), (6, 9), (18, 8)}}

banquetas = [(2,2),(3,2),(4,2),(5,2),(5,3),(2,3),(2,6),(2,7), 
            (2,7),(3,7),(4,7),(5,7),(5,6),(8,2),(10,2),(11,2),
            (8,3),(11,3),(8,6),(8,7),(9,7),(11,7),(11,6),(2,12),
            (3,12),(5,12),(2,13),(2,15),(2,16),(2,17),(2,18),
            (2,19),(2,20),(2,21),(4,21),(5,21),(5,20),(5,19),
            (5,18),(5,16),(5,15),(5,14),(5,13),(5,12),(8,12),(9,12),
            (11,12),(8,13),(8,14),(8,16),(9,16),(10,16),(11,16),(11,15),
            (11,14),(11,13),(11,12),(8,19),(9,19),(11,19),(11,20),(11,21),
            (10,21),(9,21),(8,21),(8,20),(16,12),(17,12),(18,12),(19,12),
            (20,12),(21,12),(21,13),(21,14),(21,15),(19,15),(18,15),(17,15),
            (16,15),(16,14),(16,13),(16,18),(17,18),(18,18),(19,18),(21,18),
            (21,19),(21,20),(21,21),(20,21),(19,21),(18,21),(16,21),(16,20),
            (16,19)
            ]

estacionamientos = {'A': (3, 21), 'B': (17, 21), 'C': (10, 19), 'D': (5, 17), 'E': (20, 18), 'F': (8, 15), 'G': (20, 15), 'H': (2, 14), 'I': (4, 12), 'J': (10, 12), 'K': (10, 7), 'L': (3, 6), 'M': (17, 6), 'N': (4, 3), 'O': (17, 4), 'P': (20, 4), 'Q': (20, 4), 'R': (9, 2)}

semaforosV = {
    'H': [(0,6),(1,6),(6,2),(7,2),(18,7),(19,7),(6,16),(7,16),(6,21),(7,21)],
    'V': [(2,4),(2,5),(5,0),(5,1),(8,17),(8,18),(8,22),(8,23),(17,8),(17,9)]
}

semaforosP = [(2,3),(8,2),(20,7),(5,16),(5,21),(8,19)]