# ShopEasy - E-Commerce Website (DBMS Mini Project)

A basic working e-commerce website built with **Python Flask + MySQL + HTML/CSS**.

## Folder structure
```
ecommerce_project/
|-- README.md                  <- you are here (how to run)
|-- requirements.txt           <- Python libraries needed
|-- database/
|   |-- schema.sql             <- RUN THIS: the 6 tables + sample data (used by website)
|   |-- lab_script_original.sql<- your original SQL lab script (with comments)
|   |-- queries.sql            <- extra JOIN / GROUP BY / subquery queries for demo
|-- backend/
|   |-- app.py                 <- all website logic (routes)
|   |-- db.py                  <- helper functions to talk to MySQL
|   |-- config.py              <- DB password and settings  (EDIT THIS)
|-- frontend/
|   |-- templates/             <- HTML pages
|   |-- static/style.css       <- design / colours
|-- docs/
    |-- HOW_IT_WORKS.md        <- explanation of everything (read before presenting)
    |-- er_diagram.png         <- ER diagram picture
    |-- Project_Report.docx    <- editable project report (fill your name/reg no.)
    |-- Project_Report.pdf     <- same report as PDF
```

## How to run (Windows / Mac / Linux)

1. **Install** Python 3.9+ and MySQL Server 8 (with MySQL Workbench). 
2. **Create the database**: open MySQL Workbench -> File -> Open SQL Script -> `database/schema.sql` -> click the lightning-bolt icon.
   (Or in terminal: `mysql -u root -p < database/schema.sql`)
3. **Install libraries** (in a terminal inside the project folder):
   ```
   pip install -r requirements.txt
   ```
4. **Edit `backend/config.py`** and put YOUR MySQL password in `"password"`.
5. **Start the website**:
   ```
   cd backend
   python app.py
   ```
6. Open **http://127.0.0.1:5000** in your browser.

## Demo logins
| Username   | Password     |
|------------|--------------|
| arjun_raj  | password123  |
| priya_s    | password123  |
| amit_k     | password123  |

(You can also click **Register** to create a new account.)

## Common problems
| Problem | Fix |
|---|---|
| `Access denied for user 'root'` | Wrong password in `backend/config.py` |
| `Unknown database 'ecommerce'` | You have not run `schema.sql` yet |
| `No module named flask` / `mysql` | Run `pip install -r requirements.txt` again |
| `Can't connect to MySQL server` | MySQL service is not running - start it from Services (Windows) or MySQL Workbench |
| Port 5000 already used | Change last line of app.py to `app.run(debug=True, port=5001)` |
