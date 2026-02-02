from sqlmodel import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(f"postgresql+psycopg://{os.getenv("USERNAME")}:{os.getenv("PASSWD")}@localhost:5432/test", echo=True) 