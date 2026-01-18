import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from analysis import DataAnalyzer
from visualizer import Visualizer

class DataAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Analytics: Customer & Business")
        self.root.geometry("1100x700")
        self.root.configure(bg="#f0f2f5")

        self.analyzer = DataAnalyzer()
        self.visualizer = Visualizer()
        self.file_path = None

        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#2c3e50", height=60)
        header.pack(fill="x")
        tk.Label(header, text="Data Analytics Dashboard", fg="white", bg="#2c3e50", 
                 font=("Helvetica", 18, "bold")).pack(pady=10)

        # Main Layout: Sidebar and Content
        self.sidebar = tk.Frame(self.root, bg="#34495e", width=200)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content_area = tk.Frame(self.root, bg="#f0f2f5")
        self.content_area.pack(side="right", fill="both", expand=True)

        # Sidebar Buttons
        btn_style = {"bg": "#34495e", "fg": "white", "font": ("Helvetica", 11), 
                     "bd": 0, "padx": 20, "pady": 10, "anchor": "w", 
                     "activebackground": "#1abc9c", "activeforeground": "white"}
        
        tk.Button(self.sidebar, text="Upload Data", command=self.upload_data, **btn_style).pack(fill="x")
        tk.Button(self.sidebar, text="Data Summary", command=self.show_summary, **btn_style).pack(fill="x")
        tk.Button(self.sidebar, text="Visualizations", command=self.show_visualizations, **btn_style).pack(fill="x")
        tk.Button(self.sidebar, text="Exit", command=self.root.quit, **btn_style).pack(fill="x", side="bottom")

        # Initial View
        self.welcome_screen()

    def welcome_screen(self):
        self.clear_content()
        label = tk.Label(self.content_area, text="Welcome! Please upload a CSV file to get started.", 
                        font=("Helvetica", 14), bg="#f0f2f5")
        label.pack(expand=True)

    def clear_content(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def upload_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            success, msg = self.analyzer.load_data(file_path)
            if success:
                self.file_path = file_path
                messagebox.showinfo("Success", "File loaded! Now performing preprocessing...")
                p_success, p_msg = self.analyzer.preprocess_data()
                messagebox.showinfo("Preprocessing", p_msg)
                self.show_summary()
            else:
                messagebox.showerror("Error", msg)

    def show_summary(self):
        if not self.file_path:
            messagebox.showwarning("Warning", "Please upload data first.")
            return

        self.clear_content()
        stats = self.analyzer.get_summary_stats()
        
        # Summary Frame
        summary_frame = tk.LabelFrame(self.content_area, text="Business Insights Summary", 
                                     font=("Helvetica", 12, "bold"), padx=20, pady=20, bg="white")
        summary_frame.pack(fill="x", padx=20, pady=10)

        # Display Stats
        row = 0
        for key, value in stats.items():
            tk.Label(summary_frame, text=f"{key}:", font=("Helvetica", 11, "bold"), bg="white").grid(row=row, column=0, sticky="w", pady=5)
            display_val = f"${value:,.2f}" if "Sales" in key or "Value" in key else value
            tk.Label(summary_frame, text=display_val, font=("Helvetica", 11), bg="white").grid(row=row, column=1, sticky="w", padx=10)
            row += 1

        # Detailed Tables (using Treeview)
        table_frame = tk.Frame(self.content_area, bg="#f0f2f5")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Top Customers Table
        cust_label = tk.Label(table_frame, text="Top 5 Customers by Sales", font=("Helvetica", 11, "bold"), bg="#f0f2f5")
        cust_label.pack(anchor="w")
        
        self.create_treeview(table_frame, self.analyzer.get_top_customers().reset_index(), ["Customer ID", "Total Sales"])

    def create_treeview(self, parent, df, columns):
        tree = ttk.Treeview(parent, columns=columns, show='headings', height=6)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        for _, row in df.iterrows():
            formatted_row = [f"${val:,.2f}" if isinstance(val, (int, float)) and "Sales" in columns[1] else val for val in row]
            tree.insert("", "end", values=formatted_row)
        
        tree.pack(fill="x", pady=5)

    def show_visualizations(self):
        if not self.file_path:
            messagebox.showwarning("Warning", "Please upload data first.")
            return

        self.clear_content()
        
        # Controls Frame
        ctrl_frame = tk.Frame(self.content_area, bg="#f0f2f5")
        ctrl_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(ctrl_frame, text="Select View:", font=("Helvetica", 10), bg="#f0f2f5").pack(side="left")
        
        chart_type = tk.StringVar(value="Product Performance")
        options = ["Product Performance", "Sales Trends", "Regional Distribution"]
        dropdown = ttk.Combobox(ctrl_frame, textvariable=chart_type, values=options, state="readonly")
        dropdown.pack(side="left", padx=10)
        
        # Display Frame
        self.chart_frame = tk.Frame(self.content_area, bg="white", highlightbackground="#ddd", highlightthickness=1)
        self.chart_frame.pack(fill="both", expand=True, padx=20, pady=10)

        def update_chart(*args):
            choice = chart_type.get()
            if choice == "Product Performance":
                fig = self.visualizer.create_bar_chart(self.analyzer.get_product_performance(), 
                                                       "Sales by Product", "Product", "Total Sales")
            elif choice == "Sales Trends":
                fig = self.visualizer.create_line_chart(self.analyzer.get_sales_trends(), 
                                                        "Monthly Sales Trend", "Month", "Total Sales")
            elif choice == "Regional Distribution":
                fig = self.visualizer.create_pie_chart(self.analyzer.get_regional_distribution(), 
                                                       "Sales by Region")
            self.visualizer.embed_chart(self.chart_frame, fig)

        dropdown.bind("<<ComboboxSelected>>", update_chart)
        # Initial chart
        update_chart()

if __name__ == "__main__":
    root = tk.Tk()
    app = DataAnalysisApp(root)
    root.mainloop()
