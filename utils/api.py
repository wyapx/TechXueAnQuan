import json
from typing import List

from .httpcat import HttpCat, HttpResponse


async def sign(special_id: int, step: int, cookie: dict):
    resp = await HttpCat.request(
        "POST",
        "https://huodongapi.xueanquan.com/p/guangdong/Topic/topic/platformapi/api/v1/records/sign",
        {"Content-Type": "application/json"},
        json.dumps({
            "specialId": special_id,
            "step": step
        }).encode(),
        cookie
    )
    if resp.code == 200:
        return resp.json(verify_type=False)
    else:
        raise ValueError(resp.status)


async def get_homework(cookie: dict) -> List[dict]:
    resp = await HttpCat.request(
        "GET",
        "https://yyapi.xueanquan.com/guangdong/safeapph5/api/v1/homework/homeworklist",
        cookies=cookie
    )
    if resp.code == 200:
        return resp.json(verify_type=False)
    else:
        raise ValueError(resp.status)


async def login(username: str, password: str) -> HttpResponse:
    return await HttpCat.request(
        "POST",
        "https://appapi.xueanquan.com/usercenter/api/v3/wx/login?checkShowQrCode=true&tmp=false",
        {
            "Content-Type": "application/json;charset=utf-8",
            "Origin": "https://guangzhou.xueanquan.com"
        },
        body=json.dumps({
            "loginOrigin": 1,
            "username": username,
            "password": password
        }).encode()
    )
