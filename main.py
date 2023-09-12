import uvcorn
from os import getenv
if __name__ == "__main__":
    port=getenv("PORT", 8000)
    uvcorn.run("app.Api:app", host="0.0.0.0", port=port, reload=True)