from datetime import datetime


class Task:

    def __init__(self, id, title, description="", status="pending"):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.created_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at
        }

    def update(self, data):
        if "title" in data:
            self.title = data["title"]
        if "description" in data:
            self.description = data["description"]
        if "status" in data and data["status"] in ["pending", "done"]:
            self.status = data["status"]
            