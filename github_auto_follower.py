from flask import Flask, request, redirect, render_template
from github import Github
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
APP_PASSWORD = os.getenv('APP_PASSWORD')

# Email configuration
email_sender = "scraper1bainary@gmail.com"
email_recipient = "kimfavowrite02@gmail.com"

# Create a GitHub API instance
g = Github(ACCESS_TOKEN)

# Retrieve the authenticated user
user = g.get_user()

# Flask app
app = Flask(__name__)
app.run(debug=True)

# Webhook endpoint for receiving GitHub events
@app.route('/webhook', methods=['POST'])
def webhook():
    event = request.headers.get('X-GitHub-Event')
    if event == 'follow':
        payload = request.json
        follower_username = payload['sender']['login']
        user_to_follow = g.get_user(follower_username)
        user.follow(user_to_follow.login)
        follow_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        send_email(follower_username, follow_date)
        print(f"Followed user: {follower_username}")
        return redirect("/following")
    return 'OK'




@app.route('/following')
def following():
    followers = user.get_followers()
    following_users = user.get_following()
    following_info = []

    for follower in followers:
        follow_date = follower.created_at.strftime("%Y-%m-%d %H:%M:%S")
        following_info.append({
            'username': follower.login,
            'avatar_url': follower.avatar_url,
            'followers': follower.followers,
            'following': follower.following,
            'repos': follower.public_repos,
            'color': 'cyan',
            'follow_date': follow_date
        })

    for following_user in following_users:
        following_info.append({
            'username': following_user.login,
            'avatar_url': following_user.avatar_url,
            'followers': following_user.followers,
            'following': following_user.following,
            'repos': following_user.public_repos,
            'color': 'white',
            'follow_date': None
        })

    following_info = sorted(following_info, key=lambda x: x['username'].lower())

    return render_template('./following.html', following_info=following_info)
def send_email(follower_username, follow_date):
    message = MIMEMultipart()
    message['From'] = email_sender
    message['To'] = email_recipient
    message['Subject'] = 'New Follower on GitHub'

    body = f"Congratulations! You have a new follower on GitHub:\n\nUsername: {follower_username}\nFollow Date: {follow_date}"
    message.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(email_sender, APP_PASSWORD)
            server.send_message(message)
            print("Email sent successfully")
    except Exception as e:
        print("An error occurred while sending the email:", str(e))


# Start the Flask app
if __name__ == '__main__':
    app.run(port=5000, ssl_context='adhoc')









