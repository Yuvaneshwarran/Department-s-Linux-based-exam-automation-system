import smtplib
from email.message import EmailMessage

# SMTP server configuration
smtp_server = 'smtp.gmail.com'
smtp_port = 587  # Port for TLS
sender_email = 'pk6122004@gmail.com'  # Your Gmail address
receiver_email = 'recipient@example.com'  # Recipient email address
password = 'jvsv wcxd cphz yquw'  # Your Gmail password

# Initialize server variable
server = None

# Create a message object
msg = EmailMessage()
msg['Subject'] = 'Test Email'
msg['From'] = sender_email
msg['To'] = receiver_email
msg.set_content('This is a test email sent using Python.')

try:
    # Connect to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Enable TLS encryption

    # Login to the SMTP server
    server.login(sender_email, password)

    # Send the email
    server.send_message(msg)

    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email. Error: {str(e)}")
finally:
    # Close the connection to the SMTP server
    if server is not None:
        server.quit()
