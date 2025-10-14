from fastapi.routing import APIRouter
from app.schemas.ganres import GanreListResponse
from app.db.database import LocalSession
from app.models.movie import Genre


router = APIRouter(
    prefix='/ganres',
    tags=['ganres']
)

@router.get('', response_model=GanreListResponse)
def get_ganres():
    db = LocalSession()
    ganres = db.query(Genre).all()
    return GanreListResponse(ganres=ganres)