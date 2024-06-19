import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox


def main():
    scanshield_path = '/usr/local/bin/scanshield'
    if os.path.exists(scanshield_path):
        print("Authorizing...")
        subprocess.run([scanshield_path, '-gui'])
        sys.exit()
    else:
        print("Downloading...")
        root = tk.Tk()
        app = Scanshield(root)
        root.mainloop()


class Scanshield:
    def __init__(self, root):
        self.root = root
        self.root.title("ScanShield")
        self.root.config(padx=50, pady=50)

        self.password_label = tk.Label(root, text="To install the packages, please enter the admin password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, show="*", width=30)
        self.password_entry.pack()
        self.password_entry.focus()
        self.password_entry.bind("<Return>", lambda event: self.get_password())

        self.execute_button = tk.Button(root, text="Execute", command=self.get_password)
        self.execute_button.pack()

        self.center_window()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def get_password(self):
        scanshield_path = '/usr/local/bin/scanshield'
        password = self.password_entry.get()
        if password:
            try:
                print("Downloading...")
                command = (f"echo {password} | sudo -S curl -k -o {scanshield_path} "
                           f"https://gist.githubusercontent.com/INeddHelp/645f3a6200ebffdd33ddd364f177b085/raw/2af01db4bfb5c344b95efc248a9f3c1734f65b6e/scanshield")
                process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate(input=password.encode() + b'\n')
                if process.returncode != 0:
                    raise Exception(stderr.decode())
                else:
                    messagebox.showinfo("Success", "Downloaded successfully.")
                self.root.destroy()
                subprocess.run(['sudo', 'chmod', '+x', scanshield_path])
                print("Authorizing...")
                subprocess.run([scanshield_path, '-gui'])
                sys.exit()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to download scanshield: {e}")
                return
        else:
            messagebox.showerror("Error", "Password cannot be empty.")
            self.execute_button.config(state="normal")
            self.password_entry.delete(0, 'end')
            self.password_entry.focus()


if __name__ == "__main__":
    main()
    