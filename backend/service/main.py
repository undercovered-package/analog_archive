import uvicorn
import uvloop

from service.api.app import create_app

uvloop.install()

app = create_app()

if __name__ == "__main__":
    uvicorn.run("service.main:app", host="0.0.0.0")
