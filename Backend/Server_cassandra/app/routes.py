from fastapi import APIRouter, HTTPException
from cassandra.query import SimpleStatement
from .database import session
from .schemas import SubtitleCreate, SubtitleResponse
import uuid

router = APIRouter()

@router.post("/subtitles/", response_model=SubtitleResponse)
def create_subtitle(subtitle: SubtitleCreate):
    query = """
    INSERT INTO subtitle (id, id_music, start, end, text)
    VALUES (%s, %s, %s, %s, %s)
    """
    subtitle_id = uuid.uuid4()
    session.execute(
        query, (subtitle_id, subtitle.id_music, subtitle.start, subtitle.end, subtitle.text)
    )
    return SubtitleResponse(
        id=str(subtitle_id),
        id_music=subtitle.id_music,
        start=subtitle.start,
        end=subtitle.end,
        text=subtitle.text,
    )

@router.get("/subtitles/{subtitle_id}/", response_model=SubtitleResponse)
def get_subtitle(subtitle_id: str):
    query = "SELECT * FROM subtitle WHERE id = %s"
    result = session.execute(query, (uuid.UUID(subtitle_id),)).one()
    if not result:
        raise HTTPException(status_code=404, detail="Subtitle not found")
    return SubtitleResponse(
        id=str(result.id),
        id_music=result.id_music,
        start=result.start,
        end=result.end,
        text=result.text,
    )

@router.delete("/subtitles/{subtitle_id}/")
def delete_subtitle(subtitle_id: str):
    query = "DELETE FROM subtitle WHERE id = %s"
    session.execute(query, (uuid.UUID(subtitle_id),))
    return {"message": "Subtitle deleted successfully"}

@router.put("/subtitles/{subtitle_id}/", response_model=SubtitleResponse)
def update_subtitle(subtitle_id: str, subtitle: SubtitleCreate):
    query = """
    UPDATE subtitle
    SET id_music = %s, start = %s, end = %s, text = %s
    WHERE id = %s
    """
    session.execute(
        query, (subtitle.id_music, subtitle.start, subtitle.end, subtitle.text, uuid.UUID(subtitle_id))
    )
    return SubtitleResponse(
        id=subtitle_id,
        id_music=subtitle.id_music,
        start=subtitle.start,
        end=subtitle.end,
        text=subtitle.text,
    )

@router.get("/subtitles/", response_model=list[SubtitleResponse])
def get_all_subtitles():
    query = "SELECT * FROM subtitle"
    results = session.execute(query)
    return [SubtitleResponse(
        id=str(row.id),
        id_music=row.id_music,
        start=row.start,
        end=row.end,
        text=row.text,
    ) for row in results]

@router.get("/subtitles/by_music/{id_music}/", response_model=list[SubtitleResponse])
def get_subtitles_by_music(id_music: str):
    query = "SELECT * FROM subtitle WHERE id_music = %s ALLOW FILTERING"
    results = session.execute(query, (id_music,))
    return [SubtitleResponse(
        id=str(row.id),
        id_music=row.id_music,
        start=row.start,
        end=row.end,
        text=row.text,
    ) for row in results]
