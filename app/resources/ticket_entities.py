from datetime import datetime
from enum import Enum, IntEnum
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


class TicketSource(IntEnum):
    EMAIL = 1
    PORTAL = 2
    PHONE = 3
    CHAT = 7
    FEEDBACK_WIDGET = 9
    OUTBOUND_EMAIL = 10


class AssociationType(IntEnum):
    PARENT = 1
    CHILD = 2
    TRACKER = 3
    RELATED = 4


class ConversationSource(IntEnum):
    REPLY = 0
    NOTE = 2
    TWITTER = 5
    SURVEY_FEEDBACK = 6
    FACEBOOK = 7
    FORWARDED_EMAIL = 8
    PHONE = 9
    ECOMMERCE = 11


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
    structured_body: Optional[Dict[str, Any]] = None
    user_id: int
    created_at: datetime
    updated_at: datetime
    source: Optional[ConversationSource] = None
    incoming: Optional[bool] = None
    private: Optional[bool] = None
    support_email: Optional[str] = None
    to_emails: Optional[List[str]] = None
    from_email: Optional[str] = None
    cc_emails: List[str] = []
    bcc_emails: List[str] = []
    replied_to: Optional[List[str]] = None
    notified_to: Optional[List[str]] = None
    last_edited_at: Optional[datetime] = None
    last_edited_user_id: Optional[int] = None
    attachments: List[Any] = []


class Ticket(BaseModel):
    id: int
    subject: Optional[str] = None
    description: Optional[str] = None
    description_text: Optional[str] = None
    structured_description: Optional[Dict[str, Any]] = None
    status: TicketStatus
    priority: TicketPriority
    source: TicketSource
    source_info: Optional[int] = None
    spam: bool
    deleted: Optional[bool] = None
    urgent: Optional[bool] = None
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
    association_type: Optional[AssociationType] = None
    associated_tickets_list: Optional[List[int]] = None
    # populated when include=requester|company|stats|conversations is passed
    requester: Optional[TicketRequester] = None
    company: Optional[TicketCompany] = None
    stats: Optional[TicketStats] = None
    conversations: Optional[List[TicketConversation]] = None


class TicketSearchResult(BaseModel):
    total: int
    results: List[Ticket]
