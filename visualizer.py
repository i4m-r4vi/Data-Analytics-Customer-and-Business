import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns

class Visualizer:
    def __init__(self):
        sns.set_theme(style="whitegrid")

    def create_bar_chart(self, series, title, xlabel, ylabel):
        fig, ax = plt.subplots(figsize=(6, 4))
        series.plot(kind="bar", ax=ax, color="#4a90e2")
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        plt.tight_layout()
        return fig

    def create_line_chart(self, series, title, xlabel, ylabel):
        fig, ax = plt.subplots(figsize=(6, 4))
        # Convert index to string for better display if it's Period
        series.index = series.index.astype(str)
        series.plot(kind="line", marker='o', ax=ax, color="#e67e22")
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        plt.tight_layout()
        return fig

    def create_pie_chart(self, series, title):
        fig, ax = plt.subplots(figsize=(5, 5))
        series.plot(kind="pie", autopct='%1.1f%%', ax=ax, colors=sns.color_palette("viridis"))
        ax.set_title(title)
        ax.set_ylabel("")
        plt.tight_layout()
        return fig

    def embed_chart(self, parent_frame, fig):
        # Clear previous charts if any
        for widget in parent_frame.winfo_children():
            widget.destroy()
            
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
