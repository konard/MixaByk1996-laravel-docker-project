from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.avito import (
    AvitoAccount, AvitoAd, AvitoAdTemplate, AvitoAdStat,
    AvitoCompetitor, AvitoCompetitorSnapshot,
    AvitoMessage, AvitoAutoReply,
)
from app.schemas.avito import (
    AvitoAccountCreate, AvitoAccountUpdate, AvitoAccountResponse,
    AvitoAdCreate, AvitoAdUpdate, AvitoAdResponse, AvitoAdStatResponse,
    AvitoAdTemplateCreate, AvitoAdTemplateResponse,
    AvitoCompetitorCreate, AvitoCompetitorResponse, AvitoCompetitorSnapshotResponse,
    AvitoMessageResponse,
    AvitoAutoReplyCreate, AvitoAutoReplyResponse,
)
from app.services.avito_service import AvitoApiService

router = APIRouter()


# --- Accounts ---

@router.get("/accounts", response_model=List[AvitoAccountResponse])
async def list_accounts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(AvitoAccount))
    return result.scalars().all()

@router.post("/accounts", response_model=AvitoAccountResponse, status_code=201)
async def create_account(data: AvitoAccountCreate, db: AsyncSession = Depends(get_db)):
    account = AvitoAccount(**data.model_dump())
    db.add(account)
    await db.flush()
    await db.refresh(account)
    return account

@router.get("/accounts/{account_id}", response_model=AvitoAccountResponse)
async def get_account(account_id: int, db: AsyncSession = Depends(get_db)):
    account = await db.get(AvitoAccount, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@router.put("/accounts/{account_id}", response_model=AvitoAccountResponse)
async def update_account(account_id: int, data: AvitoAccountUpdate, db: AsyncSession = Depends(get_db)):
    account = await db.get(AvitoAccount, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(account, key, value)
    await db.flush()
    await db.refresh(account)
    return account

@router.delete("/accounts/{account_id}", status_code=204)
async def delete_account(account_id: int, db: AsyncSession = Depends(get_db)):
    account = await db.get(AvitoAccount, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    await db.delete(account)


# --- Ad Templates ---

@router.get("/templates", response_model=List[AvitoAdTemplateResponse])
async def list_templates(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(AvitoAdTemplate))
    return result.scalars().all()

@router.post("/templates", response_model=AvitoAdTemplateResponse, status_code=201)
async def create_template(data: AvitoAdTemplateCreate, db: AsyncSession = Depends(get_db)):
    template = AvitoAdTemplate(**data.model_dump())
    db.add(template)
    await db.flush()
    await db.refresh(template)
    return template


# --- Ads ---

@router.get("/ads", response_model=List[AvitoAdResponse])
async def list_ads(campaign: str = None, db: AsyncSession = Depends(get_db)):
    query = select(AvitoAd)
    if campaign:
        query = query.where(AvitoAd.campaign == campaign)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/ads", response_model=AvitoAdResponse, status_code=201)
async def create_ad(data: AvitoAdCreate, db: AsyncSession = Depends(get_db)):
    ad = AvitoAd(**data.model_dump())
    db.add(ad)
    await db.flush()
    await db.refresh(ad)
    return ad

@router.get("/ads/{ad_id}", response_model=AvitoAdResponse)
async def get_ad(ad_id: int, db: AsyncSession = Depends(get_db)):
    ad = await db.get(AvitoAd, ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    return ad

@router.put("/ads/{ad_id}", response_model=AvitoAdResponse)
async def update_ad(ad_id: int, data: AvitoAdUpdate, db: AsyncSession = Depends(get_db)):
    ad = await db.get(AvitoAd, ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(ad, key, value)
    await db.flush()
    await db.refresh(ad)
    return ad

@router.delete("/ads/{ad_id}", status_code=204)
async def delete_ad(ad_id: int, db: AsyncSession = Depends(get_db)):
    ad = await db.get(AvitoAd, ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    await db.delete(ad)

@router.post("/ads/{ad_id}/publish")
async def publish_ad(ad_id: int, db: AsyncSession = Depends(get_db)):
    ad = await db.get(AvitoAd, ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    service = AvitoApiService(db)
    result = await service.publish_ad(ad)
    return {"status": "published", "avito_id": ad.avito_id}

@router.post("/ads/{ad_id}/unpublish")
async def unpublish_ad(ad_id: int, db: AsyncSession = Depends(get_db)):
    ad = await db.get(AvitoAd, ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    service = AvitoApiService(db)
    await service.unpublish_ad(ad)
    return {"status": "archived"}

@router.get("/ads/{ad_id}/stats", response_model=List[AvitoAdStatResponse])
async def get_ad_stats(ad_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(AvitoAdStat).where(AvitoAdStat.ad_id == ad_id))
    return result.scalars().all()

@router.post("/ads/{ad_id}/sync-stats")
async def sync_ad_stats(ad_id: int, db: AsyncSession = Depends(get_db)):
    ad = await db.get(AvitoAd, ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    service = AvitoApiService(db)
    stat = await service.sync_ad_stats(ad)
    return {"status": "synced", "stat_id": stat.id if stat else None}


# --- Competitors ---

@router.get("/competitors", response_model=List[AvitoCompetitorResponse])
async def list_competitors(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(AvitoCompetitor))
    return result.scalars().all()

@router.post("/competitors", response_model=AvitoCompetitorResponse, status_code=201)
async def create_competitor(data: AvitoCompetitorCreate, db: AsyncSession = Depends(get_db)):
    competitor = AvitoCompetitor(**data.model_dump())
    db.add(competitor)
    await db.flush()
    await db.refresh(competitor)
    return competitor

@router.get("/competitors/{competitor_id}", response_model=AvitoCompetitorResponse)
async def get_competitor(competitor_id: int, db: AsyncSession = Depends(get_db)):
    competitor = await db.get(AvitoCompetitor, competitor_id)
    if not competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")
    return competitor

@router.get("/competitors/{competitor_id}/snapshots", response_model=List[AvitoCompetitorSnapshotResponse])
async def get_competitor_snapshots(competitor_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(AvitoCompetitorSnapshot).where(AvitoCompetitorSnapshot.competitor_id == competitor_id)
    )
    return result.scalars().all()

@router.post("/competitors/{competitor_id}/check")
async def check_competitor(competitor_id: int, db: AsyncSession = Depends(get_db)):
    competitor = await db.get(AvitoCompetitor, competitor_id)
    if not competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")
    service = AvitoApiService(db)
    snapshots = await service.check_competitors(competitor)
    return {"status": "checked", "snapshots_count": len(snapshots)}


# --- Messages ---

@router.get("/messages", response_model=List[AvitoMessageResponse])
async def list_messages(account_id: int = None, db: AsyncSession = Depends(get_db)):
    query = select(AvitoMessage)
    if account_id:
        query = query.where(AvitoMessage.account_id == account_id)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/messages/fetch/{account_id}")
async def fetch_messages(account_id: int, db: AsyncSession = Depends(get_db)):
    account = await db.get(AvitoAccount, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    service = AvitoApiService(db)
    messages = await service.fetch_messages(account)
    return {"status": "fetched", "count": len(messages)}


# --- Auto Replies ---

@router.get("/auto-replies", response_model=List[AvitoAutoReplyResponse])
async def list_auto_replies(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(AvitoAutoReply))
    return result.scalars().all()

@router.post("/auto-replies", response_model=AvitoAutoReplyResponse, status_code=201)
async def create_auto_reply(data: AvitoAutoReplyCreate, db: AsyncSession = Depends(get_db)):
    rule = AvitoAutoReply(**data.model_dump())
    db.add(rule)
    await db.flush()
    await db.refresh(rule)
    return rule

@router.delete("/auto-replies/{rule_id}", status_code=204)
async def delete_auto_reply(rule_id: int, db: AsyncSession = Depends(get_db)):
    rule = await db.get(AvitoAutoReply, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Auto reply rule not found")
    await db.delete(rule)
