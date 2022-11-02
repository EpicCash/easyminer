import time
import requests
from flaskwebgui import FlaskUI
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from backend import provider
from backend.calculator.models import *


ORIGINS = ['*']
app = FastAPI()

app.add_middleware(
            CORSMiddleware,
            allow_origins=ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

app.mount("/frontend/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

# ui = FlaskUI(app, start_server='fastapi', width=500, height=900)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.post("/calculate")
async def calculate(parser: Parser):
    parser.parse()
    print(parser)
    rig = Rig(**parser.dict(include={'hashrate', 'algorithm', 'power_consumption'}))
    currency = Currency(**provider.MarketData().get(parser.currency))
    blockchain = Blockchain(**provider.BlockchainData().get_last_block())
    calc = Calculator(rig=rig, blockchain=blockchain, currency=currency,
                      pool_fee=parser.pool_fee, energy_price=parser.energy_price)
    print(calc)
    # print(calc.get_report(as_dict=False).formatted())
    return calc.get_report()

# @app.get('/keep-alive/')
# async def keep_alive():
#     """
#     Front-end needs to ping this endpoint to keep connection,
#     we will use it also as front-end dashboard update thread.
#     """
#     request = requests.get("https://epic-radar.com/api/explorer/blocks/")
#     if request.status_code in [200, 2001]:
#         block = request.json()['results'][0]
#
#         algo = block['algo']
#         height = block['height']
#         avg_time = block['avg_time']
#         timestamp = block['timestamp']
#         total_diffs = block['target_diffs']
#         network_hashrate = block['network_hashrate']
#
#         last_block_delta = time.time() - timestamp
#
#         if last_block_delta < 60:
#             delta = f'< minute ago'
#         else:
#             delta = f"{int(last_block_delta / 60)} minute{'s' if last_block_delta / 60 > 2 else ''} ago"
#
#         algo_icons = {
#             'randomx': {'icon': '<span class="material-icons">memory</span>', 'text': 'RandomX'},
#             'progpow': {'icon': '<span class="material-icons">sports_esports</span>', 'text': 'ProgPoW'},
#             'cuckoo': {'icon': '<span class="material-icons">dns</span> ', 'text': 'Cuckoo'},
#                         }
#
#         return {'delta': delta, 'height': height, 'algo': algo_icons[algo]}
#
#     return {'----'}
# @app.post("/login/", response_class=HTMLResponse)
# async def login(request: Request, password: str = Form(default=None)):
#     print(GPUtil.showUtilization())
#     context = {"request": request,
#                'password': password,
#                'gpus': GPUtil.getGPUs()[0]}
#     return templates.TemplateResponse("home.html", context)


# if __name__ == "__main__":

