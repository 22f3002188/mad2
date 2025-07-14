# tasks.py
from celery import current_app as celery
from flask_mail import Mail, Message
from models import get_connection
from app import app  
from io import StringIO  
import csv 

mail = Mail(app)


#------------------------------------DAILY REMINDER-----------------------------
@celery.task(name='tasks.send_daily_reminders')
def send_daily_reminders():
    with app.app_context():  
        conn = get_connection()
        cursor = conn.cursor()

        
        cursor.execute("SELECT email, full_name FROM users WHERE role = 'user'")
        users = cursor.fetchall()

        print(f"[Daily Reminder] Found {len(users)} users")

        for user in users:
            email = user['email']
            name = user['full_name']

            msg = Message(
                subject="Daily Quiz Reminder",
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


#------------------------MONTHLY REMINDER------------------------------------
@celery.task(name='tasks.send_monthly_report')
def send_monthly_report():
    with app.app_context():  
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


#-------------------------------------CSV DOWNLOAD-------------------------------
@celery.task(name='tasks.export_user_csv_and_email')
def export_user_csv_and_email(user_email):
    with app.app_context():  
        conn = get_connection()
        cursor = conn.cursor()

      
        cursor.execute("SELECT full_name FROM users WHERE email = ?", (user_email,))
        row = cursor.fetchone()
        if not row:
            print(f"No user found for {user_email}")
            return

        full_name = row['full_name']

       
        cursor.execute("""
            SELECT q.id AS quiz_id, q.chapter_id, s.date_attempt, s.score
            FROM score s
            JOIN quiz q ON s.quiz_id = q.id
            WHERE s.user_email = ?
        """, (user_email,))
        rows = cursor.fetchall()

        if not rows:
            print(f"No quiz data found for {user_email}")
            return

        
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['quiz_id', 'chapter_id', 'date_of_quiz', 'score'])

        for row in rows:
            writer.writerow([
                row['quiz_id'], row['chapter_id'], row['date_attempt'],
                row['score'] or ''
            ])

        csv_data = output.getvalue()
        output.close()

       
        msg = Message(
            subject="Your Quiz Export",
            recipients=[user_email],
            body=f"Hi {full_name},\n\nAttached is your quiz export CSV from Quiz Nation.",
        )
        msg.attach("quiz_export.csv", "text/csv", csv_data)
        mail.send(msg)
        print(f"CSV sent to {user_email}")
        conn.close()