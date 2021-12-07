from fastapi import APIRouter
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
import models, schemas
from database import get_db

router = APIRouter()


@router.get("/product", tags={"Products"})
def list_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()

    return products


@router.get("/product/{id}", tags={"Products"})
def retrieve_product(response: Response, id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
        return

    return product


@router.delete("/product/{id}", tags={"Products"})
def delete_product(id: int, db: Session = Depends(get_db)):
    product = (
        db.query(models.Product)
        .filter(models.Product.id == id)
        .delete(synchronize_session=False)
    )

    return product


@router.put("/product/{id}", tags={"Products"})
def update_product(request: schemas.Product, id: int, db: Session = Depends(get_db)):
    product = (
        db.query(models.Product).filter(models.Product.id == id).update(request.dict())
    )

    return product


@router.post(
    "/product",
    response_model=schemas.DisplayProduct,
    status_code=status.HTTP_201_CREATED,
    tags={"Products"},
)
def add_product(request: schemas.Product, db: Session = Depends(get_db)):
    new_product = models.Product(
        name=request.name,
        description=request.description,
        price=request.price,
        seller_id=1,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product