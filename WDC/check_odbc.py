import pyodbc
drivers = [d for d in pyodbc.drivers() if 'SQL Server' in d]
print("Các Driver SQL Server khả dụng trên máy bạn là:")
for d in drivers:
    print(f"- {d}")
