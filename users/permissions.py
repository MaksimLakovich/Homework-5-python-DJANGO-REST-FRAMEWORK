from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """Кастомный permission-класс, проверяющий, является ли пользователь модератором. Модераторы - это пользователи,
    которые входят в группу "Moderators". Им разрешается просматривать (GET) и редактировать (PUT, PATCH) объекты,
    но не создавать (POST) и не удалять (DELETE)."""

    def has_permission(self, request, view):
        """Возвращает True, если пользователь аутентифицирован и состоит в группе "Moderators".
        Используется в контроллерах для ограничения доступа к операциям создания и удаления уроков/курсов."""

        return (
                request.user.is_authenticated and
                request.user.groups.filter(name="Moderators").exists()
        )
