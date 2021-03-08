from pydantic import BaseSettings, AnyUrl

class Settings(BaseSettings):
    neo4j_url: str = "neo4j://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "foo"

settings = Settings()