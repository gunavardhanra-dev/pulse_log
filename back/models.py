from sqlalchemy import Index,ForeignKey, Integer, String, Text,Float, func
from sqlalchemy.orm import Mapped,mapped_column, relationship
from back.database import Base
from datetime import datetime, timezone
#models sql alc and also import from BASE

class User(Base):
    __tablename__="users"
    id: Mapped[int] = mapped_column(primary_key=True,index=True)
    username: Mapped[str] =mapped_column(nullable=False)
    age: Mapped[int] =mapped_column(nullable=False)
    weight:Mapped[float] =mapped_column(nullable=False)
    height:Mapped[float] =mapped_column(nullable=False)
    target_weight:Mapped[float] =mapped_column()
    weight_loss_rate:Mapped[float]=mapped_column(nullable=True)
    activity_level:Mapped[str]= mapped_column(nullable=True)
    average_daily_steps:Mapped[int]=mapped_column(nullable=True)
    goal_type:Mapped[str]=mapped_column(nullable=True) 
    email:Mapped[str]=mapped_column(unique=True,nullable=False)
    password:Mapped[str]=mapped_column(nullable=False)
    
class Weight_Log(Base):
    __tablename__="weight"
    id:Mapped[int]= mapped_column(primary_key=True, index=True)
    user_id:Mapped[int] =  mapped_column(ForeignKey("users.id"))
    weight:Mapped[float]= mapped_column()
    logged_at:Mapped[datetime]= mapped_column(nullable=False, default=func.now())
class meal_log(Base):
    __tablename__="calories"
    id:Mapped[int]=mapped_column(primary_key=True,index=True)
    user_id:Mapped[int]= mapped_column(ForeignKey("users.id"),nullable=False,index=True)
    food_name:Mapped[str]= mapped_column()
    quantity:Mapped[float]=mapped_column(nullable=False)
    calories_kcal:Mapped[float]=mapped_column(nullable=False)
    protein_g:Mapped[float]=mapped_column(nullable=False)
    carb_g:Mapped[float]=mapped_column(nullable=False)
    fats_g:Mapped[float]=mapped_column(nullable=False)
    logged_at:Mapped[datetime]= mapped_column(nullable=False, default=func.now())
    __table_args__=(
        Index('ix_calories_user_id_logged_at', 'user_id', 'logged_at'),
        #the "," in the end makes this a tupple lol quick note
    )
class habit_create(Base):
    __tablename__="habits"
    id:Mapped[int]=mapped_column(primary_key=True,index=True)
    user_id:Mapped[int]=mapped_column(ForeignKey("users.id"))
    habit:Mapped[str]=mapped_column(nullable=False)
    description:Mapped[str]=mapped_column(nullable=False)
class habit_log(Base):
    __tablename__ = "habit_logs"
    id:Mapped[int]=mapped_column(primary_key=True,index=False)
    user_id:Mapped[int]=mapped_column(ForeignKey("users.id"))
    habit_id:Mapped[int]=mapped_column(ForeignKey("habits.id"))
    completed:Mapped[bool]=mapped_column(nullable=False)
    duration:Mapped[float]=mapped_column(nullable=True)
    logged_at:Mapped[datetime]= mapped_column(nullable=False, default=func.now())

    habit:Mapped["habit_create"]= relationship("habit_create")
    # its simple dont get confused 
    # so basocially we are  creating a virtual python attribute "habit" which joins the habit_log and habit_create 
    # on the basis that i already connected them using the habit id and attached it to "habits.id"
    # oh there's a ForeignKey linking habit_logs.habit_id 
    # to habits.id — so when you ask for the relationship,
    # I'll use THAT to do the join