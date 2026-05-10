from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.image import Image
from app.models.user import User
from app.core.config import settings
from app.routers.auth import get_current_user
import cloudinary
import cloudinary.uploader

router = APIRouter()

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)


@router.post("/{entity_type}/{entity_id}/images", status_code=201)
async def upload_image(
    entity_type: str,
    entity_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Only admins can upload
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can upload")

    if entity_type not in ["course", "lesson", "user"]:
        raise HTTPException(status_code=400, detail="Invalid entity type")

    if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(
            status_code=400, detail="Only JPEG, PNG, WebP allowed")

    contents = await file.read()
    upload_result = cloudinary.uploader.upload(
        contents,
        folder=f"lms/{entity_type}_{entity_id}",
        resource_type="image"
    )
    image_url = upload_result["secure_url"]

    new_image = Image(
        entity_type=entity_type,
        entity_id=entity_id,
        image_url=image_url
    )
    db.add(new_image)
    await db.commit()
    await db.refresh(new_image)

    return {"message": "Image uploaded", "image_url": image_url, "image_id": new_image.id}


@router.get("/{entity_type}/{entity_id}/images")
async def get_images(
    entity_type: str,
    entity_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Image).where(Image.entity_type ==
                            entity_type, Image.entity_id == entity_id)
    )
    images = result.scalars().all()
    return images


@router.delete("/images/{image_id}", status_code=204)
async def delete_image(
    image_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can delete")

    result = await db.execute(select(Image).where(Image.id == image_id))
    image = result.scalar_one_or_none()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    await db.delete(image)
    await db.commit()
    return None
