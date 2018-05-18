import datetime


def get_high_scores(conn, game_id):
    cursor = conn.cursor()
    sql_statement = 'SELECT scores.DatePlayed, scores.User, scores.Score FROM scores ' \
                    'INNER JOIN games ON scores.GameID = games.ID ' \
                    'WHERE games.ID = ? ORDER BY Score DESC LIMIT 5'
    scores = cursor.execute(sql_statement, (game_id,)).fetchall()
    return scores


def add_score(conn, user, game_id, score):
    cursor = conn.cursor()
    sql_statement = 'INSERT INTO scores (DatePlayed, User, GameID, Score) VALUES (?, ?, ?, ?)'
    cursor.execute(sql_statement, (datetime.datetime.now(), user, game_id, score))
    conn.commit()


def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE scores (DatePlayed DATETIME, User CHARACTER(3), GameID INTEGER, Score INTEGER)')
    cursor.execute('CREATE TABLE games (ID INTEGER, Name TEXT)')
    conn.commit()
