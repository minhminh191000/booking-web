import json
import pandas as pd

# Đọc nội dung từ tệp .txt
with open('products_detail.txt', 'r') as file:
    data = file.read()

# Phân tích dữ liệu JSON
# Phân tách các đối tượng JSON thành các phần tử riêng lẻ
json_data_list = data.strip().split('\n')

# Tạo DataFrame từ dữ liệu JSON
data_list = [json.loads(item) for item in json_data_list]
df = pd.DataFrame(data_list)
df['price'] = df['price'].astype(str).str.replace('.', '', regex=True)
# Lưu DataFrame vào tệp Excel
df.to_excel('products_detail.xlsx', index=False)