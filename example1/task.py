class Task:
    def __init__(self, task_id: int, name: str):
        self.task_id = task_id
        self.name = name

    def to_dict(self):
        '''Returns the Object as Dict'''
        return {"task_id": self.task_id, "name": self.name}
