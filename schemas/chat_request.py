from pydantic import BaseModel

class ChatRequest(
    BaseModel
):

    question:str

    address:str

    parcel:dict={}

    zoning:dict={}

    flood:dict={}

    fire:dict={}

    schools:dict={}

    highways:dict={}