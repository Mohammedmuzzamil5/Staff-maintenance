import tkinter as tk
from tkinter import ttk
from backend import TrainingDB

class TrainingRequestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Request System")

        self.training_db = TrainingDB()


        tk.Label(self.root, text="Staff Name:").grid(row=0, column=0, padx=5, pady=5)
        self.staff_name_entry = tk.Entry(self.root)
        self.staff_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Training Type:").grid(row=1, column=0, padx=5, pady=5)
        self.training_type_entry = tk.Entry(self.root)
        self.training_type_entry.grid(row=1, column=1, padx=5, pady=5)

        self.request_button = tk.Button(self.root, text="Request Training", command=self.request_training)
        self.request_button.grid(row=2, column=0, columnspan=2, pady=10)


        self.tree = ttk.Treeview(self.root, columns=('ID', 'Staff Name', 'Training Type', 'Status'))
        self.tree.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.tree.heading('#0', text='ID')
        self.tree.heading('#1', text='Staff Name')
        self.tree.heading('#2', text='Training Type')
        self.tree.heading('#3', text='Status')


        self.approve_button = tk.Button(self.root, text="Approve", command=self.approve_request)
        self.approve_button.grid(row=4, column=0, pady=5)

        self.deny_button = tk.Button(self.root, text="Deny", command=self.deny_request)
        self.deny_button.grid(row=4, column=1, pady=5)

        self.update_treeview()

    def request_training(self):
        staff_name = self.staff_name_entry.get()
        training_type = self.training_type_entry.get()

        if staff_name and training_type:
            self.training_db.add_training_request(staff_name, training_type)
            self.update_treeview()


            self.staff_name_entry.delete(0, tk.END)
            self.training_type_entry.delete(0, tk.END)

    def update_treeview(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        training_data = self.training_db.get_all_training_requests()

        for row in training_data:
            self.tree.insert('', 'end', values=row)

    def approve_request(self):
        selected_item = self.tree.selection()
        if selected_item:
            request_id = self.tree.item(selected_item, 'values')[0]
            self.training_db.update_request_status(request_id, 'Approved')
            self.update_treeview()

    def deny_request(self):
        selected_item = self.tree.selection()
        if selected_item:
            request_id = self.tree.item(selected_item, 'values')[0]
            self.training_db.update_request_status(request_id, 'Denied')
            self.update_treeview()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingRequestApp(root)
    app.run()
    app.training_db.close_connection()
