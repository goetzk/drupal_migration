# routers for mysql db (drupal)
# https://docs.djangoproject.com/en/1.11/topics/db/multi-db/#automatic-database-routing

class RouteDrupal(object):
	"""Correctly route queries for Drupal DB away from default"""

	def db_for_read(self, model, **hints):
		if model._meta.app_label == 'drupal_migration':
			return 'drupaldb'
		return None

	def db_for_write(self, model, **hints):
		if model._meta.app_label == 'drupal_migration':
			return 'drupaldb'
		return None


