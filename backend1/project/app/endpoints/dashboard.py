from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.models import User, DataCollection, Activity
from app.db import get_session

router = APIRouter()

@router.get("/top-data-collectors")
async def get_top_data_collectors(db: Session = Depends(get_session)):
    collectors = (
        db.query(User.name, DataCollection.points)
        .join(DataCollection, User.id == DataCollection.user_id)
        .group_by(User.id, DataCollection.points)
        .order_by(DataCollection.points.desc())
        .limit(5)
        .all()
    )
    return {"top_collectors": collectors}

@router.get("/top-point-earners")
async def get_top_point_earners(db: Session = Depends(get_session)):
    earners = (
        db.query(User.name, func.sum(DataCollection.points).label("total_points"))
        .join(DataCollection, User.id == DataCollection.user_id)
        .group_by(User.id)
        .order_by(func.sum(DataCollection.points).desc())
        .limit(5)
        .all()
    )
    return {"top_point_earners": earners}

@router.get("/recent-activities")
async def get_recent_activities(db: Session = Depends(get_session)):
    activities = (
        db.query(User.name, Activity.activity, Activity.timestamp)
        .join(Activity, User.id == Activity.user_id)
        .order_by(Activity.timestamp.desc())
        .limit(10)
        .all()
    )
    return {"recent_activities": activities}
