# Dash Todo App

A modern, interactive todo list application built with Dash and Dash Mantine Components.
This repository is part of a 3 part tutorial on Dash-Resources.com:
- Build a TODO app with Dash plotly (part 1/3)
- Build a TODO app with Dash plotly (part 2/3)
- Build a TODO app with Dash plotly (part 2/3)


![Todo App Screenshot](placeholder-for-screenshot.png)

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
python app.py
```

Visit `http://localhost:8050` in your web browser to use the app.

## Project Structure

```
dash-todo-app/
├── app.py           # Main application file
├── assets/         
│   └── style.css    # Custom CSS styles
└── README.md
```

## Implementation Details

### Key Components

- `MantineProvider`: Provides theming and styling context
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

### Styling

Custom CSS provides:
- Smooth hover effects on inputs
- Visual feedback for task completion
- Delete button hover states
- Clean input field appearance

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Dash](https://dash.plotly.com/)
- UI components from [Dash Mantine Components](https://dash-mantine-components.com/)
- Icons from [Dash Iconify](https://github.com/snehilvj/dash-iconify)