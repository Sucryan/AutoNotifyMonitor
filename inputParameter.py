import tkinter as tk
from tkinter import messagebox
import json
import os

# abs path
current_dir = os.path.dirname(os.path.abspath(__file__))
# Parameter Path
ParaPath = os.path.join(current_dir, 'Par.txt')

class DataInputApp:
    def __init__(self, master):
        self.master = master
        master.title("資料輸入應用程式")
        master.geometry("300x250")

        # 讀取現有數據
        self.existing_data = self.load_existing_data() 
        
        # 創建和放置用戶名輸入框
        self.username_label = tk.Label(master, text="使用者/信箱:")
        self.username_label.pack()
        self.username_entry = tk.Entry(master)
        self.username_entry.pack()
        self.username_entry.insert(0, self.existing_data.get("username", ""))

        # 創建和放置密碼輸入框
        self.password_label = tk.Label(master, text="密碼:")
        self.password_label.pack()
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack()
        self.password_entry.insert(0, self.existing_data.get("password", ""))

        # 創建和放置 token 輸入框
        self.token_label = tk.Label(master, text="Token:")
        self.token_label.pack()
        self.token_entry = tk.Entry(master)
        self.token_entry.pack()
        self.token_entry.insert(0, self.existing_data.get("token", ""))

        # 搜尋訊息
        self.searchItem_label = tk.Label(master, text="搜尋項目:")
        self.searchItem_label.pack()
        self.searchItem_entry = tk.Entry(master)
        self.searchItem_entry.pack()
        self.searchItem_entry.insert(0, self.existing_data.get("searchItem", ""))

        # 創建和放置保存按鈕
        self.save_button = tk.Button(master, text="儲存", command=self.save_data)
        self.save_button.pack(pady=10)

    def load_existing_data(self):
        try:
            with open(ParaPath, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            messagebox.showwarning("警告", "無法讀取現有數據，將使用空白數據。")
            return {}

    def save_data(self):
        new_data = {}
        for key, entry in [("username", self.username_entry),
                           ("password", self.password_entry),
                           ("token", self.token_entry),
                           ("searchItem", self.searchItem_entry)]:
            new_value = entry.get()
            if new_value:  # 如果輸入不為空
                new_data[key] = new_value
            elif key in self.existing_data:  # 如果輸入為空但存在舊數據
                new_data[key] = self.existing_data[key]

        try:
            with open(ParaPath, "w") as file:
                json.dump(new_data, file)
            messagebox.showinfo("成功", "資料已成功儲存")
        except Exception as e:
            messagebox.showerror("錯誤", f"儲存資料時發生錯誤: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataInputApp(root)
    root.mainloop()