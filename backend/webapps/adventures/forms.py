from typing import List
from typing import Optional

from fastapi import Request


class adventureCreateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.date: Optional[str] = None
        self.traject: Optional[str] = None
        self.description: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.date = form.get("date")
        self.traject = form.get("traject")
        self.description = form.get("description")

    def is_valid(self):
        if not self.date or not len(self.date) >= 4:
            self.errors.append("A valid title is required")
        if not self.traject:
            self.errors.append("Valid Url is required ")
        if not self.description or not len(self.description) >= 20:
            self.errors.append("Description too short")
        if not self.errors:
            return True
        return False
