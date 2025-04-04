# Example 1: REST API

## Table of Contents

- [Intro](#intro)
- [Setup](#setup)
- [Requests](#requests)
- [Usage](#usage)

## Intro

Like the title says, this is an example for a REST API.
For the purpose of the example, I used a dict instead of an actual database.
It has all the CRUD (CREATE, READ, UPDATE, DELETE) functions.
It's done in Python with the Flask module.

## Setup

To play around with this code first download the files inside a folder:

```bash
mkdir example
cd example
git init
git branch -m main
git remote add origin https://github.com/arosario513/COMP-2052.git
git sparse-checkout init
git sparse-checkout add example1
git pull origin main
```

Then go to `example1`:

```bash
cd example1
```

Setup the python virtual environment:

### Linux/Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```powershell
python3 -m venv venv
venv\Scripts\activate.bat
```

Finally, install the required modules:

```bash
pip install -r requirements.txt
```

After that you should be good to go. Just run `python main.py` and the server should boot up

**Note:** the default server is http://127.0.0.1:5000

## Requests

### GET

| Path               | Action                                           |
| ------------------ | ------------------------------------------------ |
| /                  | Root Path                                        |
| /tasks             | Shows all tasks                                  |
| /tasks/\<task_id\> | Shows a specific task based on the given task id |

### POST

| Path   | Action          |
| ------ | --------------- |
| /tasks | Adds a new task |

### PUT

| Path               | Action                                              |
| ------------------ | --------------------------------------------------- |
| /tasks/\<task_id\> | Changes the name of the task with the given task id |

### DELETE

| Path               | Action                                  |
| ------------------ | --------------------------------------- |
| /tasks/\<task_id\> | Deletes the task with the given task id |

## Usage

I'm going to use `curl` for these examples

- `-X` will have the request type we are going to use.
- `-H` contains **H**eader data
- `-d` will have the **d**ata for the tasks we will add or modify

### Viewing all tasks

```bash
curl -X GET http://127.0.0.1:5000/tasks
```

#### Output:

```json
[
  {
    "name": "Eat",
    "task_id": 0
  },
  {
    "name": "Sleep",
    "task_id": 1
  },
  {
    "name": "Work",
    "task_id": 2
  }
]
```

### Viewing a specific task

```bash
curl -X GET http://127.0.0.1:5000/tasks/2
```

#### Output:

```json
{
  "name": "Work",
  "task_id": 2
}
```

### Adding a task

```bash
curl -X POST http://127.0.0.1:5000/tasks \
-H "Content-Type: application/json" \
-d '{ "name": "Study" }'
```

#### Output:

```json
{
  "message": "New task added.",
  "task": {
    "name": "Study",
    "task_id": 3
  }
}
```

### Changing a task

```bash
curl -X PUT http://127.0.0.1:5000/tasks/1 \
-H "Content-Type: application/json" \
-d '{ "name": "Exercise" }'
```

#### Output:

```json
{
  "message": "Updated name for task with ID 1.",
  "new_task": {
    "name": "Exercise",
    "task_id": 1
  },
  "old_task": {
    "name": "Sleep",
    "task_id": 1
  }
}
```

### Deleting a task

```bash
curl -X DELETE http://127.0.0.1:5000/tasks/2
```

#### Output:

```json
{
  "message": "Task with ID 2 deleted."
}
```
