from app import app, celery, get_connection
from flask_mail import Mail, Message

# Mail config (BEFORE Mail(app))
app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 1025
app.config['MAIL_DEFAULT_SENDER'] = 'admin@gmail.com'

mail = Mail(app)

# === Real Daily Reminder Task ===
@celery.task
def send_daily_reminders():
    with app.app_context():
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT DISTINCT u.email, u.full_name 
            FROM users u
            LEFT JOIN score s ON u.email = s.user_email
            WHERE u.role = 'user' 
            AND (
                s.date_attempt IS NULL OR 
                s.date_attempt < date('now', '-2 day')
            )
        """)
        inactive_users = cursor.fetchall()

        cursor.execute("""
            SELECT quiz_name, date_of_quiz FROM quiz 
            WHERE date_of_quiz = date('now')
        """)
        new_quizzes = cursor.fetchall()

        quiz_list_html = ''.join(
            f"<li>{q['quiz_name']} - {q['date_of_quiz']}</li>"
            for q in new_quizzes
        ) or "<li>No new quizzes today</li>"

        for user in inactive_users:
            msg = Message(
                subject="Quiz Reminder!",
                recipients=[user["email"]],
                html=f"""
                    <p>Hello {user['full_name']},</p>
                    <p>We noticed you haven't taken any quizzes recently.</p>
                    <p>New quizzes today:</p>
                    <ul>{quiz_list_html}</ul>
                    <p>Visit now and give them a try!</p>
                """
            )
            mail.send(msg)

        conn.close()
        print(f"Sent reminders to {len(inactive_users)} inactive users.")

# === MONTHLY ACTIVITY REPORT TASK ===
@celery.task
def send_monthly_report():
    with app.app_context():
        conn = get_connection()
        cursor = conn.cursor()

        # Get all users
        cursor.execute("SELECT email, full_name FROM users WHERE role = 'user'")
        users = cursor.fetchall()

        for user in users:
            email = user['email']
            name = user['full_name']

            # Get user's quiz activity this month
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
            print(f"Sent monthly report to {email}")

        conn.close()        
