# 📊 Expense Tracker and Insights WebApp

## 🚀 Overview

Expense Tracker is a web application I built using Streamlit and MongoDB, allowing users to track their expenses, view insights, and manage their budget. Users can log in or create a new account, add expenses with details such as category, type, amount, and notes, view and sort expenses, edit or delete expenses, and visualize their spending habits.

## ✨ Features

- **User authentication:** 👤 Login or create a new account to access the expense tracker.
- **Add expenses:** 💸 Record expenses with details like category, type, amount, and notes.
- **View expenses:** 📅 See all expenses in a tabular format and sort them in ascending or descending order by category or type.
- **Edit or delete expenses:** ✏️ Modify or remove existing expenses as needed.
- **View insights:** 📈 Visualize overall expenses, expenses by day, by category, and by type.
- **Budget report:** 💰 Input salary to get a report on remaining budget.
- **Containerized deployment:** 🐳 Docker used for containerization, deployed on Azure Web App hosting service.
- **Live at:**
  ```bash
  https://wheremymoney.azurewebsites.net/
  ```

## ⚙️ Installation and Usage

To run the Expense Tracker locally, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/SmridhVarma/Expense-Tracker-and-Insights-System.git
   ```
2. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```
3. **Set Up MongoDB:**
   Create a MongoDB database and configure the connection settings in config.py

4. **Run the application:**

   ```bash
   streamlit run app.py
   ```

5. **Access the application:**
   Open your web browser and go to
   ```bash
   http://localhost:8501
   ```

## 🛠️ Future Enhancements

- Implement a budgeting system to help users manage their expenses more effectively.
- Improve access speed and performance for a smoother user experience.
- Add additional features based on user feedback and requirements.
