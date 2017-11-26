# TODO: management command boilerplate

from wagtail.wagtailcore.models import Page

from blog.models import LegacyBlogPage

from drupal_migration.models import Node, NodeRevision
from drupal_migration.models import FieldRevisionBody, FieldRevisionFieldTags
from drupal_migration.models import TaxonomyTermData


# from datetime import datetime
from datetime import datetime
from django.utils import timezone
import pytz

# Where in the site do we insert nodes under
try:
  root_page = Page.objects.get(slug='weblog')
except Page.DoesNotExist as pdne:
  print 'Are you sure you created your root page?'

# TODO: if needed, hard code OUT publishing, I will review + publish by hand
for node_revision in NodeRevision.objects.all():

  current_timestamp = datetime.fromtimestamp(node_revision.timestamp)
  localised = pytz.timezone("UTC").localize(current_timestamp)

  # Try and load an existing page to add a new revision, create one if there isn't an existing page
  try:
    page = LegacyBlogPage.objects.get(drupal_id=node_revision.nid)
    print "page found in db"
  except LegacyBlogPage.DoesNotExist as dne:
    page = LegacyBlogPage()
    print "Page not found in DB: instantiated"
  except Exception as ee:
    print "Unhandled Exception:"
    print ee

  # FIXME: this isn't working
  # check if we've seen this before
  print 'comparing dates'
  print page.date
  print localised
  if page.date == localised:
    print 'already done this page/revision/timestamp'
    continue

  page_content = FieldRevisionBody.objects.get(revision_id = node_revision.vid).body_value

  print 'about to add stuff to page'
  # I can fix broken previews (probably all of them ... Later)
  # Or just have smaller number of words, also easy option and possibly nicer to look at?
  page.preview = '{0} ...'.format(page_content[:245])
  page.body = page_content
  page.date = localised
  page.title = node_revision.title
  page.revision_log = node_revision.log
  page.drupal_id = node_revision.nid

  print 'create tags'
  # Delete existing tags in case some are removed in this revision (eg Draft)
  page.tags.clear()
  # Establish page tags at this revision
  for current_tag in FieldRevisionFieldTags.objects.filter(revision_id = node_revision.vid):
    try:
      tag_name = TaxonomyTermData.objects.get(tid=current_tag.field_tags_tid).name
    except TaxonomyTermData.DoesNotExist as ttddne:
      print FieldRevisionFieldTags.objects.filter(revision_id = node_revision.vid).values()
      break

    page.tags.add(tag_name)

  # Use instead of save
  root_page.add_child(instance=page)

  print 'about to revision'
  revision = page.save_revision(
  #     user=self.import_user,
      submitted_for_moderation=False,
  )
  print 'revision done'

