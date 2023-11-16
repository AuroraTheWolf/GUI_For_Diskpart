import tkinter as tk
import subprocess
import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit(0)

# Function to run the subprocess without a visible window
def run_subprocess_no_window(command):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, startupinfo=startupinfo)

# Minimize the console window
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)

def list_disks():
    with open("commands.txt", "w") as f:
        f.write("list disk")
    result = run_subprocess_no_window(["diskpart", "/s", "commands.txt"])
    output_text.delete(1.0, tk.END)  # Clear previous output
    output_text.insert(tk.END, result.stdout)

def select_disk():
    disk_number = entry_disk_number.get()
    with open("commands.txt", "w") as f:
        f.write(f"select disk {disk_number}\nlist disk")
    result = run_subprocess_no_window(["diskpart", "/s", "commands.txt"])
    output_text.insert(tk.END, result.stdout)

def clean_disk():
    disk_number = entry_disk_number_clean.get()
    with open("commands.txt", "w") as f:
        f.write(f"select disk {disk_number}\nclean")
    result = run_subprocess_no_window(["diskpart", "/s", "commands.txt"])
    output_text.insert(tk.END, result.stdout)

def create_partition():
    disk_number = entry_disk_number_partition.get()
    partition_size = entry_partition_size.get()
    with open("commands.txt", "w") as f:
        f.write(f"select disk {disk_number}\nclean\ncreate partition primary size={partition_size}")
    result = run_subprocess_no_window(["diskpart", "/s", "commands.txt"])
    output_text.insert(tk.END, result.stdout)

def help_commands():
    help_text = (
        "Help:\n"
        "- Option 1: Lists available disks.\n"
        "- Option 2: Selects a disk based on the entered disk number.\n"
        "- Option 3: Cleans the selected disk.\n"
        "- Option 4: Creates a partition on the selected disk.\n"
        "- Option 5: Displays this help message."
    )
    output_text.insert(tk.END, help_text)

def exit_program():
    root.destroy()

root = tk.Tk()
root.title("Aurora's DiskPart GUI")

# Run the subprocess without a visible window
run_subprocess_no_window(["cmd", "/c", "echo", "Launching command prompt"])

button_list_disks = tk.Button(root, text="List Disks", command=list_disks)
button_list_disks.pack(pady=10)

label_disk_number = tk.Label(root, text="Enter disk number:")
label_disk_number.pack()
entry_disk_number = tk.Entry(root)
entry_disk_number.pack()
button_select_disk = tk.Button(root, text="Select Disk", command=select_disk)
button_select_disk.pack(pady=10)

label_disk_number_clean = tk.Label(root, text="Enter disk number to clean:")
label_disk_number_clean.pack()
entry_disk_number_clean = tk.Entry(root)
entry_disk_number_clean.pack()
button_clean_disk = tk.Button(root, text="Clean Disk", command=clean_disk)
button_clean_disk.pack(pady=10)

label_disk_number_partition = tk.Label(root, text="Enter disk number to partition:")
label_disk_number_partition.pack()
entry_disk_number_partition = tk.Entry(root)
entry_disk_number_partition.pack()

label_partition_size = tk.Label(root, text="Enter partition size (in MB):")
label_partition_size.pack()
entry_partition_size = tk.Entry(root)
entry_partition_size.pack()

button_create_partition = tk.Button(root, text="Create Partition", command=create_partition)
button_create_partition.pack(pady=10)

button_help = tk.Button(root, text="Help", command=help_commands)
button_help.pack(pady=10)

button_exit = tk.Button(root, text="Exit", command=exit_program)
button_exit.pack(pady=10)

output_text = tk.Text(root, height=10, width=50)
output_text.pack(pady=10)

root.mainloop()
