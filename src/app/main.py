from fastapi import FastAPI
import locale
from database import init_database
from prometheus_fastapi_instrumentator import Instrumentator

from routes import (
    auth_routes,
    errors_routes, 
    findtut_routes, 
    homepages_routes,
    landing_routes,
    studprofile_routes,
    tutprofile_routes,
    static_routes,
    studgrades_routes,
    studtests_routes,
    studtimetable_routes,
    tutgrades_routes,
    tuthomeworks_routes,
    tuttests_routes,
    tuttimetable_routes
)

app = FastAPI()

Instrumentator().instrument(app).expose(app)

try:
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
except locale.Error:
    print("Локаль не была корректно установлена")
    pass

@app.on_event("startup")
def startup_event():
    init_database()

app.include_router(auth_routes.router)
app.include_router(findtut_routes.router)
app.include_router(homepages_routes.router)
app.include_router(landing_routes.router)
app.include_router(studprofile_routes.router)
app.include_router(tutprofile_routes.router)
app.include_router(static_routes.router)
app.include_router(studgrades_routes.router)
app.include_router(studtests_routes.router)
app.include_router(studtimetable_routes.router)
app.include_router(tutgrades_routes.router)
app.include_router(tuthomeworks_routes.router)
app.include_router(tuttests_routes.router)
app.include_router(tuttimetable_routes.router)

app.add_exception_handler(404, errors_routes.error404)
app.add_exception_handler(500, errors_routes.error500)