import re
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail, Message
import mysql.connector
import subprocess
from threading import Thread
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Gmail SMTP server address
app.config['MAIL_PORT'] = 587  # Port for Gmail SMTP server (587 for TLS)
app.config['MAIL_USERNAME'] = 'pk6122004@gmail.com'  # Your Gmail address
app.config['MAIL_PASSWORD'] = 'vvao wzzh zqmf jeam'  # Your Gmail password
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'pk6122004@gmail.com'
app.secret_key = 'your_secret_key'
mail = Mail(app)
USERNAME = 'admin'
PASSWORD = 'admin'

# Function to initialize database
def init_db():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='kali',
        database='teacherdb'
    )
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS teachers (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    teacher_id VARCHAR(255),
                    name VARCHAR(255),
                    email VARCHAR(255),
                    logins INT
                )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS teacher_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    teacher_id INT,
                    exam VARCHAR(255),
                    starting_user INT,
                    ending_user INT,
                    class VARCHAR(255),
                    class_status VARCHAR(10),
                    exam_user_status VARCHAR(10),
                    FOREIGN KEY (teacher_id) REFERENCES teachers(id)
                )''')
    
    conn.commit()
    conn.close()

# Initialize the database
init_db()

def execute_script(script_path, script_arguments):
    subprocess.run([script_path] + script_arguments)

# Route for entering user details
@app.route('/', methods=['GET', 'POST'])
def index():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='kali',
        database='teacherdb'
    )
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM teachers")
    teachers = cursor.fetchall()

    if request.method == 'POST':
        teacher_id = request.form['teacher']
        exam = request.form['exam']
        class_name = request.form['class']
        num_users = int(request.form['num_users'])
        a = "u"
        b = "u"

        # Read starting user number from file
        with open('last_user.txt', 'r') as file:
            starting_user = int(file.readline().strip()) + 1

        # Calculate ending user number
        ending_user = starting_user + num_users

        # Update starting user number in the file
        with open('startuser.txt', 'w') as file:
            file.write(str(ending_user))

        cursor.execute("SELECT * FROM teachers WHERE id=%s", (teacher_id,))
        teacher = cursor.fetchone()
        email = teacher[2]  # Assuming email is stored at index 2
        email = [email]
        
        if teacher:
            cursor.execute(
                "INSERT INTO teacher_data (teacher_id, exam, starting_user, ending_user, class, class_status, exam_user_status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (teacher_id, exam, starting_user, ending_user, class_name, a, b))
        else:
            return "Teacher not found"

        conn.commit()
        cursor.execute("SELECT * FROM teacher_data WHERE teacher_id=%s ORDER BY id DESC LIMIT %s", (teacher_id, num_users,))
        new_users = cursor.fetchall()
        # Close the database connection
        conn.close()

        # Execute the script asynchronously
        script_path = './script.sh'
        script_arguments = [str(num_users)]  # Convert num_users to string
        script_thread = Thread(target=execute_script, args=(script_path, script_arguments))
        script_thread.start()

        # Wait for the script execution to complete
        script_thread.join()

        # Fetch newly created users
        # Fetch newly created users
        with open('login.txt', 'r') as fp:
            login_contents = fp.read()

# Prepare email message
        msg = Message(subject='Login Details', recipients=email)  # Assuming email is stored at index 2
        msg.body = 'Please find attached login details.' 
        msg.attach('login.txt', 'text/plain', login_contents.encode('utf-8'))  # Convert string to bytes
        #mail.send(msg)

        
        return render_template('new_users.html', new_users=new_users, teacher=teacher)


    return render_template('index.html', teachers=teachers)
    
# Route for viewing login details
@app.route('/view_login', methods=['GET', 'POST'])
def view_login():
    # Read the content of login.txt
    with open('login.txt', 'r') as file:
        login_data = file.readlines()

    return render_template('view_login.html', login_data=login_data)

# Route for sending email
@app.route('/send_email', methods=['POST'])
def send_email():
    teacher_email = request.form['teacher_email']

    # Send the file to the teacher's email
    with app.open_resource('login.txt') as fp:
        msg = Message(subject='Login Details', recipients=[teacher_email])
        msg.body = 'Please find attached login details.'
        msg.attach('login.txt', 'text/plain', fp.read())
        mail.send(msg)

    return "Email sent successfully!"
'''
# Route for locking classes
@app.route('/lock_classes', methods=['GET', 'POST'])
def lock_classes():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='kali',
            database='teacherdb'
        )
        cursor = conn.cursor()

        cursor.execute("SELECT id, name FROM teachers")
        teachers = cursor.fetchall()

        if request.method == 'POST':
            teacher_id = request.form['teacher']
            cursor.execute("SELECT DISTINCT class FROM teacher_data WHERE teacher_id=%s", (teacher_id,))
            classes = [row[0] for row in cursor.fetchall()]

            cursor.execute("SELECT DISTINCT exam FROM teacher_data WHERE teacher_id=%s", (teacher_id,))
            exams = [row[0] for row in cursor.fetchall()]

            if not classes:
                return "No classes found for the selected teacher."

            return render_template('lock_classes.html', teachers=teachers, classes=classes, exams=exams)

        return render_template('lock_classes.html', teachers=teachers)
    except mysql.connector.Error as e:
        return f"Database error: {e}"
    finally:
        cursor.close()
        conn.close()
'''
'''
@app.route('/lock_classes', methods=['GET', 'POST'])
def lock_classes():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='kali',
            database='teacherdb'
        )
        cursor = conn.cursor()

        cursor.execute("SELECT id, name FROM teachers")
        teachers = cursor.fetchall()

        if request.method == 'POST':
            teacher_id = request.form['teacher']
            class_name = request.form['class']
            exam_name = request.form['exam']
            cursor.execute("SELECT starting_user, ending_user FROM teacher_data WHERE teacher_id=%s AND class=%s AND exam=%s", (teacher_id, class_name, exam_name))
            start_user, end_user = cursor.fetchone()

            # Execute the lock script
            script_path = './lock.sh'
            script_arguments = [str(start_user), str(end_user)]
            subprocess.Popen([script_path] + script_arguments)

            # Update class status to 'L'
            cursor.execute("UPDATE teacher_data SET class_status='L' WHERE teacher_id=%s AND class=%s AND exam=%s", (teacher_id, class_name, exam_name))
            conn.commit()

            return redirect(url_for('lock_classes'))  # Redirect to refresh the page

        return render_template('lock_classes.html', teachers=teachers)
    except mysql.connector.Error as e:
        return f"Database error: {e}"
    finally:
        cursor.close()
        conn.close()
'''
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'kali',
    'database': 'teacherdb'
}
@app.route('/lock_classes', methods=['GET', 'POST'])
def lock_classes():
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Fetch teachers for dropdown
        cursor.execute("SELECT id,teacher_id  FROM teachers")
        teachers = cursor.fetchall()

        # Fetch classes for dropdown
        cursor.execute("SELECT DISTINCT class FROM teacher_data")
        classes = [row[0] for row in cursor.fetchall()]

        # Fetch exams for dropdown
        cursor.execute("SELECT DISTINCT exam FROM teacher_data")
        exams = [row[0] for row in cursor.fetchall()]

        if request.method == 'POST':
            teacher_id = request.form['teacher']
            class_name = request.form['class']
            exam_name = request.form['exam']

            # Fetch starting and ending user numbers
            cursor.execute("SELECT starting_user, ending_user FROM teacher_data WHERE teacher_id=%s AND class=%s AND exam=%s", (teacher_id, class_name, exam_name))
            start_user, end_user = cursor.fetchone()

            # Execute the lock script
            script_path = './lock.sh'
            script_arguments = [str(start_user), str(end_user)]
            subprocess.Popen([script_path] + script_arguments)

            # Update class status to 'L' in the database
            cursor.execute("UPDATE teacher_data SET exam_user_status='L' WHERE teacher_id=%s AND class=%s AND exam=%s", (teacher_id, class_name, exam_name))
            conn.commit()

            return "Class locked successfully!"

        return render_template('lock_classes.html', teachers=teachers, classes=classes, exams=exams)
    except mysql.connector.Error as e:
        return f"Database error: {e}"
    finally:
        cursor.close()
        conn.close()
@app.route('/give_perm', methods=['GET', 'POST'])
def give_perm():
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(**db_config)

        cursor = conn.cursor()

        # Fetch teachers for dropdown
        cursor.execute("SELECT id,teacher_id  FROM teachers")
        teachers = cursor.fetchall()

        # Fetch classes for dropdown
        cursor.execute("SELECT DISTINCT class FROM teacher_data")
        classes = [row[0] for row in cursor.fetchall()]

        # Fetch exams for dropdown
        cursor.execute("SELECT DISTINCT exam FROM teacher_data")
        exams = [row[0] for row in cursor.fetchall()]

        if request.method == 'POST':
            teacher_ids = request.form['teacher']
            class_name = request.form['class']
            exam_name = request.form['exam']
            # Fetch starting and ending user numbers
            cursor.execute("SELECT starting_user, ending_user FROM teacher_data WHERE teacher_id=%s AND class=%s AND exam=%s", (teacher_ids, class_name, exam_name))
            
            start_user, end_user = cursor.fetchone()

            cursor.execute("SELECT teacher_id  FROM teachers WHERE id=%s", (teacher_ids[0],))

            teacher_id = cursor.fetchone()

            xx = re.search(r"'(.*?)'", str(teacher_id)).group(1)
            
# Execute the lock script
            script_path = './give_perm.sh'
            script_arguments = [str(xx),str(start_user), str(end_user)]
            subprocess.Popen([script_path] + script_arguments)

            # Update class status to 'L' in the database
            conn.commit()

            return "Class permitted successfully!"

        return render_template('give_perm.html', teachers=teachers, classes=classes, exams=exams)
    except mysql.connector.Error as e:
        return f"Database error: {e}"
    finally:
        cursor.close()
        conn.close()

@app.route('/unlock_classes', methods=['GET', 'POST'])
def unlock_classes():
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Fetch teachers for dropdown

        cursor.execute("SELECT id,teacher_id  FROM teachers")
        teachers = cursor.fetchall()

        # Fetch classes for dropdown
        cursor.execute("SELECT DISTINCT class FROM teacher_data")
        classes = [row[0] for row in cursor.fetchall()]

        # Fetch exams for dropdown
        cursor.execute("SELECT DISTINCT exam FROM teacher_data")
        exams = [row[0] for row in cursor.fetchall()]

        if request.method == 'POST':
            teacher_id = request.form['teacher']
            class_name = request.form['class']
            exam_name = request.form['exam']

            # Fetch starting and ending user numbers
            cursor.execute("SELECT starting_user, ending_user FROM teacher_data WHERE teacher_id=%s AND class=%s AND exam=%s", (teacher_id, class_name, exam_name))
            start_user, end_user = cursor.fetchone()

            # Execute the lock script
            script_path = './unlock.sh'
            script_arguments = [str(start_user), str(end_user)]
            subprocess.Popen([script_path] + script_arguments)

            # Update class status to 'L' in the database
            cursor.execute("UPDATE teacher_data SET exam_user_status='U' WHERE teacher_id=%s AND class=%s AND exam=%s", (teacher_id, class_name, exam_name))
            conn.commit()

            return "Class unlocked successfully!"

        return render_template('unlock_classes.html', teachers=teachers, classes=classes, exams=exams)
    except mysql.connector.Error as e:
        return f"Database error: {e}"
    finally:
        cursor.close()
        conn.close()

@app.route('/create_teacher', methods=['GET', 'POST'])
def create_teacher():
    conn = None
    cursor = None
    try:
        if request.method == 'POST':
            teacher_id = request.form['teacher_id']  # New input field for teacher_id
            name = request.form['name']
            email = request.form['email']
            logins = int(request.form['logins'])

            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='kali',
                database='teacherdb'
            )
            cursor = conn.cursor()

            cursor.execute("INSERT INTO teachers (teacher_id, name, email, logins) VALUES (%s, %s, %s, %s)",
                           (teacher_id, name, email, logins))  # Insert teacher_id
            conn.commit()

            # Fetch updated list of teachers
            cursor.execute("SELECT * FROM teachers")
            teachers = cursor.fetchall()

            return render_template('index.html', teachers=teachers)

        return render_template('create_teacher.html')
    except mysql.connector.Error as e:
        return f"Database error: {e}"
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/show_classes', methods=['GET'])
def show_classes():
    try:
        # Connect to the database
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='kali',
            database='teacherdb'
        )
        cursor = conn.cursor()

        # Fetch teacher data
        cursor.execute("SELECT * FROM teachers")
        teachers = cursor.fetchall()

        # Close the database connection
        cursor.close()
        conn.close()

        # Render the template with teacher data
        return render_template('show_classes.html', teachers=teachers)
    except mysql.connector.Error as e:
        return f"Database error: {e}"

# Route for logging in
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['username'] = username  # Store the username in the session
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

# Route for logging out
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove the username from the session if it exists
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
