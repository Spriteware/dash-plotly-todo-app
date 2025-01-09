import dash_mantine_components as dmc
from dash import Dash, _dash_renderer, dcc
from dash_iconify import DashIconify
_dash_renderer._set_react_version("18.2.0")  # for mantine


print("------- Loading app ------ ")

# Simplified to just one list
sample_list_data = {
    "title": "My Tasks",
    "tasks_list": [
        {
            "content": "Task A", 
            "checked": True,
        },
        {
            "content": "Task B", 
            "checked": False,
        },
        {
            "content": "Task C", 
            "checked": False,
        },
    ],
}


def get_task(task_dict):
    """ Returns a single task layout """
    text = task_dict["content"]
    checked = task_dict["checked"]

    content = dmc.Grid(
        [
            dmc.GridCol(
                dmc.Checkbox(
                    checked=checked,
                    mt=2
                ), 
                span="content"
            ),
            dmc.GridCol(
                dmc.Text(
                    dcc.Input(
                        text, 
                        className="shadow-input",
                        debounce=True
                    )
                ), 
                span="auto"
            ),
            dmc.GridCol(
                dmc.ActionIcon(
                    DashIconify(icon="tabler:x", width=20),
                    variant="transparent",
                    color="gray",
                    className="task-del-button"
                ),
                span="content"
            ),
        ],
        className="task-container"
    )

    return content


def get_tasks_layout(tasks_list):
    """ Returns the list of tasks """
    tasks = []
    for task_dict in tasks_list:
        task_layout = get_task(task_dict)
        tasks.append(task_layout)

    return tasks


def get_list_layout(list_data):
    """ Returns the list of checkboxes """

    tasks_layout = get_tasks_layout(list_data["tasks_list"])

    content = dmc.Paper(
        [
            dmc.Title(list_data["title"], order=2),
            
            dmc.Container(
                tasks_layout,
                id="main_task_container",
                px=0,
                mt="md",
                mb="md",
            ),

            dmc.Button(
                "Add a new task", 
                id="new_task_button",
                style={"width": "100%"},
                variant="outline", 
                color="gray",
            )
        ],
        shadow="sm",
        p="md",
        mt="md",
        radius="sm",
    )

    return content


app = Dash(__name__)

# Simplified app layout
app.layout = dmc.MantineProvider(
    dmc.Container(
        get_list_layout(sample_list_data),
        size=400,
        mt="md"
    )
)


if __name__ == '__main__':
    app.run_server(debug=True)