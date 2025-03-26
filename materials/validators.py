import re

from rest_framework import serializers


class DescriptionValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        pattern = re.compile(r"(?:https?://)?(?:www\.)?(youtube\.com|youtu\.be)")  # Проверяет также сокращённые ссылки

        field_to_validate = dict(value).get(self.field)
        if "https://" in field_to_validate or "http://" in field_to_validate:
            if not pattern.match(field_to_validate):
                raise serializers.ValidationError("Ссылка на другие каналы кроме youtube не допустима.")
