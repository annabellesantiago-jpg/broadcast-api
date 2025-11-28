# app_pg_simple.py
from flask import Flask, request, jsonify
import psycopg2
import datetime as dt

app = Flask(__name__)

# ---------- DB Connection ----------
def get_conn():
    return psycopg2.connect(
        dbname="broadcast_db",
        user="postgres",
        password="admin",   # adjust to your local setup
        host="localhost",
        port=5432
    )

# ---------- Helpers ----------
def serialize_broadcast(row):
    return {
        "id": row[0],
        "title": row[1],
        "body": row[2],
        "status": row[3],
        "created_at": row[4].isoformat() if row[4] else None,
        "scheduled_at": row[5].isoformat() if row[5] else None,
    }

def serialize_log(row):
    return {
        "id": row[0],
        "broadcast_id": row[1],
        "status": row[2],
        "message": row[3],
        "created_at": row[4].isoformat() if row[4] else None,
    }

# ---------- Endpoints ----------

@app.post("/broadcasts")
def create_broadcast():
    data = request.get_json() or {}
    title = data.get("title")
    body = data.get("body")
    scheduled_at = data.get("scheduled_at")

    if not title or not body:
        return jsonify({"error": "title and body required"}), 400

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO broadcasts (title, body, scheduled_at) VALUES (%s, %s, %s) RETURNING *",
        (title, body, scheduled_at)
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"broadcast": serialize_broadcast(row)}), 201


@app.get("/broadcasts")
def list_broadcasts():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM broadcasts ORDER BY created_at DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({"broadcasts": [serialize_broadcast(r) for r in rows]})


@app.get("/broadcasts/<int:broadcast_id>")
def get_broadcast(broadcast_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM broadcasts WHERE id=%s", (broadcast_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return jsonify({"error": "not found"}), 404
    return jsonify({"broadcast": serialize_broadcast(row)})


@app.put("/broadcasts/<int:broadcast_id>")
def update_broadcast(broadcast_id):
    data = request.get_json() or {}
    title = data.get("title")
    body = data.get("body")
    scheduled_at = data.get("scheduled_at")

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT status FROM broadcasts WHERE id=%s", (broadcast_id,))
    status_row = cur.fetchone()
    if not status_row:
        return jsonify({"error": "not found"}), 404
    if status_row[0] == "sent":
        return jsonify({"error": "cannot modify a sent broadcast"}), 400

    cur.execute(
        "UPDATE broadcasts SET title=%s, body=%s, scheduled_at=%s WHERE id=%s RETURNING *",
        (title, body, scheduled_at, broadcast_id)
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"broadcast": serialize_broadcast(row)})


@app.delete("/broadcasts/<int:broadcast_id>")
def delete_broadcast(broadcast_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM broadcasts WHERE id=%s RETURNING id", (broadcast_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not deleted:
        return jsonify({"error": "not found"}), 404
    return jsonify({"message": "deleted"})


@app.post("/broadcasts/<int:broadcast_id>/send")
def send_broadcast(broadcast_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM broadcasts WHERE id=%s", (broadcast_id,))
    b = cur.fetchone()
    if not b:
        return jsonify({"error": "not found"}), 404
    if b[3] == "sent":
        return jsonify({"error": "already sent"}), 400

    # mark as sent
    cur.execute("UPDATE broadcasts SET status='sent' WHERE id=%s RETURNING *", (broadcast_id,))
    updated = cur.fetchone()

    # log entry
    cur.execute(
        "INSERT INTO broadcast_logs (broadcast_id, status, message) VALUES (%s, %s, %s) RETURNING *",
        (broadcast_id, "queued", "Push job queued")
    )
    log_row = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()
    return jsonify({
        "message": "broadcast sent",
        "broadcast": serialize_broadcast(updated),
        "log": serialize_log(log_row),
    }), 202


@app.get("/broadcasts/<int:broadcast_id>/logs")
def get_logs(broadcast_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM broadcast_logs WHERE broadcast_id=%s ORDER BY created_at DESC", (broadcast_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({"logs": [serialize_log(r) for r in rows]})


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
