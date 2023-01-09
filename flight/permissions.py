from rest_framework import permissions


class IsStafforReadOnly(permissions.IsAdminUser):   #isim neye izin verdiğini açıklamalı. Burada IsAdminUserı inherit ediyorum ve onun metodunu kendime göre customize ediyorum.
    def has_permission(self, request, view):   #permission her zaman true yada false döner
        if request.method in permissions.SAFE_METHODS:  #gelen metot create değilse(get ise) True dön, değilse staff ise True dön.
            return True
        return bool(request.user and request.user.is_staff)
#burada inherit kullandık. Object orientedın nimetlerinden faydalandık.