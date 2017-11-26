# TODO: management command boilerplate

from wagtail.wagtailcore.models import Page

from blog.models import BlogPage

from drupal_migration.models import Node, NodeRevision
from drupal_migration.models import FieldRevisionBody, FieldRevisionFieldTags
from drupal_migration.models import TaxonomyTermData


from datetime import datetime

# Where in the site do we insert nodes under
root_page = Page.objects.get(slug='weblog')

# TODO: if needed, hard code OUT publishing, I will review + publish by hand
for node_revision in NodeRevision.objects.all():

  # Try and load an existing page to add a new revision, create one if there isn't an existing page
  try:
    page = BlogPage.objects.get(drupal_id=node_revision.nid)
    print "page found in db"
	except BlogPage.DoesNotExist as dne:
    page = BlogPage()
		print "Page not found in DB: instantiated"
  except Exception as ee:
    print "Unhandled Exception:"
    print ee

	page.date = datetime.fromtimestamp(node_revision.timestamp)
  page.title = node_revision.title
  page.body = FieldRevisionBody.objects.get(revision_id = node_revision.vid).body_value
  page.revision_log = node_revision.log

  # Delete existing tags in case some are removed in this revision (eg Draft)
  page.tags.clear()
  # Establish page tags at this revision
  for current_tag in FieldRevisionFieldTags.objects.filter(revision_id = node_revision.vid):
    tag_name = TaxonomyTermData.objects.get(tid=current_tag.field_tags_tid).name
    page.tags.add(tag_name)

	revision = page.save_revision(
	# 		user=self.import_user,
			submitted_for_moderation=False,
	)

  # Use instead of save
  root_page.add_child(instance=page)

