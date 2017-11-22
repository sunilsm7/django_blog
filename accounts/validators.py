from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_domainonly_email(value):
	"""
	Let's validate the email passed is in the domain "yourdomain.com"
	"""
	if not "yourdomain.com" in value:
		raise ValidationError("Sorry, the email submitted is invalid. All emails have to be registered on this domain only.")


def validate_not_allowed_domain(value):
	"""
	Let's validate the email passed is in our blacklist.
	"""
	blacklist_domain = ['.edu','.org','.biz']
	if value in blacklist_domain:
		raise ValidationError("Sorry, we don\'t accept this domain email address.")
