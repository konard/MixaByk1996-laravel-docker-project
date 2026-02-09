from fastapi import APIRouter

from app.api.v1 import avito, email, contacts, dashboard

router = APIRouter()

router.include_router(avito.router, prefix="/avito", tags=["Avito"])
router.include_router(email.router, prefix="/email", tags=["Email"])
router.include_router(contacts.router, prefix="/contacts", tags=["Contacts"])
router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
