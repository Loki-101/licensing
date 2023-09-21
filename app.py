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
        
        # Extract the client's IP address from the request
        ip_address = request.headers.get("cf-connecting-ip")

        # Input validation
        if not license_key or not ip_address:
            return {"error": "Invalid input"}, 400

        # Query to check if the license and IP match
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT * FROM license_check WHERE license=%s AND ip=%s",
                    (license_key, ip_address)
                )
                valid = await cur.fetchone()
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
