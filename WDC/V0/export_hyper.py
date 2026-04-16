import pyodbc
import pandas as pd
import pantab
from tableauhyperapi import TableName

# --- BIẾN TOÀN CỤC ---
# Bạn có thể dễ dàng thay đổi tên file tại đây một lần duy nhất
OUTPUT_FILE = "database_export.hyper"

# Cấu hình kết nối MS SQL Server
conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=TRANTUAN;' 
    'DATABASE=dat207_sample;' 
    'Trusted_Connection=yes;'
)

def get_available_tables():
    """Truy vấn danh sách bảng từ Database"""
    try:
        conn = pyodbc.connect(conn_str)
        query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
        tables_df = pd.read_sql(query, conn)
        conn.close()
        return tables_df['TABLE_NAME'].tolist()
    except Exception as e:
        print(f"Lỗi kết nối: {e}")
        return []

def export_multiple_tables_to_hyper(selected_tables):
    """
    Sử dụng biến toàn cục OUTPUT_FILE để xuất dữ liệu
    """
    # Khai báo sử dụng biến toàn cục
    global OUTPUT_FILE 

    if not selected_tables:
        print("Không có bảng nào được chọn.")
        return

    conn = pyodbc.connect(conn_str)
    data_dict = {}

    print(f"\n--- Đang bắt đầu quá trình trích xuất ---")
    
    for table in selected_tables:
        try:
            print(f"Đang đọc: {table}")
            query = f"SELECT * FROM {table}"
            df = pd.read_sql(query, conn)
            data_dict[TableName("Extract", table)] = df
        except Exception as e:
            print(f"Lỗi tại bảng {table}: {e}")

    try:
        # Sử dụng giá trị từ biến toàn cục làm tên file đầu ra
        pantab.frames_to_hyper(data_dict, OUTPUT_FILE)
        print(f"\n[THÀNH CÔNG] Dữ liệu đã được cập nhật vào file: {OUTPUT_FILE}")
    except Exception as e:
        print(f"Lỗi khi ghi file: {e}")
    finally:
        conn.close()

# --- LUỒNG CHẠY CHƯƠNG TRÌNH ---
if __name__ == "__main__":
    all_tables = get_available_tables()
    
    if all_tables:
        print("Danh sách bảng hiện có:")
        for index, table in enumerate(all_tables, start=1):
            print(f"{index}. {table}")

        user_choice = input("\nNhập số thứ tự bảng bạn muốn chọn (có thể nhập nhiều số, cách nhau bởi dấu phẩy): ")
        selected_indexes = [item.strip() for item in user_choice.split(',') if item.strip().isdigit()]
        selected_list = []

        for idx_str in selected_indexes:
            idx = int(idx_str)
            if 1 <= idx <= len(all_tables):
                selected_list.append(all_tables[idx - 1])
            else:
                print(f"Số {idx} không hợp lệ và sẽ bị bỏ qua.")

        if selected_list:
            export_multiple_tables_to_hyper(selected_list)
        else:
            print("Không có bảng hợp lệ được chọn.")