import os
import json
import aiomysql
from robyn import Robyn

os.environ["ROBYN_URL"] = "0.0.0.0"

app = Robyn(__file__)

pool = None

@app.startup_handler
async def startup_handler():
    # Read configuration from environment variables
    db_user = os.getenv("DB_USER", "username")
    db_password = os.getenv("DB_PASSWORD", "password")
    db_host = os.getenv("DB_HOST", "Configure me first, moron!")
    db_name = os.getenv("DB_NAME", "license_db")
    db_port = int(os.getenv("DB_PORT", "3306"))
    if os.getenv("LOG_LEVEL") == "DEBUG":
        debug = True
    
    global pool
    pool = await aiomysql.create_pool(
        host=db_host, port=db_port,
        user=db_user, password=db_password,
        db=db_name
    )
    print("Database connected")

@app.shutdown_handler
async def shutdown_handler():
    global pool
    pool.close()
    await pool.wait_closed()

@app.post("/")
async def check_license(request):
    if os.getenv("LOG_LEVEL").lower() == "debug":
        debug = True
    else:
        debug = False
    try:
        # Extract the license_key from the JSON payload
        data = json.loads(request.body)
        license_key = data.get("license_key")
        
        headers_to_check = ["X-Forwarded-For", "Remote-Addr", "CF-Connecting-IP"]

        ip_address = None

        for header in headers_to_check:
            ip_address = request.headers.get(header)
            if ip_address:
                # If X-Forwarded-For contains multiple IPs (due to multiple proxies), take the first one
                if header == "X-Forwarded-For" and "," in ip_address:
                    ip_address = ip_address.split(",")[0].strip()
                break

        # If none of the headers provide the IP, use Robyn's method
        if not ip_address:
            ip_address = request.ip_addr

        # Input validation
        if not license_key or not ip_address:
            return {"error": "Invalid input"}, 400

        # Query to get the IP field for the given license_key
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT ip FROM license_check WHERE license=%s",
                    (license_key,)
                )
                result = await cur.fetchone()

        # If there's a result and the extracted IP is in the list of IPs for that license
        if result and ip_address in result[0].split(','):
            valid = True
        else:
            valid = False

        if debug:
            print(f"IP Address: {ip_address}")
            print(f"License Key: {license_key}")
            print(f"Query Result: {valid}")
        if valid:
            if debug:
                print("License verified")
            response_data = {"status": "success", "message": "License verified."}
            return json.dumps(response_data)
        else:
            if debug:
                print("License not found or IP mismatch")
            response_data = {"status": "failure", "message": "License not found or IP mismatch."}
            return json.dumps(response_data)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error occurred: {e}")
        return {"error": "Internal Server Error"}, 500

app.start(port=os.getenv("SERVER_PORT"))
import os
import json
import aiomysql
from robyn import Robyn

os.environ["ROBYN_URL"] = "0.0.0.0"

app = Robyn(__file__)

pool = None

@app.startup_handler
async def startup_handler():
    # Read configuration from environment variables
    db_user = os.getenv("DB_USER", "username")
    db_password = os.getenv("DB_PASSWORD", "password")
    db_host = os.getenv("DB_HOST", "Configure me first, moron!")
    db_name = os.getenv("DB_NAME", "license_db")
    db_port = int(os.getenv("DB_PORT", "3306"))
    if os.getenv("LOG_LEVEL") == "DEBUG":
        debug = True
    
    global pool
    pool = await aiomysql.create_pool(
        host=db_host, port=db_port,
        user=db_user, password=db_password,
        db=db_name
    )
    print("Database connected")

@app.shutdown_handler
async def shutdown_handler():
    global pool
    pool.close()
    await pool.wait_closed()

@app.post("/")
async def check_license(request):
    if os.getenv("LOG_LEVEL").lower() == "debug":
        debug = True
    else:
        debug = False
    try:
        # Extract the license_key from the JSON payload
        data = json.loads(request.body)
        license_key = data.get("license_key")
        
        headers_to_check = ["X-Forwarded-For", "Remote-Addr", "cf-connecting-ip"]

        ip_address = None

        for header in headers_to_check:
            ip_address = request.headers.get(header)
            if ip_address:
                # If X-Forwarded-For contains multiple IPs (due to multiple proxies), take the first one
                if header == "X-Forwarded-For" and "," in ip_address:
                    ip_address = ip_address.split(",")[0].strip()
                break

        # If none of the headers provide the IP, use Robyn's method
        if not ip_address:
            ip_address = request.ip_addr

        # Input validation
        if not license_key or not ip_address:
            return {"error": "Invalid input"}, 400

        # Query to get the IP field for the given license_key
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT ip FROM license_check WHERE license=%s",
                    (license_key,)
                )
                result = await cur.fetchone()

        # If there's a result and the extracted IP is in the list of IPs for that license
        if result and ip_address in result[0].split(','):
            valid = True
        else:
            valid = False

        if debug:
            print(f"IP Address: {ip_address}")
            print(f"License Key: {license_key}")
            print(f"Query Result: {valid}")
        if valid:
            if debug:
                print("License verified")
            response_data = {"status": "success", "message": "License verified."}
            return json.dumps(response_data)
        else:
            if debug:
                print("License not found or IP mismatch")
            response_data = {"status": "failure", "message": "License not found or IP mismatch."}
            return json.dumps(response_data)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error occurred: {e}")
        return {"error": "Internal Server Error"}, 500

app.start(port=os.getenv("SERVER_PORT"))
