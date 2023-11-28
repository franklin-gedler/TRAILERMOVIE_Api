check_keys_payload_pelicula_serie = lambda data, tipo: all(key in data[tipo] for key in ['video_id', 'link_img', 'name', 'details']) if tipo in data else False

check_keys_payload_user = lambda data, user: all(key in data['user'] for key in ['username', 'password', 'allow']) if 'user' in data and user.id == 1 else False

check_permissions_only_write = lambda user: True if user.user_permissions[0].permission_id == 2 else False

check_permissions_read_write = lambda user: True if user.user_permissions[0].permission_id in [1,2] else False