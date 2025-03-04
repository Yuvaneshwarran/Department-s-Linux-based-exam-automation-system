# Department Exam Automation System

## 🖥️ Project Overview

The Department Exam Automation System is a robust, Linux-based application designed to streamline exam account management and administration. Built with modern web technologies, this system provides an efficient solution for creating, managing, and monitoring student exam accounts.

## ✨ Key Features

- **Automated Exam Account Creation**: Seamlessly generate unique exam accounts for students
- **Email Notification System**: Automatically send exam account details to teachers
- **User-Friendly Web Interface**: Intuitive UI for teachers and administrators
- **Secure Account Management**: Granular permissions and account controls
- **Logging and Tracking**: Comprehensive user creation and system logs

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Scripting**: Bash
- **Database**: MySQL
- **Frontend**: HTML/CSS
- **Deployment**: Linux Environment

## 📦 Project Structure

```
exam-automation/
│
├── bin/                # Executable scripts
├── lib/                # Library files
├── templates/          # HTML templates
│   ├── login.html
│   ├── create_teacher.html
│   ├── show_users.html
│   └── ...
│
├── app.py              # Main Flask application
├── database.db         # SQLite database
├── scripts/            # Utility bash scripts
│   ├── user_creation.sh
│   ├── give_perm.sh
│   └── lock_classes.sh
└── README.md
```

## 🚀 Installation and Setup

### Prerequisites

- Linux Operating System
- Python 3.8+
- MySQL
- Flask
- Bash

### Installation Steps

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/exam-automation.git
   cd exam-automation
   ```

2. Create a virtual environment
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Configure database
   ```bash
   python setup_database.py
   ```

5. Run the application
   ```bash
   python app.py
   ```

## 🔐 Security Features

- Secure user authentication
- Role-based access control
- Automated account locking mechanisms
- Encrypted communication
- Comprehensive logging system

## 📋 Usage Guide

### For Administrators
- Create and manage teacher accounts
- Lock/unlock exam classes
- View and manage user permissions

### For Teachers
- Access student exam accounts
- Send exam account details via email
- Monitor exam account status

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🐛 Known Issues and Troubleshooting

- Ensure proper permissions for bash scripts
- Check email configuration settings
- Verify database connection parameters

## 📞 Contact

Your Name - yuvaneshwarran@gmail.com

Project Link: [https://github.com/yuvaneshwarran/exam-automation](https://github.com/yuvaneshwarran/exam-automation)