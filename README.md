# Todo App

A simple todo application built with Python and Tkinter.

## How to Run the App

Hey there! Here's how to get this Todo app running on your computer. It's pretty simple!

### First time setup

1. Make sure you have Python on your computer. Open Terminal and type:
   ```
   python3 --version
   ```
   If you see a version number, you're good to go!

2. Download all the files to a folder on your computer.

3. Open Terminal and go to your folder:
   ```
   cd path/to/folder
   ```

4. Run the setup script:
   ```
   chmod +x setup.sh
   ./setup.sh
   ```
   This creates a special environment for the app to run in.

### Running the app

After you've done the setup once, you can start the app anytime by:

1. Open Terminal
2. Go to your app folder
3. Type:
   ```
   ./run_todo.sh
   ```

That's it! The app should open, and you can start adding your tasks.

### What if something goes wrong?

If you get an error about "Tkinter", just copy and paste this in Terminal:
```
sudo apt-get install python3-tk
```

If you can't run the scripts, try:
```
chmod +x app.py
chmod +x run_todo.sh
```

Easy, right? Now you can keep track of your homework and other tasks!

## Features

- Create, read, update, and delete todos
- Mark todos as complete/incomplete
- Automatic saving to a file
- Works on Windows, Linux, and macOS

## Project Files

- `app.py` - The main application
- `setup.sh` - Setup script
- `run_todo.sh` - Script to run the app
- `run_todo.bat` - Script to run the app on Windows
- `todos.json` - Where your todos are saved

Enjoy using the app!