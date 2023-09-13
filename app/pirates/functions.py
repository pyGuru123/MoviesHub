import requests
from loguru import logger

base_endpoint = "https://tg-api-zehr.onrender.com"
libgen_endpoint = base_endpoint + "/api/v1/leecher/libgen"
ytsmx_endpoint = base_endpoint + "/api/v1/leecher/ytsmx"
piratesbay_endpoint = base_endpoint + "/api/v1/leecher/piratesbay"
bitsearch_endpoint = base_endpoint + "/api/v1/leecher/bitsearch"
magnetdl_endpoint = base_endpoint + "/api/v1/leecher/magnetdl"
nyaasi_endpoint = base_endpoint + "/api/v1/leecher/nyaasi"
zooqle_endpoint = base_endpoint + "/api/v1/leecher/zooqle"
x1337_endpoint = base_endpoint + "/api/v1/leecher/1337x"
kickass_endpoint = base_endpoint + "/api/v1/leecher/kickass"

cinevood_endpoint = base_endpoint + "/api/v1/gdtot/cinevood"

def parse_result(data_set):
	result = ""
	for data in data_set[:5]:
		result += f"<b>{data['name']} - {data['size']}</b> \n <code>{data['magnet']}</code> \n\n"

	if len(result) > 4096:
		result = ""
		for data in data_set[:4]:
			result += f"<b>{data['name']} - {data['size']}</b> \n <code>{data['magnet']}</code> \n\n"

	return result

async def get_libgen_links(file_name):
	payload  = {
		"book_name" : file_name
	}

	response = requests.post(libgen_endpoint, json=payload)
	data_set = response.json()
	result = ""
	for data in data_set:
		result += f"<b>{data['name']} - {data['size']}</b> \n {data['link']} \n\n"

	return result

async def get_piratesbay_links(movie):
	payload  = {
		"movie" : movie
	}

	response = requests.post(piratesbay_endpoint, json=payload)
	data_set = response.json()
	result = parse_result(data_set)

	return result

async def get_ytsmx_links(movie):
	payload  = {
		"movie" : movie
	}

	response = requests.post(ytsmx_endpoint, json=payload)
	data_set = response.json()
	result = parse_result(data_set)

	return result

async def get_bitsearch_links(movie):
	payload  = {
		"movie" : movie
	}

	response = requests.post(bitsearch_endpoint, json=payload)
	data_set = response.json()
	result = parse_result(data_set)

	return result

async def get_magnetdl_links(movie):
	payload  = {
		"movie" : movie
	}

	response = requests.post(magnetdl_endpoint, json=payload)
	data_set = response.json()
	result = parse_result(data_set)

	return result

async def get_nyaasi_links(movie):
	payload  = {
		"movie" : movie
	}

	response = requests.post(nyaasi_endpoint, json=payload)
	data_set = response.json()
	result = parse_result(data_set)

	return result

async def get_zooqle_links(movie):
	payload  = {
		"movie" : movie
	}

	response = requests.post(zooqle_endpoint, json=payload)
	data_set = response.json()
	result = parse_result(data_set)

	return result

async def get_1337x_links(movie):
	payload  = {
		"movie" : movie
	}

	response = requests.post(x1337_endpoint, json=payload)
	data_set = response.json()
	result = parse_result(data_set)

	return result

async def get_kickass_links(movie):
	payload  = {
		"movie" : movie
	}

	response = requests.post(kickass_endpoint, json=payload)
	data_set = response.json()
	result = parse_result(data_set)

	return result

async def get_cinevood_links(movie):
	payload  = {
		"movie" : movie
	}

	response = requests.post(cinevood_endpoint, json=payload)
	data_set = response.json()
	result = parse_result(data_set)

	return result