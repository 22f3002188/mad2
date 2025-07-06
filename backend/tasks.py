# tasks.py
from celery import current_app as celery
from flask_mail import Mail, Message
from models import get_connection
from app import app  # ✅ fix for RuntimeError

mail = Mail(app)


@celery.task(name='tasks.send_daily_reminders')
def send_daily_reminders():
    with app.app_context():  # ✅ fixed context
        conn = get_connection()
        cursor = conn.cursor()

        # TEMP: Email all users for testing
        cursor.execute("SELECT email, full_name FROM users WHERE role = 'user'")
        users = cursor.fetchall()

        print(f"[Daily Reminder] Found {len(users)} users")

        for user in users:
            email = user['email']
            name = user['full_name']

            msg = Message(
                subject="📢 Daily Quiz Reminder",
                recipients=[email],
                html=f"""
                <p>Hello {name},</p>
                <p>This is your daily reminder to attempt quizzes.</p>
                <p><b>Log in to Quiz Nation and don't miss your streak!</b></p>
                """
            )
            print(f"[Daily Reminder] Sending email to {email}")
            mail.send(msg)

        conn.close()



@celery.task(name='tasks.send_monthly_report')
def send_monthly_report():
    with app.app_context():  # ✅ fixed context
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT email, full_name FROM users WHERE role = 'user'")
        users = cursor.fetchall()

        for user in users:
            email = user['email']
            name = user['full_name']

            cursor.execute("""
                SELECT s.date_attempt, q.quiz_name, s.score
                FROM score s
                JOIN quiz q ON s.quiz_id = q.id
                WHERE s.user_email = ?
                AND strftime('%Y-%m', s.date_attempt) = strftime('%Y-%m', 'now')
            """, (email,))
            scores = cursor.fetchall()

            if not scores:
                continue

            total = len(scores)
            avg_score = sum([row['score'] for row in scores]) / total

            rows_html = "".join(
                f"<tr><td>{row['date_attempt']}</td><td>{row['quiz_name']}</td><td>{row['score']:.2f}</td></tr>"
                for row in scores
            )

            html = f"""
                <h3>Monthly Report - {name}</h3>
                <p>Total quizzes taken: <b>{total}</b></p>
                <p>Average score: <b>{avg_score:.2f}</b></p>
                <table border="1" cellpadding="6" cellspacing="0">
                    <tr><th>Date</th><th>Quiz Name</th><th>Score</th></tr>
                    {rows_html}
                </table>
            """

            msg = Message(
                subject="Your Monthly Quiz Report",
                recipients=[email],
                html=html
            )
            mail.send(msg)

        conn.close()
