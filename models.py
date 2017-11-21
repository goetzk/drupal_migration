# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models



# - field_data_body , page bodies (180 rows)
#   select entity_id, revision_id, body_value from field_data_body ;
class FieldDataBody(models.Model):
    entity_type = models.CharField(max_length=128)
    bundle = models.CharField(max_length=128)
    deleted = models.IntegerField()
    entity_id = models.IntegerField()
    revision_id = models.IntegerField(blank=True, null=True)
    language = models.CharField(max_length=32)
    delta = models.IntegerField()
    body_value = models.TextField(blank=True)
    body_summary = models.TextField(blank=True)
    body_format = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'field_data_body'


# - field_data_field_files, files uploaded in to drupal. (i only have 5, easier to manually move them?)
#   select entity_id, revision_id, delta, field_files_fid, field_files_description from field_data_field_files;
class FieldDataFieldFiles(models.Model):
    entity_type = models.CharField(max_length=128)
    bundle = models.CharField(max_length=128)
    deleted = models.IntegerField()
    entity_id = models.IntegerField()
    revision_id = models.IntegerField(blank=True, null=True)
    language = models.CharField(max_length=32)
    delta = models.IntegerField()
    field_files_fid = models.IntegerField(blank=True, null=True)
    field_files_display = models.IntegerField()
    field_files_description = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'field_data_field_files'


# - field_data_field_tags, map between node/pages and taxonomy/tags
#   select entity_id, revision_id, delta, field_tags_tid from field_data_field_tags;
class FieldDataFieldTags(models.Model):
    entity_type = models.CharField(max_length=128)
    bundle = models.CharField(max_length=128)
    deleted = models.IntegerField()
    entity_id = models.IntegerField()
    revision_id = models.IntegerField(blank=True, null=True)
    language = models.CharField(max_length=32)
    delta = models.IntegerField()
    field_tags_tid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'field_data_field_tags'


# - field_revision_body, appears to contain history of all fields. relationship to node_revision? (312 rows)
#   select entity_id, revision_id, body_value from field_revision_body ;
class FieldRevisionBody(models.Model):
    entity_type = models.CharField(max_length=128)
    bundle = models.CharField(max_length=128)
    deleted = models.IntegerField()
    entity_id = models.IntegerField()
    revision_id = models.IntegerField()
    language = models.CharField(max_length=32)
    delta = models.IntegerField()
    body_value = models.TextField(blank=True)
    body_summary = models.TextField(blank=True)
    body_format = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'field_revision_body'


# - field_revision_field_files, history of file changes (?); will skip (18 rows)
#   select * from field_revision_field_files ;
class FieldRevisionFieldFiles(models.Model):
    entity_type = models.CharField(max_length=128)
    bundle = models.CharField(max_length=128)
    deleted = models.IntegerField()
    entity_id = models.IntegerField()
    revision_id = models.IntegerField()
    language = models.CharField(max_length=32)
    delta = models.IntegerField()
    field_files_fid = models.IntegerField(blank=True, null=True)
    field_files_display = models.IntegerField()
    field_files_description = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'field_revision_field_files'


# - field_revision_field_tags (1097 rows!)
#   select entity_id, revision_id, delta, field_tags_tid from field_revision_field_tags;
class FieldRevisionFieldTags(models.Model):
    entity_type = models.CharField(max_length=128)
    bundle = models.CharField(max_length=128)
    deleted = models.IntegerField()
    entity_id = models.IntegerField()
    revision_id = models.IntegerField()
    language = models.CharField(max_length=32)
    delta = models.IntegerField()
    field_tags_tid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'field_revision_field_tags'


class FileManaged(models.Model):
    fid = models.IntegerField(primary_key=True)
    uid = models.IntegerField()
    filename = models.CharField(max_length=255)
    uri = models.CharField(unique=True, max_length=255)
    filemime = models.CharField(max_length=255)
    filesize = models.IntegerField()
    status = models.IntegerField()
    timestamp = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'file_managed'


class FileUsage(models.Model):
    fid = models.IntegerField()
    module = models.CharField(max_length=255)
    type = models.CharField(max_length=64)
    id = models.IntegerField()
    count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'file_usage'

class History(models.Model):
    uid = models.IntegerField()
    nid = models.IntegerField()
    timestamp = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'history'


# - node for page titles, created, updated, vid, status (published) (180 rows)
#   select vid, title, status, created, changed, promote from node;
class Node(models.Model):
    nid = models.IntegerField(primary_key=True)
    vid = models.IntegerField(unique=True, blank=True, null=True)
    type = models.CharField(max_length=32)
    language = models.CharField(max_length=12)
    title = models.CharField(max_length=255)
    uid = models.IntegerField()
    status = models.IntegerField()
    created = models.IntegerField()
    changed = models.IntegerField()
    comment = models.IntegerField()
    promote = models.IntegerField()
    sticky = models.IntegerField()
    tnid = models.IntegerField()
    translate = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'node'


# - node_revision for nid (node id; 'page'), vid (revision id?), title (page title), log, timestamp, status (published)  (312 rows)
#   select nid, vid, title, log, timestamp, status from node_revision;
class NodeRevision(models.Model):
    nid = models.IntegerField()
    vid = models.IntegerField(primary_key=True)
    uid = models.IntegerField()
    title = models.CharField(max_length=255)
    log = models.TextField()
    timestamp = models.IntegerField()
    status = models.IntegerField()
    comment = models.IntegerField()
    promote = models.IntegerField()
    sticky = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'node_revision'


# - taxonomy_index for created date (or ignore and simply attach to posts)
#   select * from taxonomy_index ;
class TaxonomyIndex(models.Model):
    nid = models.IntegerField()
    tid = models.IntegerField()
    sticky = models.IntegerField(blank=True, null=True)
    created = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'taxonomy_index'


# - taxonomy_term_data for tags (210 rows)
#   select name from taxonomy_term_data;
class TaxonomyTermData(models.Model):
    tid = models.IntegerField(primary_key=True)
    vid = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    format = models.CharField(max_length=255, blank=True)
    weight = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'taxonomy_term_data'


