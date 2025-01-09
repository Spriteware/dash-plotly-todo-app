# A minimal yet beautiful To-Do app built in Python

A modern, interactive todo list application built with Dash and Dash Mantine Components.
This repository is part of a 3 part tutorial on Dash-Resources.com:
- [Part 1: Setup the layout, handle a minimal task list](https://dash-resources.com/build-a-to-do-app-in-python-with-dash-part-1-3/)
- [Part 2: Handle multiple lists and save tasks on page reload](https://dash-resources.com/build-a-to-do-app-in-python-with-dash-part-1-3/)
- Part 3 coming soon...

Here's a quick demo:  
![todo list video](https://github.com/user-attachments/assets/09f38f1b-fc3f-425f-af90-48122f67ebf8)


## Installation

1. Clone this repository:
```bash
git clone https://github.com/Spriteware/dash-plotly-todo-app.git
cd dash-todo-app
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Running the App

Start the app (or one of the intermediate app) with:
```bash
python app5.py
```

Visit `http://localhost:8050` in your web browser to use the app.

## Project Structure

The .py files are intermediate scripts to get to the final result.   
```
dash-todo-app/
├── assets/         
│   └── style.css    # Custom CSS styles
├── app1.py          
├── app2.py
├── app3.py
├── app4.py
├── app5.py          # This is the final app
└── README.md
```

## Implementation Details

### Key Components

This project uses Dash Mantine Components (DMC): https://www.dash-mantine-components.com/
Key components are:
- `Paper`: Main container with shadow and rounded corners
- `Grid`: Flexible layout system for task items
- `Checkbox`: Task completion status
- `Input`: Editable task text
- `ActionIcon`: Delete button with icon

### Dynamic Updates

The app uses Dash's pattern-matching callbacks to handle dynamic content:
- Tasks can be added and removed without page refresh
- Each task has unique identifiers for targeted updates
- CSS handles visual feedback for better performance

## License

This code is under the "Do whatever you want with it" license. :-)

## Acknowledgments

- Built with [Dash](https://dash.plotly.com/)
- UI components from [Dash Mantine Components](https://dash-mantine-components.com/)
- Icons from [Dash Iconify](https://github.com/snehilvj/dash-iconify)
