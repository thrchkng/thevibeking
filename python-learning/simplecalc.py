import tkinter as tk
from tkinter import messagebox

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Калькулятор")
        self.window.geometry("300x400")
        self.window.resizable(False, False)
        
        self.current_input = ""
        self.result_var = tk.StringVar()
        
        self.create_widgets()
    
    def create_widgets(self):
        # Поле вывода
        display_frame = tk.Frame(self.window)
        display_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        display = tk.Entry(display_frame, textvariable=self.result_var, 
                          font=('Arial', 18), justify='right', state='readonly')
        display.pack(expand=True, fill="both")
        
        # Кнопки
        buttons_frame = tk.Frame(self.window)
        buttons_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Расположение кнопок
        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', '=', '+'],
            ['C', 'CE']
        ]
        
        for i, row in enumerate(buttons):
            for j, button_text in enumerate(row):
                if button_text == '=':
                    btn = tk.Button(buttons_frame, text=button_text, 
                                  font=('Arial', 14),
                                  command=self.calculate)
                    btn.grid(row=i, column=j, sticky="nsew", padx=2, pady=2)
                elif button_text in ['C', 'CE']:
                    btn = tk.Button(buttons_frame, text=button_text, 
                                  font=('Arial', 14),
                                  command=self.clear if button_text == 'C' else self.clear_entry)
                    btn.grid(row=i, column=j, sticky="nsew", padx=2, pady=2)
                else:
                    btn = tk.Button(buttons_frame, text=button_text, 
                                  font=('Arial', 14),
                                  command=lambda x=button_text: self.button_click(x))
                    btn.grid(row=i, column=j, sticky="nsew", padx=2, pady=2)
                
                buttons_frame.grid_columnconfigure(j, weight=1)
            buttons_frame.grid_rowconfigure(i, weight=1)
    
    def button_click(self, value):
        self.current_input += str(value)
        self.result_var.set(self.current_input)
    
    def clear(self):
        self.current_input = ""
        self.result_var.set("")
    
    def clear_entry(self):
        self.current_input = self.current_input[:-1]
        self.result_var.set(self.current_input)
    
    def calculate(self):
        try:
            if self.current_input:
                # Безопасное вычисление
                result = eval(self.current_input)
                self.result_var.set(result)
                self.current_input = str(result)
        except ZeroDivisionError:
            messagebox.showerror("Ошибка", "Деление на ноль!")
            self.clear()
        except:
            messagebox.showerror("Ошибка", "Неверное выражение!")
            self.clear()
    
    def run(self):
        self.window.mainloop()

# Запуск калькулятора
if __name__ == "__main__":
    calc = Calculator()
    calc.run()