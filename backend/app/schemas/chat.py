from pydantic import AliasChoices, BaseModel, ConfigDict, Field

class ChatRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    message: str = Field(
        min_length=1,
        validation_alias=AliasChoices("message", "question"),
    )


