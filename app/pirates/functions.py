import requests
from loguru import logger

base_endpoint = "https://tg-api-zehr.onrender.com"
libgen_endpoint = base_endpoint + "/api/v1/leecher/libgen"
ytsmx_endpoint = base_endpoint + "/api/v1/leecher/ytsmx"

async def get_libgen_links(file_name):
	payload  = {
		"book_name" : file_name
	}

	response = requests.post(libgen_endpoint, json=payload)
	logger.info(response)
	data_set = response.json()
	result = ""
	for data in data_set:
		result += f"{data['name']} - {data['size']} \n {data['link']} \n\n"

	return result

async def get_ytsmx_links(movie):
	response = requests.get(ytsmx_endpoint + f"/{movie}")
	data_set = response.json()
	logger.info(response)
	result = ""
	for data in data_set[:8]:
		result += f"{data['name']} - {data['size']} \n ```{data['magnet']}``` \n\n"

	return result