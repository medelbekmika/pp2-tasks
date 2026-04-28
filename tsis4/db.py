import psycopg2
from config import load_config


def connect():
    try:
        config = load_config()
        return psycopg2.connect(**config)
    except Exception as e:
        print("DB connection error:", e)
        return None


def get_or_create_player(username: str):
    conn = connect()
    if conn is None:
        return None

    try:
        cur = conn.cursor()

        cur.execute("SELECT id FROM players WHERE username = %s", (username,))
        row = cur.fetchone()

        if row:
            player_id = row[0]
        else:
            cur.execute(
                "INSERT INTO players(username) VALUES (%s) RETURNING id",
                (username,)
            )
            player_id = cur.fetchone()[0]
            conn.commit()

        cur.close()
        conn.close()
        return player_id

    except Exception as e:
        print("DB error:", e)
        conn.rollback()
        conn.close()
        return None


def save_result(username: str, score: int, level_reached: int):
    conn = connect()
    if conn is None:
        return

    try:
        cur = conn.cursor()

        cur.execute("SELECT id FROM players WHERE username = %s", (username,))
        row = cur.fetchone()

        if row:
            player_id = row[0]
        else:
            cur.execute(
                "INSERT INTO players(username) VALUES (%s) RETURNING id",
                (username,)
            )
            player_id = cur.fetchone()[0]

        cur.execute(
            """
            INSERT INTO game_sessions(player_id, score, level_reached)
            VALUES (%s, %s, %s)
            """,
            (player_id, score, level_reached)
        )

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        print("Save result error:", e)
        conn.rollback()
        conn.close()


def get_top_scores(limit: int = 10):
    conn = connect()
    if conn is None:
        return []

    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT p.username, g.score, g.level_reached, g.played_at
            FROM game_sessions g
            JOIN players p ON g.player_id = p.id
            ORDER BY g.score DESC, g.level_reached DESC, g.played_at DESC
            LIMIT %s
            """,
            (limit,)
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    except Exception as e:
        print("Leaderboard error:", e)
        conn.close()
        return []


def get_personal_best(username: str) -> int:
    conn = connect()
    if conn is None:
        return 0

    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT COALESCE(MAX(g.score), 0)
            FROM game_sessions g
            JOIN players p ON g.player_id = p.id
            WHERE p.username = %s
            """,
            (username,)
        )
        best = cur.fetchone()[0]
        cur.close()
        conn.close()
        return int(best)

    except Exception as e:
        print("Personal best error:", e)
        conn.close()
        return 0
