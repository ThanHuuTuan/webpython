from sqlalchemy import true

from app.models import *
from app import db


def read_data(tensach1=None):
    sach = Sach.query.all()
    if tensach1:
        sach = [p for p in sach if p["tensach"].find(tensach1) >= 0]
    return sach


def list_theloai():
    theloai1 = Loaisach.query.all()
    return theloai1


def timkiem(loai=None, kw=None):
    if loai == "ten":
        sach = Sach.query.filter(Sach.tensach.contains(kw))
    if loai == "nxb":
        sach = Sach.query.join(Nxb, Sach.Nxb_id == Nxb.id).filter(Nxb.tennxb.contains(kw))
    if loai == "test":
        sach = Sach.query.join(Loaisach, Sach.loaisach_id == Loaisach.id).filter(Loaisach.tenloai.contains(kw))

    return sach


def check_user(username, password):
    user = User.query.filter(User.username == username, User.password == password).first()
    if user:
        return user
    else:
        return None


def add_user(name, username, password):
    dem = User.query.count()
    user = User(name=name, active=1, username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return dem
