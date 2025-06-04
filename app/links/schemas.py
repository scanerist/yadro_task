from pydantic import BaseModel, HttpUrl, ConfigDict

from datetime import datetime

class LinkBase(BaseModel):
    orig_url: HttpUrl

class LinkCreate(LinkBase):
    pass

class LinkRead(LinkBase):
    id: int
    short_code: str
    is_active: bool
    created_at: datetime
    expires_at: datetime
    click_count: int

    model_config = ConfigDict(from_attributes=True,
                              json_schema_extra={
                                 "example": {
                                     "id": 1,
                                     "orig_url": "https://example.com",
                                     "short_code": "abc123",
                                     "is_active": True,
                                     "created_at": "2023-10-01T12:00:00Z",
                                     "expires_at": "2023-11-01T12:00:00Z",
                                     "click_count": 10
                                 }
                             })

class LinkStats(BaseModel):
    link: str
    orig_link: str
    last_hour_clicks: int
    last_day_clicks: int