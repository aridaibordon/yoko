LOCAL_SERVER_LIST = [
    ("submarine", "10.35.135.53"),
    ("pepper", "10.35.135.100"),
    ("soul", "10.35.135.98"),
    ("abbey", "10.35.135.99"),
    ("magical", "10.35.135.106"),
    ("help", "10.35.135.107"),
    ("white", "10.35.135.115"),
]

CMD_DICT = {
    "get_users": "eval getent passwd {$(awk '/^UID_MIN/ {print $2}' /etc/login.defs)..$(awk '/^UID_MAX/ {print $2}' /etc/login.defs)} | cut -d: -f1"
}
