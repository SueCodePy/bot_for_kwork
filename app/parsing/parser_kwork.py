import aiohttp
import asyncio
from config.config import settings
from app.data_base.crud import add_kwork


cookies = settings.cookies
headers = settings.headers


async def run_parser():

    async with aiohttp.ClientSession(headers=headers, cookies=cookies) as session:
        page = 1
        last_page = 1
        list_kwork_id = []
        while page <= last_page:
            data = {
                'page': (None, str(page))
            }
            async with session.post('https://kwork.ru/projects', data=data) as resp:
                res = await resp.json()
                # last_page = res['data']['pagination']['last_page']

                for el in res['data']['pagination']['data']:
                    descr = el['description'][:2999] if len(el['description']) > 3000 else el['description']
                    kw_price = float(el['priceLimit'])
                    kw_cnt = el['kwork_count']
                    status = el['status']
                    time_limit = el['timeLeft']
                    kw_id = int(el['id'])
                    #link = ''.join([d['url'] for d in el['links'] if d['active']])
                    link = f"https://kwork.ru/projects/{kw_id}"
                    is_new = await add_kwork(
                        kw_id=kw_id,
                        descr=descr,
                        kw_cnt=kw_cnt,
                        kw_price=kw_price,
                        url_page=link)
                    if is_new:
                        list_kwork_id.append(int(el['id']))

            page += 1
            await asyncio.sleep(1)

    return list_kwork_id


