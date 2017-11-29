from django.core.management.base import BaseCommand, CommandError

from wagtail.wagtailcore.models import Page

from blog.models import LegacyBlogPage

from drupal_migration.models import Node, NodeRevision
from drupal_migration.models import FieldRevisionBody, FieldRevisionFieldTags
from drupal_migration.models import TaxonomyTermData


# from datetime import datetime
from datetime import datetime
from django.utils import timezone
import pytz


class Command(BaseCommand):
	help = 'Migrates pages from Drupal to Django'

	def handle(self, *args, **options):

		# Where in the site do we insert nodes under
		try:
			root_page = Page.objects.get(slug='weblog')
		except Page.DoesNotExist as pdne:
			self.stdout.write('Are you sure you created your root page?')

		for node_revision in NodeRevision.objects.all():
			self.stdout.write('Using revision {0} from node {1}'.format(node_revision.vid, node_revision.nid))

			current_timestamp = datetime.fromtimestamp(node_revision.timestamp)
			localised = pytz.timezone("UTC").localize(current_timestamp)

			# Try and load an existing page to add a new revision, create one if there isn't an existing page
			try:
				page = LegacyBlogPage.objects.get(drupal_id=node_revision.nid)
				# self.stdout.write("page found in db"))
			except LegacyBlogPage.DoesNotExist as dne:
				page = LegacyBlogPage()
				# self.stdout.write("Page not found in DB: instantiated")
			except Exception as ee:
				self.stdout.write("Unhandled Exception:")
				self.stdout.write(ee)

			if page.date == localised:
				# self.stdout.write('already done this page/revision/timestamp')
				continue

			page_content = FieldRevisionBody.objects.get(revision_id = node_revision.vid).body_value

			# self.stdout.write('about to add stuff to page')
			# I can fix broken previews (probably all of them ... Later)
			# Or just have smaller number of words, also easy option and possibly nicer to look at?
			page.preview = u'{0} ...'.format(page_content[:495])
			page.body = page_content
			page.date = localised
			page.title = node_revision.title
			page.revision_log = node_revision.log
			page.drupal_id = node_revision.nid

			# self.stdout.write('create tags')
			# Delete existing tags in case some are removed in this revision (eg Draft)
			page.tags.clear()
			# Establish page tags at this revision
			for current_tag in FieldRevisionFieldTags.objects.filter(revision_id = node_revision.vid):
				try:
					tag_name = TaxonomyTermData.objects.get(tid=current_tag.field_tags_tid).name
				except TaxonomyTermData.DoesNotExist as ttddne:
					# self.stdout.write(FieldRevisionFieldTags.objects.filter(revision_id = node_revision.vid).values())
					break

				page.tags.add(tag_name)

      # Ensure pages are not published during migration
      page.live = False

			# Use instead of save
			if not page.id:
				root_page.add_child(instance=page)

			# self.stdout.write('About to save revision')
			revision = page.save_revision(
					submitted_for_moderation=False,
			)
			# self.stdout.write('revision done')

