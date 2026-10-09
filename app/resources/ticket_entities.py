from datetime import datetime
from enum import IntEnum
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class TicketStatus(IntEnum):
    OPEN = 2
    PENDING = 3
    RESOLVED = 4
    CLOSED = 5


class TicketPriority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


class TicketFilter(str, Enum):
    NEW_AND_MY_OPEN = "new_and_my_open"
    WATCHING = "watching"
    SPAM = "spam"
    DELETED = "deleted"


class TicketOrderBy(str, Enum):
    CREATED_AT = "created_at"
    DUE_BY = "due_by"
    UPDATED_AT = "updated_at"
    STATUS = "status"


class TicketRequester(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    mobile: Optional[str] = None
    phone: Optional[str] = None


class TicketCompany(BaseModel):
    id: int
    name: str


class TicketStats(BaseModel):
    closed_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    first_responded_at: Optional[datetime] = None


class TicketConversation(BaseModel):
    id: int
    ticket_id: int
    body: str
    body_text: Optional[str] = None
    user_id: int
    created_at: datetime
    updated_at: datetime
    source: Optional[int] = None
    incoming: Optional[bool] = None
    private: Optional[bool] = None
    attachment_ids: Optional[List[Any]] = None


class Ticket(BaseModel):
    id: int
    subject: Optional[str] = None
    description: Optional[str] = None
    description_text: Optional[str] = None
    structured_description: Optional[Dict[str, Any]] = None
    status: TicketStatus
    priority: TicketPriority
    source: int
    source_info: Optional[int] = None
    spam: bool
    fr_escalated: bool
    is_escalated: bool
    requester_id: int
    responder_id: Optional[int] = None
    group_id: Optional[int] = None
    company_id: Optional[int] = None
    email_config_id: Optional[int] = None
    product_id: Optional[int] = None
    type: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    due_by: Optional[datetime] = None
    fr_due_by: Optional[datetime] = None
    cc_emails: List[str] = []
    fwd_emails: List[str] = []
    reply_cc_emails: List[str] = []
    to_emails: Optional[List[str]] = None
    tags: List[str] = []
    custom_fields: Dict[str, Any] = {}
    attachments: List[Any] = []
    association_type: Optional[int] = None
    associated_tickets_list: Optional[List[int]] = None
    # requester identifier fields returned directly on the ticket
    email: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    twitter_id: Optional[str] = None
    facebook_id: Optional[str] = None
    unique_external_id: Optional[str] = None
    # parent/child ticket linking
    parent_id: Optional[int] = None
    # internal routing fields
    internal_agent_id: Optional[int] = None
    internal_group_id: Optional[int] = None
    # populated when include=requester|company|stats|conversations is passed
    requester: Optional[TicketRequester] = None
    company: Optional[TicketCompany] = None
    stats: Optional[TicketStats] = None
    conversations: Optional[List[TicketConversation]] = None


class TicketSearchResult(BaseModel):
    total: int
    results: List[Ticket]
