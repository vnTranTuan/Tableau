import pyodbc
import pandas as pd
import os

# --- CẤU HÌNH KẾT NỐI ---
# Nếu dùng Windows Authentication (Trusted_Connection), hãy giữ nguyên
# Nếu dùng tài khoản SQL, hãy thêm UID=username;PWD=password; vào chuỗi
conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=TRANTUAN;' 
    'DATABASE=dat207_sample;' 
    'Trusted_Connection=yes;'
)
OUTPUT_FOLDER="export_data"

def get_available_tables():
    """Liệt kê các bảng trong database"""
    try:
        conn = pyodbc.connect(conn_str)
        query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
        tables_df = pd.read_sql(query, conn)
        conn.close()
        return tables_df['TABLE_NAME'].tolist()
    except Exception as e:
        print(f"Lỗi kết nối: {e}")
        return []

def export_to_csv(selected_tables):
    """Chọn bảng và xuất dữ liệu ra CSV"""
    if not selected_tables:
        print("Không có bảng nào được chọn.")
        return

    conn = pyodbc.connect(conn_str)
    
    # Tạo thư mục 'exports' nếu chưa có để chứa file CSV
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    for table in selected_tables:
        try:
            print(f"Đang trích xuất dữ liệu từ bảng: {table}...")
            query = f"SELECT * FROM {table}"
            df = pd.read_sql(query, conn)
            
            # Xuất file CSV (Sử dụng utf-8-sig để tránh lỗi font tiếng Việt nếu có)
            file_path = f"{OUTPUT_FOLDER}/{table}.csv"
            df.to_csv(file_path, index=False, encoding='utf-8-sig')
            print(f"-> Đã lưu file: {file_path}")
        except Exception as e:
            print(f"Lỗi khi trích xuất bảng {table}: {e}")

    conn.close()
    print("\nQuá trình hoàn tất!")

# --- LUỒNG THỰC THI ---
if __name__ == "__main__":
    # 1. Liệt kê danh sách bảng
    all_tables = get_available_tables()
    
    if all_tables:
        print("\n=== DANH SÁCH BẢNG TRONG DATABASE ===")
        for i, table in enumerate(all_tables):
            print(f"{i+1}. {table}")
        
        # 2. Người dùng chọn bảng
        print("\nNhập số thứ tự các bảng muốn chọn (cách nhau bằng dấu phẩy), hoặc 'all' để chọn tất cả:")
        user_input = input("Lựa chọn của bạn: ").strip().lower()
        
        selected_list = []
        if user_input == 'all':
            selected_list = all_tables
        else:
            try:
                indices = [int(x.strip()) - 1 for x in user_input.split(',')]
                selected_list = [all_tables[i] for i in indices if 0 <= i < len(all_tables)]
            except ValueError:
                print("Lỗi: Vui lòng chỉ nhập số hoặc 'all'.")

        # 3. Tiến hành xuất dữ liệu
        if selected_list:
            print(f"\nCác bảng đã chọn: {selected_list}")
            export_to_csv(selected_list)
    else:
        print("Không tìm thấy bảng nào hoặc lỗi kết nối.")