import pyodbc
import pandas as pd
import pantab
from tableauhyperapi import TableName

# 1. Cấu hình kết nối MS SQL Server
# Thay đổi các thông số Server và Database cho đúng với máy của bạn
conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=TRANTUAN;' 
    'DATABASE=dat207_sample;' 
    'Trusted_Connection=yes;'
)
OUTPUT_FILE="DuLieu_Tu_MSSQL.hyper"

def get_available_tables():
    """Lấy danh sách tất cả các bảng hiện có trong database"""
    try:
        conn = pyodbc.connect(conn_str)
        query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
        tables_df = pd.read_sql(query, conn)
        conn.close()
        return tables_df['TABLE_NAME'].tolist()
    except Exception as e:
        print(f"Lỗi khi kết nối SQL Server: {e}")
        return []

# def export_multiple_tables_to_hyper(selected_tables, output_file="combined_data.hyper"):
#     """
#     Yêu cầu 2 & 3: Kết nối nhiều bảng và xuất ra file Hyper để reload vào Tableau
#     """
#     if not selected_tables:
#         print("Không có bảng nào được chọn.")
#         return

#     conn = pyodbc.connect(conn_str)
#     data_dict = {}

#     print(f"\nĐang tiến hành trích xuất {len(selected_tables)} bảng...")
    
#     for table in selected_tables:
#         try:
#             print(f"-> Đang đọc dữ liệu từ bảng: {table}")
#             query = f"SELECT * FROM {table}"
#             df = pd.read_sql(query, conn)
            
#             # Đưa vào dictionary để pantab tạo các table riêng biệt trong 1 file .hyper
#             # TableName("Schema", "Table") -> Mặc định Tableau dùng schema là 'Extract'
#             data_dict[TableName("Extract", table)] = df
#         except Exception as e:
#             print(f"Lỗi khi đọc bảng {table}: {e}")

#     # Ghi đè file Hyper cũ để cập nhật dữ liệu mới (Reload data)
#     pantab.frame_to_hyper(data_dict, output_file)
#     conn.close()
#     print(f"\nThành công! File '{output_file}' đã sẵn sàng để sử dụng trong Tableau Public.")

def export_multiple_tables_to_hyper(selected_tables, output_file=OUTPUT_FILE):
    if not selected_tables:
        print("Không có bảng nào được chọn.")
        return

    conn = pyodbc.connect(conn_str)
    data_dict = {}

    print(f"\nĐang tiến hành trích xuất {len(selected_tables)} bảng...")
    
    for table in selected_tables:
        try:
            print(f"-> Đang đọc dữ liệu từ bảng: {table}")
            query = f"SELECT * FROM {table}"
            df = pd.read_sql(query, conn)
            
            # Key của dict phải là TableName hoặc chuỗi định dạng "schema.table"
            # Trong Tableau Public, chúng ta thường dùng schema mặc định là 'Extract'
            target_table = TableName("Extract", table)
            data_dict[target_table] = df
            
        except Exception as e:
            print(f"Lỗi khi đọc bảng {table}: {e}")

    try:
        # QUAN TRỌNG: Dùng frames_to_hyper (có 's') khi truyền vào một Dictionary
        pantab.frames_to_hyper(data_dict, output_file)
        print(f"\nThành công! Đã ghi {len(data_dict)} bảng vào file '{output_file}'.")
    except Exception as e:
        print(f"Lỗi khi ghi file Hyper: {e}")
    finally:
        conn.close()

# --- CHƯƠNG TRÌNH CHÍNH ---
if __name__ == "__main__":
    # Bước 1: Liệt kê các bảng (Yêu cầu 1)
    all_tables = get_available_tables()
    
    if all_tables:
        print("Danh sách các bảng có trong Database của bạn:")
        for i, table in enumerate(all_tables):
            print(f"{i+1}. {table}")
        
        # Bước 2: Cho phép người dùng chọn nhiều bảng (Yêu cầu 2)
        print("\nNhập số thứ tự các bảng bạn muốn chọn (cách nhau bởi dấu phẩy), hoặc gõ 'all' để chọn tất cả:")
        user_input = input("Lựa chọn của bạn: ").strip().lower()
        
        selected_list = []
        if user_input == 'all':
            selected_list = all_tables
        else:
            try:
                indices = [int(x.strip()) - 1 for x in user_input.split(',')]
                selected_list = [all_tables[i] for i in indices if 0 <= i < len(all_tables)]
            except:
                print("Lựa chọn không hợp lệ.")

        # Bước 3: Xuất dữ liệu (Hỗ trợ reload bằng cách chạy lại script này)
        if selected_list:
            print(f"\nBảng đã chọn: {selected_list}")
            export_multiple_tables_to_hyper(selected_list)