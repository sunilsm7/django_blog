from rest_framework import permissions

class IsSuperUser(permissions.BasePermission):
	"""
	Custom permission to only allow superuser to retrieve or edit.
	"""
	def has_permission(self, request, view):
		return request.user and request.user.is_superuser