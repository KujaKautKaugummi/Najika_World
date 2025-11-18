"""
Region Boss API - Najika World (Territory Control System)
==========================================================

REST API für Gebietsherrscher System (FastAPI) (DATABASE)

Uses RegionBoss and Challenge models from magic_progress.py

Endpoints:
- POST /api/region-boss/conquer - Conquer region (DATABASE)
- POST /api/region-boss/challenge/create - Create challenge (DATABASE)
- GET /api/region-boss/region/{region} - Get region info (DATABASE)
- GET /api/region-boss/all - Get all regions (DATABASE)
- POST /api/region-boss/tax/set - Set tax rate (DATABASE)
- GET /api/region-boss/state/export - Export state (DATABASE)

Copyright: Najika World
Author: Claude Code (CLI)
Date: 2025-11-18
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from datetime import datetime

from backend.database import get_db
from backend.models.magic_progress import RegionBoss, Challenge

# Create FastAPI Router
router = APIRouter(prefix="/api/region-boss", tags=["region_boss"])


# ============================================================================
# REQUEST MODELS (Pydantic)
# ============================================================================

class ConquerRegionRequest(BaseModel):
    player_id: int
    region: str
    conquest_path: str = "krieg"  # krieg, handel, diplomatie, quest_line


class CreateChallengeRequest(BaseModel):
    challenger_id: int
    region: str
    challenge_type: str = "krieg"


class SetTaxRateRequest(BaseModel):
    boss_player_id: int
    region: str
    tax_rate: float


# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/conquer")
async def conquer_region(request: ConquerRegionRequest, db: Session = Depends(get_db)):
    """
    Conquer Region (DATABASE)

    Body:
    {
        "player_id": 1,
        "region": "samtmoos_tiefwald",
        "conquest_path": "krieg"
    }
    """
    try:
        # Check if region exists
        region_boss = db.query(RegionBoss).filter(
            RegionBoss.region == request.region
        ).first()

        if region_boss:
            # Region already has boss - challenge required
            if region_boss.boss_player_id == request.player_id:
                return {
                    "success": False,
                    "message": "Du kontrollierst diese Region bereits!"
                }
            else:
                return {
                    "success": False,
                    "message": f"Region wird von Spieler {region_boss.boss_player_id} kontrolliert. Erstelle eine Challenge!",
                    "boss_player_id": region_boss.boss_player_id
                }
        else:
            # Create new region boss entry
            region_boss = RegionBoss(
                region=request.region,
                boss_player_id=request.player_id,
                conquest_path=request.conquest_path,
                control_started=datetime.utcnow(),
                tax_rate=5.0,
                last_conquest=datetime.utcnow()
            )
            db.add(region_boss)
            db.commit()
            db.refresh(region_boss)

            return {
                "success": True,
                "message": f"Region {request.region} erfolgreich erobert!",
                "region": region_boss.to_dict()
            }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/challenge/create")
async def create_challenge(request: CreateChallengeRequest, db: Session = Depends(get_db)):
    """
    Create Challenge (DATABASE)

    Body:
    {
        "challenger_id": 2,
        "region": "samtmoos_tiefwald",
        "challenge_type": "krieg"
    }
    """
    try:
        # Get region boss
        region_boss = db.query(RegionBoss).filter(
            RegionBoss.region == request.region
        ).first()

        if not region_boss:
            raise HTTPException(status_code=404, detail="Region hat keinen Boss")

        if region_boss.boss_player_id == request.challenger_id:
            raise HTTPException(status_code=400, detail="Du kannst dich nicht selbst herausfordern!")

        # Create challenge
        challenge = Challenge(
            region=request.region,
            challenger_id=request.challenger_id,
            defender_id=region_boss.boss_player_id,
            challenge_type=request.challenge_type,
            status="pending"
        )

        db.add(challenge)
        db.commit()
        db.refresh(challenge)

        # Update region boss
        region_boss.active_challenge_id = challenge.id
        region_boss.challenge_count += 1
        db.commit()

        return {
            "success": True,
            "challenge_id": challenge.id,
            "message": f"Challenge erstellt gegen Spieler {region_boss.boss_player_id}!",
            "challenge": challenge.to_dict()
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/region/{region}")
async def get_region_info(region: str, db: Session = Depends(get_db)):
    """
    Get Region Info (DATABASE)

    Path: /api/region-boss/region/samtmoos_tiefwald
    """
    try:
        region_boss = db.query(RegionBoss).filter(
            RegionBoss.region == region
        ).first()

        if not region_boss:
            return {
                "region": region,
                "has_boss": False,
                "message": "Diese Region ist unbeansprucht!"
            }

        # Get active challenge
        active_challenge = None
        if region_boss.active_challenge_id:
            challenge = db.query(Challenge).filter(
                Challenge.id == region_boss.active_challenge_id
            ).first()
            if challenge:
                active_challenge = challenge.to_dict()

        return {
            "region": region,
            "has_boss": True,
            "boss": region_boss.to_dict(),
            "active_challenge": active_challenge
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/all")
async def get_all_regions(db: Session = Depends(get_db)):
    """
    Get All Regions (DATABASE)

    Path: /api/region-boss/all
    """
    try:
        regions = db.query(RegionBoss).all()

        return {
            "regions": [r.to_dict() for r in regions],
            "count": len(regions)
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tax/set")
async def set_tax_rate(request: SetTaxRateRequest, db: Session = Depends(get_db)):
    """
    Set Tax Rate (DATABASE)

    Body:
    {
        "boss_player_id": 1,
        "region": "samtmoos_tiefwald",
        "tax_rate": 7.5
    }
    """
    try:
        region_boss = db.query(RegionBoss).filter(
            RegionBoss.region == request.region
        ).first()

        if not region_boss:
            raise HTTPException(status_code=404, detail="Region nicht gefunden")

        if region_boss.boss_player_id != request.boss_player_id:
            raise HTTPException(status_code=403, detail="Du kontrollierst diese Region nicht!")

        # Validate tax rate (5-10%)
        if not (5.0 <= request.tax_rate <= 10.0):
            raise HTTPException(status_code=400, detail="Tax rate muss zwischen 5% und 10% liegen")

        region_boss.tax_rate = request.tax_rate
        db.commit()
        db.refresh(region_boss)

        return {
            "success": True,
            "region": request.region,
            "new_tax_rate": request.tax_rate,
            "message": f"Tax rate auf {request.tax_rate}% gesetzt"
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/state/export")
async def export_state(db: Session = Depends(get_db)):
    """
    Export Complete State (DATABASE)

    Path: /api/region-boss/state/export
    """
    try:
        regions = db.query(RegionBoss).all()
        challenges = db.query(Challenge).all()

        return {
            "regions": [r.to_dict() for r in regions],
            "challenges": [c.to_dict() for c in challenges],
            "region_count": len(regions),
            "challenge_count": len(challenges)
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
