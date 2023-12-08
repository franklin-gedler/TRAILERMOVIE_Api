
# Valida si el payload recibido tiene las keys video_id, link_img, name_pelicula/name_serie y details
check_keys_payload_create_pelicula_serie = lambda data, tipo: all(key in data for key in ['video_id', 'link_img', 'details']) if f"name_{tipo}" in data else False

unpack_values_data_create_pelicula_serie = lambda data, keys_order, unidecode: [unidecode(data[key]).strip().capitalize() if key == 'name_pelicula' or key == 'name_serie' else data[key].strip() for key in keys_order]

# Valida si current_user es id 1 en la base de datos y el payload recibido tiene las keys username, password y allow
check_keys_payload_user_create = lambda data, user: all(key in data for key in ['username', 'password', 'allow']) if user.id == 1 else False

unpack_values_data_create_user = lambda data, keys_order, unidecode: [data[key].strip() if key == 'password' else unidecode(data[key]).strip().lower() for key in keys_order]


# Valida si el current_user es el super admin y valida si el payload recibido tiene la key user
is_current_user_super_admin = lambda data, user: True if 'user' in data and user.id == 1 else False

# Valida si el payload recibido tiene la key dada
check_key_payload = lambda data, key: True if key in data else False

# Valida si el usuario tiene permisos de escritura que a su vez tiene permisos de lectura
check_permissions_only_write = lambda user: True if user.user_permissions[0].permission_id == 2 else False

# Valida si el usuario tiene permisos de lectura y escritura
check_permissions_read_write = lambda user: True if user.user_permissions[0].permission_id in [1,2] else False

# Valida si el usuario esta deshabilitado
check_user_disable = lambda user: user.user_permissions[0].permission_id if user.user_permissions[0].permission_id != 3 else False