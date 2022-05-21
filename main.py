import asyncio
import json
import re
import traceback
from typing import Set, List

from utils.api import get_homework, sign, login
from utils.httpcat import HttpCat


async def get_page(url: str) -> str:
    resp = await HttpCat.request("GET", url)
    if resp.code != 200:
        print(resp.text())
        raise ValueError(url+resp.status)
    return resp.text()


def load_account(path: str) -> List[List[str]]:
    return json.load(open(path, "rb"))


async def get_unfinish_spid(cookie: dict) -> Set[int]:
    need_to_work = []
    for hw in await get_homework(cookie):
        if hw["workStatus"] == "UnFinish":
            need_to_work.append(hw["url"])

    sp_ids = set()
    for url in need_to_work:
        try:
            html = await get_page(url)
        except ValueError as e:
            print(e)
            continue
        title = re.search("<title>(.*?)</title>", html)
        if title.group(1).startswith("跳转中"):
            if match := re.findall(r"location.replace\((.*?)\+", html):
                for r in match:
                    rp = url.replace("index.html", r.strip("' "))
                    if rp not in need_to_work:
                        need_to_work.append(rp)
                print("handled a redirect:", url)
            else:
                raise ValueError("new location not found")
        else:
            if match := re.search(r'data-specialId\s?="(\d*)"', html):
                sp_ids.add(match.group(1))
            else:
                raise ValueError("specialId not found")
    return sp_ids


async def do_it(username: str, password: str) -> bool:
    login_resp = await login(username, password)
    ret = login_resp.json()
    if ret["err_code"]:
        print(f"User: {username}: {ret['err_desc']}")
        return False
    spid = await get_unfinish_spid(login_resp.cookies)
    print(list(spid), "not finish")
    for i in spid:
        for s in range(1, 16):
            result = await sign(i, s, login_resp.cookies)
            if not (result["result"] or result["httpCode"] == 200):
                print(f"spid: {i}, step: {s}; return an error: [{result['httpCode']}]{result['msg']}")
            elif result["httpCode"] == 0:  # done
                print(f"spid: {i}: all done")
                break
            else:
                print(f"spid: {i}, step: {s}: done")
    print("all finished")
    return True


async def main():
    for (name, passwd) in load_account("accounts.json"):
        print("fetching:", name)
        try:
            await do_it(name, passwd)
        except:
            traceback.print_exc()


if __name__ == '__main__':
    asyncio.run(main())
