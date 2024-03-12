from pydantic import BaseModel, root_validator
import hashlib


class SourceUrl(BaseModel):
    url: str
    hash: str = ""

    @root_validator(pre=True)
    def set_hash(cls, values):
        if url := values.get('url'):
            values['hash'] = hashlib.sha256(url.encode()).hexdigest()
        return values
