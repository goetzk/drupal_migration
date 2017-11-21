from __future__ import unicode_literals

from django.db import models


# - field_data_body , page bodies (180 rows)
#   select entity_id, revision_id, body_value from field_data_body ;
# NOTE: this is current body, where FieldRevisionBody is all the previous revisions?
class FieldDataBody(models.Model):
    entity_type = models.CharField(max_length=128)            # Ignore, always node
    bundle = models.CharField(max_length=128)                 # ignore, always extended_thoughts or short thoughts
    deleted = models.IntegerField()                           # ignore, always 0
    entity_id = models.IntegerField()                         # ignore, always 2
    revision_id = models.IntegerField(blank=True, null=True)  # TODO: use this
    language = models.CharField(max_length=32)                # ignore, unset
    delta = models.IntegerField()                             # ignore, always 0
    body_value = models.TextField(blank=True)                 # text, actual body
    body_summary = models.TextField(blank=True)               # ignore, always blank
    body_format = models.CharField(max_length=255, blank=True) # ignore, don't care about the html supportedness

    class Meta:
        managed = False
        db_table = 'field_data_body'

# - field_data_field_files, files uploaded in to drupal. (i only have 5, easier to manually move them?)
#   select entity_id, revision_id, delta, field_files_fid, field_files_description from field_data_field_files;
class FieldDataFieldFiles(models.Model):
    entity_type = models.CharField(max_length=128)            # Ignore, always node
    bundle = models.CharField(max_length=128)                 # ignore, always extended_thoughts or short thoughts
    deleted = models.IntegerField()                           # ignore, always 0
    entity_id = models.IntegerField()                         # TODO: use this, it is node id
    revision_id = models.IntegerField(blank=True, null=True)  # TODO: use this, associates with a revision
    language = models.CharField(max_length=32)                # ignore, unset
    delta = models.IntegerField()                             # ignore, always 0
    field_files_fid = models.IntegerField(blank=True, null=True) # NOTE: unique file id: probably PK
    field_files_display = models.IntegerField()               # Ignore, all 1
    field_files_description = models.TextField(blank=True)    # TODO: use this, some have text

    class Meta:
        managed = False
        db_table = 'field_data_field_files'


# - field_data_field_tags, map between node/pages and taxonomy/tags
#   select entity_id, revision_id, delta, field_tags_tid from field_data_field_tags;
class FieldDataFieldTags(models.Model):
    entity_type = models.CharField(max_length=128)            # Ignore, always node
    bundle = models.CharField(max_length=128)                 # ignore, always extended_thoughts
    deleted = models.IntegerField()                           # ignore, always 0
    entity_id = models.IntegerField()                         # ignore, always 2
    revision_id = models.IntegerField(blank=True, null=True)  # NOTE: this changes
    language = models.CharField(max_length=32)                # ignore, undef
    delta = models.IntegerField()                             # ignore, changes but probably safe to ignore
    field_tags_tid = models.IntegerField(blank=True, null=True) # FIXME: is this an index? not sure what the numbers here relate to

    class Meta:
        managed = False
        db_table = 'field_data_field_tags'


# - field_revision_body, appears to contain history of all fields. relationship to node_revision? (312 rows)
#   select entity_id, revision_id, body_value from field_revision_body ;
# NOTE: has more revision_id's than FieldDataBody. that has 181 and this 314 (revision id is 322, some missing? deleted?)
# If they are duplicate when they match, I don't need to look at FieldDataBody
class FieldRevisionBody(models.Model):
    entity_type = models.CharField(max_length=128)            # Ignore, always node
    bundle = models.CharField(max_length=128)                 # ignore, always extended_thoughts
    deleted = models.IntegerField()                           # ignore, always 0
    entity_id = models.IntegerField()                         # NOTE: this changes, probably node id
    revision_id = models.IntegerField()                       # NOTE: this changes
    language = models.CharField(max_length=32)                # ignore, always undef
    delta = models.IntegerField()                             # ignore, always 0
    body_value = models.TextField(blank=True)                 # NOTE: use this
    body_summary = models.TextField(blank=True)               # ignore, always blank
    body_format = models.CharField(max_length=255, blank=True) # ignore, full vs limited html; don't care

    class Meta:
        managed = False
        db_table = 'field_revision_body'


# - field_revision_field_files, history of file changes (?); will skip (18 rows)
#   select * from field_revision_field_files ;
class FieldRevisionFieldFiles(models.Model):
    entity_type = models.CharField(max_length=128)            # Ignore, always node
    bundle = models.CharField(max_length=128)                 # ignore, always extended_thoughts
    deleted = models.IntegerField()                           # ignore, always 0
    entity_id = models.IntegerField()                         # NOTE: this changes
    revision_id = models.IntegerField()                       # NOTE: this changes
    language = models.CharField(max_length=32)                # ignore, always unde
    delta = models.IntegerField()                             # Varies, but will probably ignore it
    field_files_fid = models.IntegerField(blank=True, null=True) # NOTE: this changes, not 100% sure what it points at
    field_files_display = models.IntegerField()               # ignore, all 1
    field_files_description = models.TextField(blank=True)    # NOTE: some have text in them

    class Meta:
        managed = False
        db_table = 'field_revision_field_files'


# - field_revision_field_tags (1097 rows!)
#   select entity_id, revision_id, delta, field_tags_tid from field_revision_field_tags;
class FieldRevisionFieldTags(models.Model):
    entity_type = models.CharField(max_length=128)            # Ignore, always node
    bundle = models.CharField(max_length=128)                 # ignore, always extended_thoughts
    deleted = models.IntegerField()                           # ignore, always 0
    entity_id = models.IntegerField()                         # NOTE: this changes
    revision_id = models.IntegerField()                       # NOTE: this changes
    language = models.CharField(max_length=32)                # ignore, always unde
    delta = models.IntegerField()                             # Varies, but will probably ignore it
    field_tags_tid = models.IntegerField(blank=True, null=True) # NOTE: changes, but NFI what it points at

    class Meta:
        managed = False
        db_table = 'field_revision_field_tags'


class FileManaged(models.Model):
    fid = models.IntegerField(primary_key=True)         # NOTE: changes, unique here
    uid = models.IntegerField()                         # ignore, always 1 (user id, presumably)
    filename = models.CharField(max_length=255)         # NOTE: files name, useful
    uri = models.CharField(unique=True, max_length=255) # ignore, just filename with public:// prefixed to it
    filemime = models.CharField(max_length=255)         # NOTE: mime type, might be useful?
    filesize = models.IntegerField()                    # ignore, size probably isn't relevant
    status = models.IntegerField()                      # ignore, all 1
    timestamp = models.IntegerField()                   # NOTE: probably a publication/upload stamp

    class Meta:
        managed = False
        db_table = 'file_managed'


class FileUsage(models.Model):
    fid = models.IntegerField()                         # NOTE: maps to FileManaged.fid
    module = models.CharField(max_length=255)           # ignore, all file
    type = models.CharField(max_length=64)              # ignore, all node
    id = models.IntegerField()                          # NOTE: node id (Node.nid) / page its on
    count = models.IntegerField()                       # ignore, not sure what this is for

    class Meta:
        managed = False
        db_table = 'file_usage'


# - node for page titles, created, updated, vid, status (published) (180 rows)
#   select vid, title, status, created, changed, promote from node;
class Node(models.Model):
    nid = models.IntegerField(primary_key=True)                     # NOTE: use this, nodes unique ID
    vid = models.IntegerField(unique=True, blank=True, null=True)   # TODO: confirm, is this the current revision?
    type = models.CharField(max_length=32)                          # ignore, just extended/short thoughts
    language = models.CharField(max_length=12)                      # ignore, all undef
    title = models.CharField(max_length=255)                        # NOTE: use this, its text
    uid = models.IntegerField()                                     # ignore, all 1
    status = models.IntegerField()                                  # NOTE: published yes/no (1/0)
    created = models.IntegerField()                                 # NOTE: use this
    changed = models.IntegerField()                                 # NOTE: use this
    comment = models.IntegerField()                                 # ignore, all 0
    promote = models.IntegerField()                                 # ignore, i wasn't really using this properly
    sticky = models.IntegerField()                                  # ignore, all 0
    tnid = models.IntegerField()                                    # ignore, all 0
    translate = models.IntegerField()                               # ignore, all 0

    class Meta:
        managed = False
        db_table = 'node'


# - node_revision for nid (node id; 'page'), vid (revision id?), title (page title), log, timestamp, status (published)  (312 rows)
#   select nid, vid, title, log, timestamp, status from node_revision;
class NodeRevision(models.Model):
    nid = models.IntegerField()                     # NOTE: use this, nodes unique ID
    vid = models.IntegerField(primary_key=True)     # TODO: confirm, is this the current revision?
    uid = models.IntegerField()                     # ignore, all 0
    title = models.CharField(max_length=255)        # NOTE: use this
    log = models.TextField()                        # NOTE: use this
    timestamp = models.IntegerField()               # NOTE: use this
    status = models.IntegerField()                  # published yes/no (1/0)
    comment = models.IntegerField()                 # ignore, all 0
    promote = models.IntegerField()                  # ignore, not using anyway
    sticky = models.IntegerField()                  # ignore, all 0

    class Meta:
        managed = False
        db_table = 'node_revision'


# - taxonomy_index for created date (or ignore and simply attach to posts)
#   select * from taxonomy_index ;
class TaxonomyIndex(models.Model):
    nid = models.IntegerField()                          # NOTE: use this, TODO: FK on Node.nid (node id)
    tid = models.IntegerField()                          # NOTE: use this, TODO: FK on TaxonomyTermData.tid (term id)
    sticky = models.IntegerField(blank=True, null=True)  # ignore, all 0
    created = models.IntegerField()                      # NOTE: use this , TODO: return as datettime

    class Meta:
        managed = False
        db_table = 'taxonomy_index'


# - taxonomy_term_data for tags (210 rows)
#   select name from taxonomy_term_data;
class TaxonomyTermData(models.Model):
    tid = models.IntegerField(primary_key=True)         # NOTE: this changes
    vid = models.IntegerField()                         # NOTE: presumably version id, use this
    name = models.CharField(max_length=255)             # NOTE: keyword for tag
    description = models.TextField(blank=True)          # NOTE: description of tag
    format = models.CharField(max_length=255, blank=True) # ignore
    weight = models.IntegerField()                      # ignore

    class Meta:
        managed = False
        db_table = 'taxonomy_term_data'


