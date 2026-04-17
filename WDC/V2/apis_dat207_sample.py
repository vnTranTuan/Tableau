from flask import Flask, jsonify
from flask_cors import CORS
import pyodbc
import socket

app = Flask(__name__)
CORS(app) # Cho phép Tableau truy cập API từ trình duyệt

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

# # Cấu hình kết nối SQL Server, với internet IP và port
def get_sql_connection():
    # Các thông số cần thay đổi
    # remote_ip = '123.456.78.90' # IP Internet của server
    remote_ip = '127.0.0.1' # IP local của server
    port = '1433'                # Port mặc định của SQL Server là 1433
    database = 'dat207_sample'
    user = 'test'       # Tài khoản SQL Server (ví dụ: sa)
    password = 'p@ssw0rd'
    
    conn_str = (
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={remote_ip},{port};'
        f'DATABASE={database};'
        f'UID={user};'
        f'PWD={password};'
    )
    return pyodbc.connect(conn_str)

# # Cấu hình kết nối SQL Server
# def get_sql_connection():
#     conn_str = (
#         'DRIVER={ODBC Driver 17 for SQL Server};'
#         'SERVER=TRANTUAN;' # Thay bằng tên Server của bạn
#         'DATABASE=dat207_sample;' # Thay bằng tên Database của bạn
#         'Trusted_Connection=yes;'
#     )
#     return pyodbc.connect(conn_str)

def fetch_data(query):
    try:
        conn = get_sql_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        
        # Lấy tên cột
        columns = [column[0] for column in cursor.description]
        # Chuyển đổi dữ liệu sang dạng danh sách các Dictionary
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return results
    except Exception as e:
        return {"error": str(e)}

# --- TẠO CÁC API RIÊNG BIỆT ---

@app.route('/api/V2/sanpham', methods=['GET'])
def get_sanpham():
    data = fetch_data("SELECT ID, ma_san_pham, ten_san_pham, don_gia FROM tbl_SAN_PHAM")
    print(data)
    return jsonify(data)

@app.route('/api/V2/doanhso', methods=['GET'])
def get_doanhso():
    data = fetch_data("SELECT ID, ngay, doanh_so FROM tbl_DOANH_SO")
    return jsonify(data)

@app.route('/api/V2/khachhang', methods=['GET'])
def get_khachhang():
    data = fetch_data("SELECT ID, ma_khach_hang, ten_khach_hang, dia_chi FROM tbl_KHACH_HANG")
    return jsonify(data)

@app.route('/api/V2/donhang', methods=['GET'])
def get_orders():
    data = fetch_data("SELECT ID, ma_don_hang, so_luong, ma_san_pham, khuyen_mai FROM tbl_DON_HANG")
    return jsonify(data)

if __name__ == '__main__':
    # Chạy Server tại port 5000
    print(f"API Server đang chạy tại http://{get_local_ip()}:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)