class Restriction:
    @staticmethod
    def get(key_string: str = '', user_id: int = 0, attempt: int = 0) -> None:
        from loader import cache
        return cache.get(
            key_string.format(user_id)
        )

    @staticmethod
    def set(key_string: str = '', key_value: str = '', user_id: int = 0, expires_at: int = 0, attempt: int = 0) -> bool:
        from loader import cache
        exist = Restriction.get(key_string, user_id)
        key_string = key_string.format(user_id)

        if not exist:
            cache.set(key_string, key_value)

        if expires_at > 0:
            cache.expire(key_string, (expires_at * 60))

        return True

    @staticmethod
    def action(key_string: str = '', user_id: int = 0, attempt: int = 0, expires_at: int = 0) -> None:
        from loader import cache
        exist = Restriction.get(key_string, user_id)

        if not exist:
            Restriction.set(key_string, 0, user_id, expires_at, attempt)
            cache.incr(key_string.format(user_id), amount=int(1))

        if exist and int(exist) < attempt:
            cache.incr(key_string.format(user_id), amount=int(1))

        if exist and int(exist) >= attempt:
            return True

        return False

    @staticmethod
    def delete(key_string: str = '', user_id: int = 0) -> None:
        from loader import cache
        cache.delete(key_string.format(user_id))
