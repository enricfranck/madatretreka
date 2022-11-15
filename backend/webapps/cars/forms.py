from typing import List
from typing import Optional

from fastapi import Request


class carCreateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.name: Optional[str] = None
        self.url_image: Optional[str] = None
        self.description: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.name = form.get("name")
        self.url_image = form.get("url_image")
        self.description = form.get("description")

    def is_valid(self):
        if not self.name or not len(self.name) >= 4:
            self.errors.append("A valid name is required")
        if not self.url_image:
            self.errors.append("Valid Url is required ")
        if not self.description or not len(self.description) >= 10:
            self.errors.append("Description too short")
        if not self.errors:
            return True
        return False
