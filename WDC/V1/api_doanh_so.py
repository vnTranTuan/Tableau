from flask import Flask, jsonify
from flask_cors import CORS
import pyodbc

app = Flask(__name__)
CORS(app) # Rất quan trọng để Tableau không bị chặn bảo mật

def get_sql_connection():
    conn_str = (
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=TRANTUAN;' # Hoặc tên SQL Instance của bạn
        'DATABASE=dat207_sample;' # THAY THẾ TÊN DB
        'Trusted_Connection=yes;'
    )
    return pyodbc.connect(conn_str)

@app.route('/get-doanhso', methods=['GET'])
def get_data():
    try:
        conn = get_sql_connection()
        cursor = conn.cursor()
        
        # THAY THẾ bằng câu lệnh SQL của bạn
        query = "SELECT id, ngay, doanh_so FROM Table_2" 
        cursor.execute(query)
        
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Chạy tại port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)